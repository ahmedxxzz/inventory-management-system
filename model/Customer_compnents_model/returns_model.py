import sqlite3
from datetime import datetime

class ReturnModel:
    def __init__(self, supplier):
        self.conn = sqlite3.connect('IMS.db')
        self.cursor = self.conn.cursor()
        self.supplier = supplier



    def check_customer_name_exist(self, cus_name):
        self.cursor.execute("SELECT name FROM Customers WHERE name = ?", (cus_name,))
        cus  = self.cursor.fetchone()[0]
        if cus:
            return True
        return False


    def check_product_code_exist(self, product_code):
        self.cursor.execute("SELECT product_id FROM Products WHERE type = ?", (product_code,))
        if self.cursor.fetchone()[0]:
            return True
        return False


    def check_product_quantity(self, product_code):
        self.cursor.execute("SELECT current_quantity FROM Products WHERE type = ?", (product_code,))
        return self.cursor.fetchone()[0]


    def save_return_to_db(self, data):
        '''
        insert the returned data 
        then reduce the product quantity
        then reduce the customer money and quantity
        
        '''
        customer_id = self.cursor.execute("SELECT customer_id FROM Customers WHERE name = ?", (data[0],)).fetchone()[0]
        product_id = self.cursor.execute("SELECT product_id FROM Products WHERE type = ?", (data[1],))
        price_per_piece = self.cursor.execute("SELECT cus_price_per_piece FROM Products WHERE type = ?", (data[1],)).fetchone()[0]
        self.cursor.execute('''INSERT INTO Cus_Returned_Items (date, product_id, quantity, reason, price_per_piece,  customer_id, resource_name)  VALUES (?, ?, ?, ?, ?, ?, ?);''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), product_id, int(data[2]), data[3],  price_per_piece, customer_id, self.supplier))
        self.cursor.execute("UPDATE Products SET current_quantity = current_quantity + ? WHERE product_id = ?", (int(data[2]), product_id))
        if self.supplier == 'golden rose':
            self.cursor.execute("UPDATE Customers SET Golden_Rose_amount_money = Golden_Rose_amount_money - ? ,Golden_Rose_current_quantity = Golden_Rose_current_quantity - ? WHERE customer_id = ?", (float(price_per_piece) * int(data[2]), int(data[2]), customer_id))
        else:
            self.cursor.execute("UPDATE Customers SET Snow_White_amount_money = Snow_White_amount_money - ? ,Snow_White_current_quantity = Snow_White_current_quantity - ? WHERE customer_id = ?", (float(price_per_piece) * int(data[2]), int(data[2]), customer_id))
        self.conn.commit()
        return True


    def get_returns_from_db(self):


        self.cursor.execute('''
                            SELECT
                                    C.name AS cus_name,
                                    CRI.date AS time,
                                    P.type AS productcode,
                                    CRI.quantity AS quantity,
                                    'علشان اهبل' AS reason
                                FROM
                                    Cus_Returned_Items AS CRI
                                JOIN
                                    Customers AS C ON CRI.customer_id = C.customer_id
                                JOIN
                                    Products AS P ON CRI.product_id = P.product_id ;
                            ''')
        return self.cursor.fetchall()


    def get_customer_names_and_money(self):
        if self.supplier == 'golden rose':
            self.cursor.execute("SELECT name, Golden_Rose_amount_money FROM Customers")
        else:
            self.cursor.execute("SELECT name, Snow_White_amount_money FROM Customers")
        return self.cursor.fetchall()


    def get_products_codes(self):
        self.cursor.execute("SELECT type, 0 FROM Products")
        return self.cursor.fetchall()

