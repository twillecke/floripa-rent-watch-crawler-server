from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import sys, os
abspt = os.path.abspath('../../')
sys.path.append(abspt)
from query import Database


class DuplicatesPipeline:

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
    #Instanceing database connection
    def process_item(self, item, spider):
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

        #Inserting into Database
        db = Database() 
        db.insert_item(data)

        return item

class ZapimoveisPipeline:
    def process_item(self, item, spider):
        return item
