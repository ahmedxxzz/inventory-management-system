class ShowDetailsPopupModel:
    def __init__(self, operation_id, db_conn):
        self.operation_id = operation_id
        self.conn = db_conn
        self.cursor = self.conn.cursor()
        
        
    
    
    def get_buy_details(self):
        self.cursor.execute(
            f'''Select
                P.name as product_code,
                FPI.price_per_item ,
                FPI.quantity ,
                FPI.discount_per_item ,
                FPI.quantity * (FPI.price_per_item  - FPI.discount_per_item) as total_price,
                CASE
                    WHEN FP.is_paid  = 0 THEN 'لاء'
                    ELSE 'نعم'
                END AS paid
                FROM 
                    Factory_Purchases_Bill_Items AS FPI
                JOIN
                    Factory_Purchases_Bills AS FP
                    ON FPI.purchases_bill_id = FP.purchases_bill_id
                JOIN 
                    Product AS P
                    ON FPI.product_id = P.product_id
                WHERE 
                    FPI.purchases_bill_id  = ?;
                
                ''', (self.operation_id,))
        
        return self.cursor.fetchall()
    
    def get_pay_details(self):
        self.cursor.execute("SELECT amount_paid, balance_before FROM Factory_Pays WHERE pay_id = ?", (self.operation_id,))
        
        return self.cursor.fetchall()
    
    
    def get_return_details(self):
        self.cursor.execute(
                f'''Select
                        P.name as product_code,
                        FRI.quantity ,
                        FRI.price_at_return ,
                        FRI.quantity  * FRI.price_at_return as total_price,
                        FR.reason 
                    FROM 
                        Factory_Return_Items  AS FRI
                    Join 
                        Product AS P
                        ON FRI.product_id = P.product_id
                    Join 
                        Factory_Returns AS FR
                        ON FRI.return_id = FR.return_id
                    WHERE 
                        FRI.return_id  = ?;
                    
                    ''', (self.operation_id,))
        return self.cursor.fetchall()


