import sqlite3
from sqlite3 import Error
from datetime import datetime

class PayModel:
    def __init__(self):
        self.conn = sqlite3.connect('IMS.db')
        self.cursor = self.conn.cursor()
    
    
    def get_factory_names_and_money(self):
        '''return [('حماده طلبة', 50000.0),('عمرو هلال', 75000.0),('علاء احمد', 30000.0),]'''        
        self.cursor.execute("SELECT name, amount_money FROM Factories")
        
        return self.cursor.fetchall()
    
    
    def get_all_pays(self):
        self.cursor.execute("SELECT * FROM Fac_Pays")
        return self.cursor.fetchall()


    def get_factory_name_byid(self, id):
        self.cursor.execute("SELECT name FROM Factories WHERE factory_id = ?", (id,))
        return self.cursor.fetchone()[0]


    def get_pays_from_db(self ):
        date = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute("SELECT * FROM Fac_Pays")
        pays_data = self.cursor.fetchall() # [(pay_id, date, amount_money, factory_id, fac_money_before, safe_id), ...]
        
        final_data = []
        for row in pays_data:
            final_data.append([ self.get_factory_name_byid(row[3]), date, float(row[2]), float(row[4]), float(row[4] - float(row[2]))])
        
        '''
        returned data = [ [factory_name, date, amount_money, fac_money_before, fac_money_after] ]
        '''
        
        return final_data

    
    def check_factory_name_exist(self, name):
        self.cursor.execute("SELECT * FROM Factories WHERE name = ?", (name,))
        fac = self.cursor.fetchone()
        if fac == None:
            return False
        return True


    def check_factory_money(self, name):
        self.cursor.execute("SELECT amount_money FROM Factories WHERE name = ?", (name,))
        return self.cursor.fetchone()[0]


    def check_safe_money(self, safe_type):
        self.cursor.execute("SELECT amount_money FROM Safe WHERE type = ?", (safe_type,))
        return self.cursor.fetchone()[0]


    def save_pay_to_db(self, factory_name, amount_money, safe_type):
        try :
            safe_id = self.cursor.execute("SELECT safe_id FROM Safe WHERE type = ?", (safe_type,)).fetchone()[0]
            fac_id , fac_money_before = self.cursor.execute("SELECT factory_id, amount_money FROM Factories WHERE name = ?", (factory_name,)).fetchone()
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            self.cursor.execute("INSERT INTO Fac_Pays (factory_id, fac_money_before, date, amount_money, safe_id) VALUES (?, ?, ?, ?, ?)", (fac_id, fac_money_before, date, amount_money, safe_id))        

            self.cursor.execute("UPDATE Factories SET amount_money = amount_money - ? WHERE factory_id = ?", (amount_money, fac_id))
            self.cursor.execute("UPDATE Safe SET amount_money = amount_money - ? WHERE safe_id = ?", (amount_money, safe_id))
            self.conn.commit()
        
        except Exception as e:
            print(f"there is a problem in save_pay_to_db : {e}")
            return False
        return True