import sqlite3
from datetime import datetime

class ReturnModel:
    def __init__(self):
        self.conn = sqlite3.connect('IMS.db')
        self.cursor = self.conn.cursor()




    def check_factory_name_exist(self, fac_name):
        self.cursor.execute("SELECT name FROM Factories WHERE name = ?", (fac_name,))
        fac  = self.cursor.fetchone()[0]
        if fac:
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
        then reduce the factory money and quantity
        
        '''
        factory_id = self.cursor.execute("SELECT factory_id FROM Factories WHERE name = ?", (data[0],)).fetchone()[0]
        product_id = self.cursor.execute("SELECT product_id FROM Products WHERE type = ?", (data[1],))
        price_per_piece = self.cursor.execute("SELECT fac_price_per_piece FROM Products WHERE type = ?", (data[1],)).fetchone()[0]
        self.cursor.execute('''INSERT INTO Fac_Returned_Items (date, product_id, quantity, reason, price_per_piece,  factory_id)  VALUES (?, ?, ?, ?, ?, ?);''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), product_id, int(data[2]), data[3],  price_per_piece, factory_id))
        self.cursor.execute("UPDATE Products SET current_quantity = current_quantity - ? WHERE product_id = ?", (int(data[2]), product_id))
        self.cursor.execute("UPDATE Factories SET amount_money = amount_money - ? ,current_quantity = current_quantity - ? WHERE factory_id = ?", (float(price_per_piece) * int(data[2]), int(data[2]), factory_id))
        
        self.conn.commit()
        
        return True


    def get_returns_from_db(self):
        
        
        ''' 
        returned data = [ (facname, time, productcode,  quantity, reason), ()]
        '''

        self.cursor.execute(''' 
                            SELECT
                                    F.name AS facname,
                                    FRI.date AS time,
                                    P.type AS productcode,
                                    FRI.quantity AS quantity,
                                    'علشان اهبل' AS reason
                                FROM
                                    Fac_Returned_Items AS FRI
                                JOIN
                                    Factories AS F ON FRI.factory_id = F.factory_id
                                JOIN
                                    Products AS P ON FRI.product_id = P.product_id;
                                    
                            ''')
        return self.cursor.fetchall()


    def get_factory_names_and_money(self):
        self.cursor.execute("SELECT name, amount_money FROM Factories")
        return self.cursor.fetchall()


    def get_products_codes(self):
        self.cursor.execute("SELECT type, 0 FROM Products")
        return self.cursor.fetchall()

