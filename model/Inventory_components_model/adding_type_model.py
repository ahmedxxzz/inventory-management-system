import sqlite3


class AddingTypeModel:
    def __init__(self):
        self.conn = sqlite3.connect('IMS.db')
        self.cursor = self.conn.cursor()


    def get_products_info(self):
        return self.cursor.execute("SELECT type, current_quantity, cus_price_per_piece, resource_name  FROM Products").fetchall()


    def save_product(self, product_code, cus_price, supplier):
        try :
            self.cursor.execute("INSERT INTO Products (type, cus_price_per_piece, resource_name) VALUES (?, ?, ?);", (product_code,  cus_price, supplier))
            self.conn.commit()
        except Exception as e:
            print(f"there is a problem in save_product : {e}")
            return False
        return True


    def check_product_code_exist(self, product_code):
        self.cursor.execute("SELECT type FROM Products WHERE type = ?", (product_code,))
        if self.cursor.fetchone():
            return True
        return False


    def edit_product(self, product_code, price, supplier):
        try :
            self.cursor.execute("UPDATE Products SET cus_price_per_piece = ?, resource_name = ? WHERE type = ?", (price, supplier, product_code, ))
            self.conn.commit()
        except Exception as e:
            print(f"there is a problem in save_product : {e}")
            return False
        return True