import sqlite3

class ReportModel:
    def __init__(self, factory_id=None):
        self.conn = sqlite3.connect('IMS.db')
        self.cursor = self.conn.cursor()
        self.factory_id = factory_id


    def get_factory_data(self):
        query = "SELECT name, amount_money, current_quantity FROM Factories WHERE factory_id = ?"
        self.cursor.execute(query, (self.factory_id,))
        return self.cursor.fetchone()


    def get_purchases_data(self):
        self.cursor.execute(
                    '''SELECT SUM(FPI.quantity * (FPI.price_per_piece - FPI.discount_per_piece)) AS net_amount, FP.purchas_date, 'buy'
                    FROM Fac_Purchases FP JOIN Fac_PurchaseItems FPI ON FP.purchase_id = FPI.purchase_id
                    WHERE FP.factory_id = ? GROUP BY FP.purchase_id, FP.purchas_date ORDER BY FP.purchas_date
                    ''', (self.factory_id,))
        return self.cursor.fetchall() # returned data = [ (50010, '2022-01-01', 'buy'), (6014, '2022-01-02', 'buy') ]

    def get_payments_data(self):
        return self.cursor.execute('''SELECT amount_money, date, 'pay' AS net_amount FROM Fac_Pays WHERE factory_id = ? ORDER BY date''',(self.factory_id,)).fetchall()


    def get_returned_data(self):
        return self.cursor.execute('''SELECT SUM(quantity * price_per_piece) AS net_amount, date, 'return' FROM Fac_Returned_Items WHERE factory_id = ? GROUP BY date ORDER BY date''',(self.factory_id,)).fetchall()