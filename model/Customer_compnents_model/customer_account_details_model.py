import sqlite3



class CustomerAccountDetailsModel:
    def __init__(self, customer_name, supplier):
        self.conn = sqlite3.connect('IMS.db')
        self.cursor = self.conn.cursor()
        self.customer_name = customer_name
        self.supplier = supplier

    
    
    
    def get_customer_account_details(self):
        cus_id = self.get_cus_id_by_name(self.customer_name)
        
        self.cursor.execute(f"SELECT purchase_id, purchase_date, cost_money, 'شراء' FROM Cus_Purchases WHERE customer_id = ? AND resource_name=?", (cus_id, self.supplier))
        buys = self.cursor.fetchall()
        
        self.cursor.execute(f"SELECT pay_id, date, amount_money, 'دفع' FROM Cus_Pays WHERE customer_id = ? AND resource_name=?", (cus_id, self.supplier))
        pays = self.cursor.fetchall() 
        
        self.cursor.execute(f"SELECT returned_process_id, date, quantity * price_per_piece , 'مرتجع' FROM Cus_Returned_Items WHERE customer_id = ? AND resource_name=?", (cus_id, self.supplier))
        returns = self.cursor.fetchall() 
        return buys + pays + returns


    def get_cus_id_by_name(self, name):
        self.cursor.execute("SELECT customer_id FROM Customers WHERE name = ?", (name,))
        return self.cursor.fetchone()[0]


    def get_customer_data(self):
        if self.supplier == 'golden rose':
            self.cursor.execute("SELECT Golden_Rose_amount_money, Golden_Rose_current_quantity FROM Customers WHERE name = ?", (self.customer_name,))
        else:
            self.cursor.execute("SELECT Snow_White_amount_money, Snow_White_current_quantity FROM Customers WHERE name = ?", (self.customer_name,)) 
        return self.cursor.fetchone()