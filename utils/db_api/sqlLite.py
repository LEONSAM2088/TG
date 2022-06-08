import os
import sqlite3 as lite

con = lite.connect("mydatabase.db")


class DB:
    @staticmethod
    def insert_item(title, price, description, photo_link, metro_station, weight, type1):
        sql = f"INSERT INTO ITEM(title, price, description, photo_link, metro_station, weight, type) values('{title}', {price}, '{description}', '{photo_link}', '{metro_station}', {weight}, '{type1}')"
        con.execute(sql)
        con.commit()

    @staticmethod
    def delete_item(price):
        sqlSelect = f"select id, photo_link from ITEM where price = '{price}' ORDER BY id LIMIT 1"

        cursor = con.cursor()
        cursor.execute(sqlSelect)
        records = cursor.fetchone()

        con.commit()
        sql = f"""DELETE FROM ITEM WHERE id = {records[0]}"""
        con.execute(sql)
        con.commit()
        if os.path.isfile(f'photos/{records[1]}'):
            os.remove(f'photos/{records[1]}')
        else:
            print("File doesn't exists!")

    @staticmethod
    def insert_order(user_id, price, tp, station):

        sql = f"INSERT INTO ORDERUSER(user_id, price, type_item, station) values({user_id}, {price}, '{tp}', '{station}')"
        con.execute(sql)
        con.commit()

    @staticmethod
    def delete_order(user_id):
        sql = f"""DELETE FROM ORDERUSER WHERE user_id = {user_id}"""
        con.execute(sql)
        con.commit()

    @staticmethod
    def select_one_item(type_item, price, station):
        sql = f"""SELECT * FROM ITEM WHERE type = '{type_item}' AND metro_station = '{station}' AND price = {price} AND blocked=true ORDER BY id LIMIT 1"""
        cursor = con.cursor()
        cursor.execute(sql)
        records = cursor.fetchone()
        con.commit()
        return records

    @staticmethod
    def block_item(id):
        return id

    @staticmethod
    def select_items():
        sql = f"""SELECT * FROM ITEM"""
        cursor = con.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        con.commit()
        return records

    @staticmethod
    def select_order(id_order):
        sql = f"""SELECT * FROM ORDERUSER WHERE user_id = '{id_order}'"""
        cursor = con.cursor()
        cursor.execute(sql)
        records = cursor.fetchone()
        con.commit()
        return records

    @staticmethod
    def check_exist(id_user):
        try:

            author_ids = con.execute(f"select id from ORDERUSER where user_id = '{id_user}'").fetchone()[0]
            return True
        except:
            return False

    @staticmethod
    def check_item(price, station):

        try:

            author_ids = con.execute(f"select id from ITEM where blocked=0 and metro_station='{station}' and price={price}").fetchone()[0]
            return True
        except:
            return False
    @staticmethod
    def check_exist_item(type_item, station, price):
        try:

            author_ids = con.execute(
                f"select id from ITEM where type = '{type_item}' AND metro_station = '{station}' AND price = {price}").fetchone()[
                0]
            return True
        except:
            return False

    @staticmethod
    def reserve_item(price, station):
        sql = f"UPDATE ITEM SET blocked = 1 where blocked=0 and metro_station='{station}' and price={price}"
        con.execute(sql)
        con.commit()

    @staticmethod
    def unreserve_item(price, station):
        sql = f"UPDATE ITEM SET blocked = 0 where blocked=1 and metro_station='{station}' and price={price}"
        con.execute(sql)
        con.commit()

    @staticmethod
    def unreserve_any_item():
        try:
            sql = f"UPDATE ITEM SET blocked = 0 where blocked=1"
            con.execute(sql)
            con.commit()
        except:
            print("err")