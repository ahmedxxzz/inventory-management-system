class FactoryAccountDetailsModel:
    def __init__(self, db_conn, factory_id):
        self.db_conn = db_conn
        self.cursor = self.db_conn.cursor()
        self.factory_id = factory_id


    def get_factory_name(self):
        self.cursor.execute("SELECT name FROM Factories WHERE factory_id = ?", (self.factory_id,))
        return self.cursor.fetchone()[0]


    def get_factory_data(self):
        self.cursor.execute("SELECT current_balance, current_quantity FROM Factories WHERE factory_id = ?", (self.factory_id,))
        return self.cursor.fetchone()


    def get_factor_transactions(self):
        purchases_transactions = self.cursor.execute("SELECT date, 'فاتورة شراء', total_amount FROM Factory_Purchases_Bills WHERE factory_id = ?", (self.factory_id, )).fetchall()
        pays_transactions = self.cursor.execute("SELECT date, 'دفعة', amount_paid FROM Factory_Pays WHERE factory_id = ?", (self.factory_id, )).fetchall()
        returns_transactions = self.cursor.execute("SELECT date, 'مرتجع', total_amount FROM Factory_Returns WHERE factory_id = ?", (self.factory_id, )).fetchall()
        all_transactions = purchases_transactions + pays_transactions + returns_transactions
        return sorted(all_transactions, key=lambda t: t[0], reverse=True)
