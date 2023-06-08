import psycopg2 as pg
import datetime
from password import pg_pw, aes_key


class Database():

    def __init__(self):

        self.DB_HOST = 'localhost'
        self.DB_NAME = 'rent_watch'
        self.DB_PORT = 5432
        self.DB_USER = 'postgres'

        self.conn = pg.connect(
            host=self.DB_HOST,
            database=self.DB_NAME,
            port=self.DB_PORT,
            user=self.DB_USER,
            password=pg_pw()
        )

        self.cur = self.conn.cursor()

    def test_conn(self):
        print(self.conn)

    def close_conn(self):
        self.conn.close()

    def fetch_last_job_stats(self):
        try:
            cur = self.cur

            sql_stats = "SELECT * FROM job_stats ORDER BY 1 DESC LIMIT 1;"

            sql_columns = """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = 'job_stats';
            """

            cur.execute(sql_stats)
            stats = cur.fetchone()

            stats = [stat for stat in stats]

            cur.execute(sql_columns)
            columns = cur.fetchall()

            columns = [elem[0] for elem in columns]

            return stats, columns

        except Exception as error:
            return error

    def insert_into_job_stats(self, obj):
        try:
            conn = self.conn
            cur = self.cur

            sql_insert = """
                         INSERT INTO job_stats
                         (spider_name, item_count, item_drop_count, start_time, finish_time,
                         duration, request_count, response_count, finish_reason, max_depth)
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                         """

            cur.execute(sql_insert, obj)

            conn.commit()

        except Exception as error:
            return error

    def insert_item(self, obj):
        try:
            conn = self.conn
            cur = self.cur

            sql_insert = """
                         INSERT INTO rent_data (
                         job_id, rent_id,
                         address, region,
                         city, state,
                         housing_type, rent_type,
                         price, cond_price,
                         iptu_price, size_m2,
                         bedroom_count, parking_count,
                         bathroom_count, datetime )
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s,
                                 %s, %s, %s, %s, %s, %s, %s, %s);
                         """

            cur.execute(sql_insert, obj)
            conn.commit()

        except Exception as error:
            return error

    def fetch_mailing_list(self):
        try:
            conn = self.conn
            cur = self.cur

            sql_select = f"""
                        SELECT convert_from(decrypt(email,\'{aes_key()}\','AES'),'SQL_ASCII')
                        FROM mailing_list
                        WHERE status = 1;
                        """

            cur.execute(sql_select)

            mail_list = cur.fetchall()
            mail_list = [mail[0] for mail in mail_list]

            return mail_list

        except Exception as error:
            return error

    def activate_mailing_list(self, email):
        try:
            conn = self.conn
            cur = self.cur

            sql_update = f"""
                        UPDATE mailing_list
                        SET status = 1
                        WHERE email = encrypt(\'{email}\', \'{aes_key()}\', 'AES')
                        """

            cur.execute(sql_update)
            conn.commit()

        except Exception as error:
            return error

    def deactivate_mailing_list(self, email):
        try:
            conn = self.conn
            cur = self.cur

            sql_update = f"""
                        UPDATE mailing_list
                        SET status = 0
                        WHERE email = encrypt(\'{email}\',\'{aes_key()}\', 'AES')
                        """

            cur.execute(sql_update)
            conn.commit()

        except Exception as error:
            return error

    def insert_into_mailing_list(self, email):
        try:
            conn = self.conn
            cur = self.cur

            sql_insert = f"""
                        INSERT INTO mailing_list (email, status)
                        VALUES (encrypt(\'{email}\',\'{aes_key()}\', 'AES') , 1)
                        """

            cur.execute(sql_insert)
            conn.commit()


        except Exception as error:
            return error


if __name__ == "__main__":
    db = Database()
    print(db.fetch_mailing_list())
