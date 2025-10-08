class FactoryAccountModel:
    def __init__(self, db_conn):
        self.conn = db_conn
        self.cursor = self.conn.cursor()


    def get_factories_accounts(self):
        self.cursor.execute("SELECT name, current_balance, current_quantity FROM Factories")
        return self.cursor.fetchall()


    def search_factories_accounts(self, name=None):
        if name:
            return self.cursor.execute("SELECT name, current_balance, current_quantity FROM Factories WHERE name LIKE ?", ('%' + name + '%',)).fetchall()
        return self.cursor.execute("SELECT name, current_balance, current_quantity FROM Factories").fetchall()


    def factory_exists(self, factory_name):
        self.cursor.execute("SELECT name FROM Factories WHERE name = ?", (factory_name,))
        return self.cursor.fetchone() is not None


    def add_factory_account(self, factory_name, factory_amount_money, factory_product_quantity):
        try:
            self.cursor.execute("INSERT INTO Factories (name, current_balance, current_quantity) VALUES (?, ?, ?)", (factory_name, factory_amount_money, factory_product_quantity))
            self.conn.commit()
            return True, None
        
        except Exception as e:
            try:
                self.conn.rollback()
            except Exception as e:
                return False, e
            return False, e


    def get_factory_id(self, factory_name):
        self.cursor.execute("SELECT factory_id FROM Factories WHERE name = ?", (factory_name,))
        return self.cursor.fetchone()[0]