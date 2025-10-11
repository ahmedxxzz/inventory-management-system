
class AccountReportModel:
    def __init__(self, factory_id, db_conn = None):
        self.factory_id = factory_id
        self.conn = db_conn
        self.cursor = self.conn.cursor()


    def get_factory_data(self):
        query = "SELECT name, current_balance, current_quantity FROM Factories WHERE factory_id = ?"
        self.cursor.execute(query, (self.factory_id,))
        return self.cursor.fetchone()


    def get_purchases_data(self):
        return self.cursor.execute(
                    '''SELECT 
                        SUM(FPI.quantity * (FPI.price_per_item - FPI.discount_per_item)) AS net_amount,
                        FP.date,
                        'buy'
                    FROM 
                        Factory_Purchases_Bills FP 
                    JOIN 
                        Factory_Purchases_Bill_Items FPI 
                        ON FP.purchases_bill_id = FPI.purchases_bill_id
                    WHERE 
                        FP.factory_id = ? 
                    GROUP BY 
                        FP.purchases_bill_id, FP.date 
                    ORDER BY 
                        FP.date
                    ''', (self.factory_id,)).fetchall()



    def get_paid_purchases_data(self):
        self.cursor.execute(
                    '''SELECT 
                        SUM(FP.total_amount)
                    FROM 
                        Factory_Purchases_Bills FP 
                    WHERE 
                        FP.factory_id = ? AND FP.is_paid = 1
                    ''', (self.factory_id,))
        result = self.cursor.fetchone()

        if result and result[0] is not None:
            return result[0]
        else:
            return 0.00


    def get_payments_data(self):
        return self.cursor.execute('''SELECT amount_paid, date, 'pay' AS net_amount FROM Factory_Pays WHERE factory_id = ? ORDER BY date''',(self.factory_id,)).fetchall()


    def get_returned_data(self):
        return self.cursor.execute('''SELECT SUM(T1.quantity * T1.price_at_return) AS net_amount, T2.date, 'return' AS transaction_type 
                                        FROM 
                                            Factory_Return_Items AS T1
                                        JOIN 
                                            Factory_Returns AS T2 
                                            ON T1.return_id = T2.return_id
                                        WHERE 
                                            T2.factory_id = ? 
                                        GROUP BY 
                                            T2.date
                                        ORDER BY 
                                            T2.date ;''',(self.factory_id,)).fetchall()

