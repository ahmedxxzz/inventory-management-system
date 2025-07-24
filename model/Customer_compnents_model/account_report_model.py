import sqlite3

class AccountReportModel:
    def __init__(self, customer_id, supplier):
        self.conn = sqlite3.connect('IMS.db')
        self.cursor = self.conn.cursor()
        self.customer_id = customer_id
        self.supplier = supplier
        


    def get_customer_data(self):
        if self.supplier== 'golden rose':
            self.cursor.execute("SELECT name, Golden_Rose_amount_money, Golden_Rose_current_quantity FROM Customers WHERE customer_id = ?", (self.customer_id,))
        else:
            self.cursor.execute("SELECT name, Snow_White_amount_money, Snow_White_current_quantity FROM Customers WHERE customer_id = ?", (self.customer_id,))
        return self.cursor.fetchone()



    def get_purchases_data(self):
        self.cursor.execute(
                    '''SELECT SUM(CPI.quantity * (CPI.price_per_piece - CPI.discount_per_piece)) AS net_amount, CP.purchase_date, 'buy'
                    FROM Cus_Purchases CP JOIN Cus_PurchaseItems CPI ON CP.purchase_id = CPI.purchase_id
                    WHERE CP.customer_id = ? AND CP.resource_name = ? GROUP BY CP.purchase_id, CP.purchase_date ORDER BY CP.purchase_date
                    ''', (self.customer_id, self.supplier))
        return self.cursor.fetchall() # returned data = [ (50010, '2022-01-01', 'buy'), (6014, '2022-01-02', 'buy') ]

    def get_payments_data(self):
        return self.cursor.execute('''SELECT amount_money AS net_amount, date, 'pay' FROM Cus_Pays WHERE customer_id = ? AND resource_name = ? ORDER BY date''',(self.customer_id, self.supplier)).fetchall()



    def get_returned_data(self):
        return self.cursor.execute(''' SELECT SUM(quantity * price_per_piece ) AS net_amount, date ,'return' FROM Cus_Returned_Items
                    WHERE customer_id = ? AND resource_name = ? GROUP BY date ORDER BY date''',(self.customer_id, self.supplier)).fetchall()