class ShowDetailsPopupModel:
    def __init__(self, operation_id, db_conn):
        self.operation_id = operation_id
        self.conn = db_conn
        self.cursor = self.conn.cursor()
        
        
    
    
    def get_buy_details(self):
        self.cursor.execute(
            f'''Select
                P.name as product_code,
                CSI.price_per_item ,
                CSI.quantity ,
                CSI.discount_per_item ,
                CSI.quantity * (CSI.price_per_item  - CSI.discount_per_item) as total_price,
                CASE
                    WHEN CS.is_paid  = 0 THEN 'لاء'
                    ELSE 'نعم'
                END AS paid
                FROM 
                    Customer_Sales_Bill_Items AS CSI
                JOIN
                    Customer_Sales_Bills AS CS
                    ON CSI.sales_bill_id = CS.sales_bill_id
                JOIN 
                    Product AS P
                    ON CSI.product_id = P.product_id
                WHERE 
                    CS.sales_bill_id= ?;
                
                ''', (self.operation_id,))
        
        return self.cursor.fetchall()
    
    def get_pay_details(self):
        self.cursor.execute("SELECT amount_paid, balance_before FROM Customer_Pays WHERE pay_id = ?", (self.operation_id,))
        
        return self.cursor.fetchall()
    
    
    def get_return_details(self):
        self.cursor.execute(
                f'''Select
                        P.name as product_code,
                        CRI.quantity ,
                        CRI.price_at_return ,
                        CRI.quantity  * CRI.price_at_return as total_price,
                        CRI.reason
                    FROM 
                        Customer_Return_Items  AS CRI
                    Join 
                        Product AS P
                        ON CRI.product_id = P.product_id
                    WHERE 
                        CRI.return_id  = ?;
                    
                    ''', (self.operation_id,))
        return self.cursor.fetchall()


