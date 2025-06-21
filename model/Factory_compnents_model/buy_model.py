import sqlite3
from sqlite3 import Error


class BuyModel:
    def __init__(self):
        self.conn = sqlite3.connect('IMS.db')
        self.cursor = self.conn.cursor()
    
        self.data = [
            # [facname, time, productcode, price, quantity, discount, total price]
            ['عمر خالد', '2025-04-21 20:54:29', '1003', 500, 50, 1, 24750.0],
            ['علاء احمد', '2025-04-21 21:54:29', '1001', 500, 210, 1, 103950.0],
            ['علاء احمد', '2025-04-21 22:54:29', '1005', 500, 20, 1, 9900.0],
            ['علاء احمد', '2025-04-21 19:54:29', '1003', 500, 200, 1, 99000.0],
            ['علاء احمد', '2025-04-21 20:52:29', '1003', 500, 40, 1, 19800.0],
            ['علاء احمد', '2025-04-21 20:54:29', '1003', 500, 50, 1, 24750.0],
            ['حمادة عمير', '2025-04-21 21:54:29', '1001', 500, 210, 1, 103950.0],
            ['علاء احمد', '2025-04-21 22:54:29', '1005', 500, 20, 1, 9900.0],
            ['علاء احمد', '2025-04-21 19:54:29', '1003', 500, 200, 1, 99000.0],
            ['علاء احمد', '2025-04-21 20:52:29', '1003', 500, 40, 1, 19800.0],
            ['علاء احمد', '2025-04-21 20:54:29', '1003', 500, 50, 1, 24750.0],
            ['علاء احمد', '2025-04-21 21:54:29', '1001', 500, 210, 1, 103950.0],
            ['علاء احمد', '2025-04-21 22:54:29', '1005', 500, 20, 1, 9900.0],
            ['علاء احمد', '2025-04-21 19:54:29', '1003', 500, 200, 1, 99000.0],
            ['علاء احمد', '2025-04-21 20:52:29', '1003', 500, 40, 1, 19800.0]
        ]
    
    def get_factory_names_and_money(self):
        '''return [('حماده طلبة', 50000.0),('عمرو هلال', 75000.0),('علاء احمد', 30000.0),]'''        
        self.cursor.execute("SELECT name, amount_money FROM Factories")
        
        # return self.cursor.fetchall()
        return [('حماده طلبة', 50000.0),('عمرو هلال', 75000.0),('علاء احمد', 30000.0),]

    def get_products_codes(self):
        self.cursor.execute("SELECT type FROM Products")
        # [1001, 1002, 1003,]
        
        # return [(row[0],0) for row in self.cursor.fetchall()]
    
        return [(row,0) for row in range(1001, 1020)]

    def insert_buys_to_db(self, buys):
        for buy in buys:
            self.data.append(buy)
        print(f"this is buys added: \n{buys}")
        return True


    def get_buys_from_db(self ):
        # print(self.data[-1])
        self.data[-1][-1] = (float(self.data[-1][3]) - float(self.data[-1][5] )) * int(self.data[-1][4])
        # print(self.data[-1])
        
        
        
        return self.data