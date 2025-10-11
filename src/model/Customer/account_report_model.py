
class AccountReportModel:
    def __init__(self, customer_id, distributor, db_conn):
        self.conn = db_conn
        self.cursor = self.conn.cursor()
        self.customer_id = customer_id
        self.distributor_id = self.get_distributor_id(distributor)


    def get_distributor_id(self, distributor_name):
        self.cursor.execute("SELECT distributor_id FROM Distributor WHERE name = ?", (distributor_name,))
        return self.cursor.fetchone()[0]


    def get_customer_data(self):
        self.cursor.execute("""SELECT
                                    C.name AS customer_name,
                                    CDA.current_balance ,
                                    CDA.current_quantity
                                FROM
                                    Customer_Distributor_Accounts AS CDA
                                JOIN
                                    Customer AS C
                                    ON CDA.customer_id = C.customer_id
                                JOIN
                                    Distributor AS D
                                    ON CDA.distributor_id = D.distributor_id
                                WHERE
                                    CDA.customer_id = ? AND CDA.distributor_id = ?
                            """, (self.customer_id,self.distributor_id))
        return self.cursor.fetchone()


    def get_purchases_data(self):
        self.cursor.execute(
                    '''SELECT 
                            SUM(CSI.quantity * (CSI.price_per_item - CSI.discount_per_item)) AS net_amount, 
                            CS.date, 
                            'buy'
                        FROM 
                            Customer_Sales_Bills CS 
                        JOIN 
                            Customer_Sales_Bill_Items CSI 
                            ON CS.sales_bill_id = CSI.sales_bill_id
                        WHERE 
                            CS.customer_id = ? AND CS.distributor_id = ? 
                        GROUP BY 
                            CS.sales_bill_id, CS.date 
                        ORDER BY 
                            CS.date
                    ''', (self.customer_id, self.distributor_id))
        return self.cursor.fetchall() # returned data = [ (50010, '2022-01-01', 'buy'), (6014, '2022-01-02', 'buy') ]


    def get_paid_purchases_data(self):
        self.cursor.execute(
            '''SELECT 
                    SUM(CS.total_amount)
                FROM 
                    Customer_Sales_Bills CS 
                WHERE 
                    CS.customer_id = ? 
                    AND CS.distributor_id = ? 
                    AND CS.is_paid = 1
            ''', (self.customer_id, self.distributor_id))
            
        result = self.cursor.fetchone()
        
        if result and result[0] is not None:
            return result[0]
        else:
            return 0.00


    def get_payments_data(self):
        return self.cursor.execute('''SELECT 
                                        amount_paid AS net_amount, 
                                        date, 
                                        'pay'
                                    FROM 
                                        Customer_Pays 
                                    WHERE 
                                        customer_id = ? AND distributor_id = ? 
                                    ORDER BY 
                                        date
                                    ''',(self.customer_id, self.distributor_id)).fetchall()


    def get_returned_data(self):
        return self.cursor.execute('''SELECT 
                                        SUM(CRI.quantity * CRI.price_at_return ) AS net_amount, 
                                        CR.date , 
                                        'return' 
                                    FROM 
                                        Customer_Return_Items CRI
                                    JOIN 
                                        Customer_Returns CR 
                                        ON CRI.return_id = CR.return_id
                                    WHERE 
                                        CR.customer_id = ? AND CR.distributor_id = ? 
                                    GROUP BY 
                                        CR.date 
                                    ORDER 
                                        BY CR.date
                                        ''',(self.customer_id, self.distributor_id)).fetchall()

