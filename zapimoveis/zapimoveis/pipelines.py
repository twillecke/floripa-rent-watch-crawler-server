from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import psycopg2 as pg


class DuplicatesPipeline:
"""Remove Duplicate items by ID"""
    def __init__(self):
        self.id_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['id'] in self.id_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.id_seen.add(adapter['id'])
            return item


class StorageDBPipeline:
   """Inserts each item into DB"""
    def __init__(self):
        self.db_conn = pg.connect(
            host="localhost",
            database="rent_watch",
            port=5432,
            user="postgres",
	    password="password" # Use the real password here!
        )

    def process_item(self, item, spider):
        with self.db_conn.cursor() as cursor:
            sql = """
                INSERT INTO rent_data (
                job_id,
                rent_id,
                address,
                region,
                city,
                state,
                housing_type,
                rent_type,
                price,
                cond_price,
                iptu_price,
                size_m2,
                bedroom_count,
                parking_count,
                bathroom_count,
                datetime )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            adapter = ItemAdapter(item)
            data = [-987,
                    adapter['id'], adapter['address'], adapter['region'], 'Florianopolis', 'SC',
                    adapter['housing_type'], adapter['rent_type'], adapter['price'],
                    adapter['condominium'], adapter['iptu_price'],
                    adapter['size_m2'], adapter['bedroom_count'], adapter['parking_count'],
                    adapter['bathroom_count'], 'NOW()'
                    ]

            for k in range(len(data)):
                if data[k] == 'None':
                    data[k] = None

            cursor.execute(sql, data)
            self.db_conn.commit()
        return item

    def close_spider(self, spider):
        self.db_conn.close()

class ZapimoveisPipeline:
    def process_item(self, item, spider):
        return item
