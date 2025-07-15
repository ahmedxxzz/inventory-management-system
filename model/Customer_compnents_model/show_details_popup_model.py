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
                CP.price_per_piece ,
                CP.quantity ,
                CP.discount_per_piece ,
                CP.quantity * (CP.price_per_piece - CP.discount_per_piece) as total_price,
                CASE
                    WHEN CP.paid = 0 THEN 'لاء'
                    ELSE 'نعم'
                END AS paid
                FROM Cus_PurchaseItems AS CP
                Join Products AS P
                ON CP.product_id = P.product_id
                WHERE CP.purchase_id = ?;
                ''', (self.operation_id,))
        
        return self.cursor.fetchall()
    
    def get_pay_details(self):
        self.cursor.execute("SELECT amount_money, customer_money_before FROM Cus_Pays WHERE pay_id = ?", (self.operation_id,))
        return self.cursor.fetchall()
    
    
    def get_return_details(self):
        self.cursor.execute(
                f'''Select
                    P.type as product_code,
                    CR.quantity ,
                    CR.price_per_piece ,
                    CR.quantity * CR.price_per_piece as total_price,
                    CR.reason 
                    FROM Cus_Returned_Items AS CR
                    Join Products AS P
                    ON CR.product_id = P.product_id
                    WHERE CR.returned_process_id = ?;
                    ''', (self.operation_id,))
        return self.cursor.fetchall()


