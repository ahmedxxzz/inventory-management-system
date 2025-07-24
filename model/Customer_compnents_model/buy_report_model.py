import sqlite3


class BuyReportModel:
    def __init__(self):
        self.conn = sqlite3.connect('IMS.db')
        self.cursor = self.conn.cursor()
        



    def get_cus_id_from_name(self, name):
        self.cursor.execute("SELECT customer_id FROM Customers WHERE name = ?", (name,))
        return self.cursor.fetchone()[0]


    def get_product_id_from_code(self, code):
        self.cursor.execute("SELECT product_id FROM Products WHERE type = ?", (code,))
        return self.cursor.fetchone()[0]


    def get_product_price_from_id(self, code):
        self.cursor.execute("SELECT cus_price_per_piece FROM Products WHERE product_id = ?", (int(code),))
        return self.cursor.fetchone()[0]


    def get_cus_money_by_id(self, id):
        self.cursor.execute(f"SELECT {'Golden_Rose_amount_money' if self.supplier == 'golden rose' else 'Snow_White_amount_money'} FROM Customers WHERE customer_id = ?", (id,))
        data = self.cursor.fetchone()
        if data :
            return data[0]
        else :
            return 0

