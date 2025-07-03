import sqlite3


class CustomerAccountModel:
    def __init__(self, supplier):
        self.conn = sqlite3.connect('IMS.db')
        self.cursor = self.conn.cursor()
        self.supplier = supplier


    def get_customers_data(self, name=None):
        '''
        returned data = [ ('حماده طلبة', 50000.0, 5), ('عمرو هلال', 75000.0, 20), ('علاء احمد', 30000.0, 0), ]
        '''
        if name:
            if self.supplier == 'golden rose':
                return self.cursor.execute("SELECT name, Golden_Rose_amount_money, Golden_Rose_current_quantity FROM Customers WHERE name LIKE ?", ('%' + name + '%',)).fetchall()
            else:
                return self.cursor.execute("SELECT name, Snow_White_amount_money, Snow_White_current_quantity FROM Customers WHERE name LIKE ?", ('%' + name + '%',)).fetchall()
        else:
            if self.supplier == 'golden rose':
                return self.cursor.execute("SELECT name, Golden_Rose_amount_money, Golden_Rose_current_quantity FROM Customers" ).fetchall()
            else:
                return self.cursor.execute("SELECT name, Snow_White_amount_money, Snow_White_current_quantity FROM Customers" ).fetchall()


    def zeros_customer_account(self, name):
        if self.supplier == 'golden rose':
            self.cursor.execute("UPDATE Customers SET Golden_Rose_amount_money = 0, Golden_Rose_current_quantity = 0 WHERE name = ?", (name,))
        else:
            self.cursor.execute("UPDATE Customers SET Snow_White_amount_money = 0, Snow_White_current_quantity = 0 WHERE name = ?", (name,))
        self.conn.commit()


    def adding_new_cus(self, name, amount_money, current_quantity):
        if self.supplier == 'golden rose':
            self.cursor.execute("INSERT INTO Customers (name, Golden_Rose_amount_money, Golden_Rose_current_quantity) VALUES (?, ?, ?)", (name, amount_money, current_quantity))
        else:
            self.cursor.execute("INSERT INTO Customers (name, Snow_White_amount_money, Snow_White_current_quantity) VALUES (?, ?, ?)", (name, amount_money, current_quantity))
        self.conn.commit()


    def check_customer_name_exist(self, name):
        self.cursor.execute("SELECT name FROM Customers ",)
        names = self.cursor.fetchall()
        for n in names:
            if n[0] == name:
                return True
        return False

