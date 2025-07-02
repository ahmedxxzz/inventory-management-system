import sqlite3



class SafeModel:
    def __init__(self):
        self.conn = sqlite3.connect('IMS.db')
        self.cursor = self.conn.cursor()
        
    
    def get_safes_info(self, name=None):
        if name:
            return self.cursor.execute("SELECT safe_id, type, amount_money FROM Safe WHERE type LIKE ?", ('%' + name + '%',)).fetchall()
        
        
        return self.cursor.execute("SELECT safe_id, type, amount_money FROM Safe").fetchall()


    def check_safe_name_exist(self, name):
        self.cursor.execute("SELECT type FROM Safe ",)
        names = self.cursor.fetchall()
        for n in names:
            if n[0] == name:
                return True
        return False


    def adding_new_safe(self, type, amount_money):
        self.cursor.execute("INSERT INTO Safe (type, amount_money) VALUES (?, ?)", (type, amount_money))
        self.conn.commit()
        return True


    def delete_safe(self, safe_name):
        self.cursor.execute("DELETE FROM Safe WHERE type = ?", (safe_name,))
        self.conn.commit()
        return True

    def update_safe(self, type, amount_money):
        self.cursor.execute("UPDATE Safe SET amount_money = ? WHERE type = ?", (amount_money, type))
        self.conn.commit()
        return True