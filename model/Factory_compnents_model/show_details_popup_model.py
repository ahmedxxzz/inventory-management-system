import sqlite3


class ShowDetailsPopupModel:
    def __init__(self, operation_id):
        self.operation_id = operation_id
        self.conn = sqlite3.connect('IMS.db')
        self.cursor = self.conn.cursor()
        
        
    
    
    def get_buy_details(self):
        self.cursor.execute(
            f'''Select
                P.type as product_code,
                FP.price_per_piece ,
                FP.quantity ,
                FP.discount_per_piece ,
                FP.quantity * (FP.price_per_piece - FP.discount_per_piece) as total_price,
                CASE
                    WHEN FP.paid = 0 THEN 'لاء'
                    ELSE 'نعم'
                END AS paid
                FROM Fac_PurchaseItems AS FP
                Join Products AS P
                ON FP.product_id = P.product_id
                WHERE FP.purchase_id = ?;
                
                ''', (self.operation_id,))
        
        return self.cursor.fetchall()
    
    def get_pay_details(self):
        self.cursor.execute("SELECT amount_money, fac_money_before FROM Fac_Pays WHERE pay_id = ?", (self.operation_id,))
        
        
        return self.cursor.fetchall()
    
    
    def get_return_details(self):
        self.cursor.execute(
                f'''Select
                    P.type as product_code,
                    FR.quantity ,
                    FR.price_per_piece ,
                    FR.quantity * FR.price_per_piece as total_price,
                    FR.reason 
                    FROM Fac_Returned_Items AS FR
                    Join Products AS P
                    ON FR.product_id = P.product_id
                    WHERE FR.returned_process_id = ?;
                    
                    ''', (self.operation_id,))
        return self.cursor.fetchall()


