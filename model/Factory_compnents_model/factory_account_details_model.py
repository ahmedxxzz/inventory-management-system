import sqlite3



class FactoryAccountDetailsModel:
    def __init__(self, factory_name):
        self.conn = sqlite3.connect('IMS.db')
        self.cursor = self.conn.cursor()
        self.factory_name = factory_name

    
    
    
    def get_factory_account_details(self):
        fac_id = self.get_fac_id_by_name(self.factory_name)
        
        self.cursor.execute(f"SELECT '{self.factory_name}', purchas_date, cost_money, 'شراء' FROM Fac_Purchases WHERE factory_id = ?", (fac_id,))
        buys = self.cursor.fetchall() # [(factory_name, purchas_date, cost_money, 'شراء'), ...]
        
        self.cursor.execute(f"SELECT '{self.factory_name}', date, amount_money, 'دفع' FROM Fac_Pays WHERE factory_id = ?", (fac_id,))
        pays = self.cursor.fetchall() # [(factory_name, purchas_date, cost_money, 'شراء'), ...]
        
        self.cursor.execute(f"SELECT '{self.factory_name}', date, quantity * price_per_piece , 'مرتجع' FROM Fac_Returned_Items WHERE factory_id = ?", (fac_id,))
        returns = self.cursor.fetchall() # [(factory_name, purchas_date, cost_money, 'شراء'), ...]
        return buys + pays + returns


    def get_fac_id_by_name(self, name):
        self.cursor.execute("SELECT factory_id FROM Factories WHERE name = ?", (name,))
        return self.cursor.fetchone()[0]


    def get_factory_data(self):
        self.cursor.execute("SELECT amount_money, current_quantity FROM Factories WHERE name = ?", (self.factory_name,))
        return self.cursor.fetchone()