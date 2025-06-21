import sqlite3
from sqlite3 import Error


class ReturnModel:
    def __init__(self):
        self.conn = sqlite3.connect('IMS.db')
        self.cursor = self.conn.cursor()
        self.data = [
            # [facname, time, productcode,  quantity, reason]
            ['عمر خالد', '2025-04-21 20:53:29', 1001, 200,'علشان اهبل'],
            ['علاء احمد', '2025-04-21 21:56:29', 1001, 500,'علشان اهبل'],
            ['علاء احمد', '2025-04-21 22:54:29', 1001, 600,'علشان اهبل'],
            ['علاء احمد', '2025-04-21 19:49:29', 1001, 200,'علشان اهبل'],
            ['علاء احمد', '2025-04-21 20:52:29', 1002, 600,'علشان اهبل'],
        ]



    def check_factory_name_exist(self, fac_name):
        # self.cursor.execute("SELECT * FROM Factories WHERE name = ?", (fac_name,))
        # return self.cursor.fetchone()
        return True
    
    def check_product_code_exist(self, product_code):
        # self.cursor.execute("SELECT * FROM Products WHERE code = ?", (product_code,))
        # return self.cursor.fetchone()
        return True
    
    def save_return_to_db(self, data):
        return True

    def get_returns_from_db(self):
        # self.cursor.execute("SELECT * FROM Returns")
        # return self.cursor.fetchall()
        return self.data
    
    def get_factory_names_and_money(self):
        # self.cursor.execute("SELECT name, amount_money FROM Factories")
        # return self.cursor.fetchall()
        return [('حماده طلبة', 50000.0),('عمرو هلال', 75000.0),('علاء احمد', 30000.0),]
    
    def get_products_codes(self):
        # self.cursor.execute("SELECT type FROM Products")
        # return self.cursor.fetchall()
        return [(row,0) for row in range(1001, 1020)]