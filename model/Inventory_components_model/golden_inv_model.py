import sqlite3


class GoldenInvModel:
    def __init__(self):
        self.conn = sqlite3.connect('IMS.db')
        self.cursor = self.conn.cursor()


    def get_products_info(self):
        return self.cursor.execute("SELECT type, current_quantity, cus_price_per_piece FROM Products where resource_name = 'golden rose'").fetchall()

    def search_product(self, product_code):
        self.cursor.execute("SELECT type, current_quantity, cus_price_per_piece FROM Products WHERE type LIKE ? and resource_name='golden rose'", ('%' + product_code + '%',))
        return self.cursor.fetchall()
