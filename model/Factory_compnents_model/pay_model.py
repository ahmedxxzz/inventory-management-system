import sqlite3
from sqlite3 import Error

class PayModel:
    def __init__(self):
        self.conn = sqlite3.connect('IMS.db')
        self.cursor = self.conn.cursor()
        self.data = [
            # [facname, time, productcode, price, quantity, discount, total price]
            ['عمر خالد', '2025-04-21 20:54:29', '5000', 20000, 15000],
            ['علاء احمد', '2025-04-21 21:54:29', '400', 50000, 49600,],
            ['علاء احمد', '2025-04-21 22:54:29', '250', 60000, 20,],
            ['علاء احمد', '2025-04-21 19:54:29', '1000', 25000, 200,],
            ['علاء احمد', '2025-04-21 20:52:29', '4000', 62000, 61600,],
        ]
    
    
    def get_factory_names_and_money(self):
        '''return [('حماده طلبة', 50000.0),('عمرو هلال', 75000.0),('علاء احمد', 30000.0),]'''        
        self.cursor.execute("SELECT name, amount_money FROM Factories")
        
        # return self.cursor.fetchall()
        return [('حماده طلبة', 50000.0),('عمرو هلال', 75000.0),('علاء احمد', 30000.0),]
    
    
    def get_all_pays(self):
        self.cursor.execute("SELECT * FROM Fac_Pays")
        return self.cursor.fetchall()


    def get_pays_from_db(self ):
        # print(self.data[-1])
        # self.data[-1][-1] = (float(self.data[-1][3]) - float(self.data[-1][5] )) * int(self.data[-1][4])
        # print(self.data[-1])
        
        
        
        return self.data
    
    def check_factory_name_exist(self, name):
        self.cursor.execute("SELECT * FROM Factories WHERE name = ?", (name,))
        # return self.cursor.fetchone()
        return True

    def check_factory_money(self, name):
        self.cursor.execute("SELECT amount_money FROM Factories WHERE name = ?", (name,))
        # return self.cursor.fetchone()
        return 5000




    def get_safe_money(self, safe_type):
        if safe_type == 'cash':
            return 100000
        elif safe_type == 'vodafone cash':
            return 1000
    
    
    def save_pay_to_db(self, fac_name, money_amount, safe_type):
        
        return True