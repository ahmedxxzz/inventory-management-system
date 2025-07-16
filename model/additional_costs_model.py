import sqlite3
from datetime import datetime

class AdditionalCostsModel:
    def __init__(self):
        self.conn = sqlite3.connect('IMS.db')
        self.cursor = self.conn.cursor()


    def get_Adds(self):
        return self.cursor.execute("SELECT AC.type, AC.date, AC.amount_of_money,SF.type  FROM Additional_Costs as AC INNER JOIN Safe AS SF ON AC.safe_id = SF.safe_id").fetchall()


    def get_safes(self):
        data = self.cursor.execute("SELECT type FROM Safe").fetchall()
        safe_values =[] 
        for i in data:
            safe_values.append(i[0])
        return safe_values


    def get_safe_id_from_name(self, name):
        self.cursor.execute("SELECT safe_id FROM Safe WHERE type = ?", (name,))
        return self.cursor.fetchone()[0]


    def save_adds(self, adds_type, price,  safe):
        try :
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute("INSERT INTO Additional_Costs (type, date, amount_of_money,  safe_id) VALUES (?, ?, ?, ?);", (adds_type,  date, price, self.get_safe_id_from_name(safe))) 
            self.conn.commit()
        except Exception as e:
            print(f"there is a problem in save_product : {e}")
            return False
        return True
    
    


    # def get_safe_name_from_id(self, id):
    #     self.cursor.execute("SELECT name FROM Safe WHERE safe_id = ?", (id,))
    #     return self.cursor.fetchone()[0]

