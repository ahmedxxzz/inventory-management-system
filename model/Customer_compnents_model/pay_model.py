import sqlite3
from sqlite3 import Error
from datetime import datetime

class PayModel:
    def __init__(self, supplier):
        self.conn = sqlite3.connect('IMS.db')
        self.cursor = self.conn.cursor()
        self.supplier = supplier
    
    
    def get_customer_names_and_money(self):
        '''return [('حماده طلبة', 50000.0),('عمرو هلال', 75000.0),('علاء احمد', 30000.0),]'''
        if self.supplier == 'golden rose':
            self.cursor.execute("SELECT name, Golden_Rose_amount_money FROM Customers")
        else:
            self.cursor.execute("SELECT name, Snow_White_amount_money FROM Customers")

        return self.cursor.fetchall()


    def get_all_pays(self):
        self.cursor.execute("SELECT * FROM Cus_Pays where resource_name = ?", (self.supplier,))
        return self.cursor.fetchall()


    def get_pays_from_db(self ):
        self.cursor.execute('''
                            SELECT
                                C.name AS customer_name,
                                CP.date,
                                CP.amount_money,
                                CP.customer_money_before,
                                CP.customer_money_after
                            FROM
                                Cus_Pays AS CP
                            INNER JOIN
                                Customers AS C
                            ON
                                CP.customer_id = C.customer_id;
                            ''')
        
        return self.cursor.fetchall()


    def check_customer_name_exist(self, name):
        self.cursor.execute("SELECT customer_id FROM Customers WHERE name = ?", (name,))
        cus = self.cursor.fetchone()
        if cus == None:
            return False
        return True


    def check_customer_money(self, name):
        if self.supplier == 'golden rose':
            self.cursor.execute("SELECT Golden_Rose_amount_money FROM Customers WHERE name = ?", (name,))
        else:
            self.cursor.execute("SELECT Snow_White_amount_money FROM Customers WHERE name = ?", (name,))
        return self.cursor.fetchone()[0]


    def check_safe_money(self, safe_type):
        self.cursor.execute("SELECT amount_money FROM Safe WHERE type = ?", (safe_type,))
        return self.cursor.fetchone()[0]


    def save_pay_to_db(self, customer_name, amount_money, safe_type):
        try :
            safe_id, safe_money_before = self.cursor.execute("SELECT safe_id, amount_money FROM Safe WHERE type = ?", (safe_type,)).fetchone()
            if self.supplier == 'golden rose':
                cus_id , cus_money_before = self.cursor.execute("SELECT customer_id, Golden_Rose_amount_money FROM Customers WHERE name = ?", (customer_name,)).fetchone()
            else:
                cus_id , cus_money_before = self.cursor.execute("SELECT customer_id, Snow_White_amount_money FROM Customers WHERE name = ?", (customer_name,)).fetchone()
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self.cursor.execute("INSERT INTO Cus_Pays (customer_id, customer_money_before, customer_money_after, date, amount_money, safe_id, resource_name, safe_money_before) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (cus_id, cus_money_before, float(cus_money_before) - float(amount_money) , date, amount_money, safe_id, self.supplier, safe_money_before))        
            if self.supplier == 'golden rose':
                self.cursor.execute("UPDATE Customers SET Golden_Rose_amount_money = Golden_Rose_amount_money - ? WHERE customer_id = ?", (amount_money, cus_id))
            else:
                self.cursor.execute("UPDATE Customers SET Snow_White_amount_money = Snow_White_amount_money - ? WHERE customer_id = ?", (amount_money, cus_id))
                
            self.cursor.execute("UPDATE Safe SET amount_money = amount_money + ? WHERE safe_id = ?", (amount_money, safe_id))

            if self.supplier == 'golden rose':
                self.cursor.execute("DELETE FROM Notifications WHERE type='golden_cus_unpaid' AND entity_id = ?", (cus_id,))
            else:
                self.cursor.execute("DELETE FROM Notifications WHERE type='snow_cus_unpaid' AND entity_id = ?", (cus_id,))
            self.conn.commit()

        except Exception as e:
            print(f"there is a problem in save_pay_to_db : {e}")
            return False

        return True

    def get_safes(self):
        data = self.cursor.execute("SELECT type FROM Safe").fetchall()
        safe_values =[] 
        for i in data:
            safe_values.append(i[0])
        return safe_values