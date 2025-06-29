import sqlite3


class FactoryAccountModel:
    def __init__(self):
        self.conn = sqlite3.connect('IMS.db')
        self.cursor = self.conn.cursor()
    
    def get_factories_data(self, name=None):
        '''
        returned data = [ ('حماده طلبة', 50000.0, 5), ('عمرو هلال', 75000.0, 20), ('علاء احمد', 30000.0, 0), ]
        '''
        if name:
            return self.cursor.execute("SELECT name, amount_money, current_quantity FROM Factories WHERE name LIKE ?", ('%' + name + '%',)).fetchall()
        return self.cursor.execute("SELECT name, amount_money, current_quantity FROM Factories").fetchall()


    def zeros_factory_account(self, name):
        self.cursor.execute("UPDATE Factories SET amount_money = 0, current_quantity = 0 WHERE name = ?", (name,))
        self.conn.commit()


    def adding_new_fac(self, name, amount_money, current_quantity):
        self.cursor.execute("INSERT INTO Factories (name, amount_money, current_quantity) VALUES (?, ?, ?)", (name, amount_money, current_quantity))
        self.conn.commit()


    def check_factory_name_exist(self, name):
        self.cursor.execute("SELECT name FROM Factories ",)
        names = self.cursor.fetchall()
        for n in names:
            if n[0] == name:
                return True
        return False


