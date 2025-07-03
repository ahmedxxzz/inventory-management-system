import sqlite3
from sqlite3 import Error
from datetime import datetime


class BuyModel:
    def __init__(self):
        self.conn = sqlite3.connect('IMS.db')
        self.cursor = self.conn.cursor()



    def get_customer_names_and_money(self, supplier):
        self.cursor.execute(f"SELECT name, {'Golden_Rose_amount_money' if supplier == 'golden rose' else 'Snow_White_amount_money'}  FROM Customers")
        '''
        returned data = [('احمد', 550), ('محمد', 500)]
        '''
        return self.cursor.fetchall()


    def get_products_codes(self):
        self.cursor.execute("SELECT type, 0 FROM Products")
        '''
        returned data = [ ('1001', 0), ('1002', 0), ('1003', 0), ]
        '''
        return self.cursor.fetchall()


    def get_buys_from_db(self, supplier):

        '''
        data returned example :
        [ [cusname, time, productcode, price, quantity, discount, total price, paid or not], ]
        
        '''
        self.cursor.execute(
            '''
            SELECT
            C.name,
            CP.purchase_date,
            P.type,
            CPI.price_per_piece ,
            CPI.quantity,
            CPI.discount_per_piece,
            (CPI.price_per_piece - CPI.discount_per_piece) * CPI.quantity AS total_price,
            CASE
                WHEN CPI.paid = 1 THEN 'نعم'
                ELSE 'لا'
                END AS paid_status
            FROM Customers AS C
            JOIN Cus_Purchases AS CP
            ON C.customer_id = CP.customer_id
            JOIN Cus_PurchaseItems AS CPI
            ON CP.purchase_id = CPI.purchase_id
            JOIN Products AS P
            ON CPI.product_id = P.product_id
            where CP.resource_name = ?;
            ''', (supplier,)
        )

        return self.cursor.fetchall()


    def get_cus_id_from_name(self, name):
        self.cursor.execute("SELECT customer_id FROM Customers WHERE name = ?", (name,))
        return self.cursor.fetchone()[0]


    def get_product_id_from_code(self, code):
        self.cursor.execute("SELECT product_id FROM Products WHERE type = ?", (code,))
        return self.cursor.fetchone()[0]


    def get_cus_money_by_id(self, id, supplier):
        self.cursor.execute(f"SELECT {'Golden_Rose_amount_money' if supplier == 'golden rose' else 'Snow_White_amount_money'} FROM Customers WHERE customer_id = ?", (id,))
        data = self.cursor.fetchone()
        if data :
            return data[0]
        else :
            return 0


    def insert_buys_to_db(self, buys, supplier):
        '''
        buys = [
            [cusname, productcode, price, quantity, discount, supplier, paid or not],
            [cusname, productcode, price, quantity, discount, supplier, paid or not],
        ]
        '''
        
        
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for buy in buys:
            buy[0] = self.get_cus_id_from_name(buy[0])
            buy[1] = self.get_product_id_from_code(buy[1])
            buy[6] = 0 if buy[6] == 'لا' else 1
        buys.sort(key=lambda x: x[0])
        
        
        def group_by_customer(buys):
            cus_grouped_lists = []
            current_group = [buys[0]] 
            for i in range(1, len(buys)):
                if buys[i][0] == current_group[0][0]:
                    current_group.append(buys[i])
                else:
                    
                    cus_grouped_lists.append(current_group)
                    current_group = [buys[i]]
            cus_grouped_lists.append(current_group) 
            return cus_grouped_lists
        
        buys = group_by_customer(buys)
        '''
        now buys = [
            # [ list of buys of the same customer ]
             [[cus id, productcode id, price, quantity, discount, supplier, paid or not],[cusname, productcode, price, quantity, discount, supplier, paid or not],],
             [[cus id, productcode id, price, quantity, discount, supplier, paid or not],[cusname, productcode, price, quantity, discount, supplier, paid or not],]
             ]
        '''
        total_discounts = []
        
        for buy in buys:
            totaldiscount = 0
            for item in buy:
                totaldiscount+= item[4]
            total_discounts.append(totaldiscount)
            
        try :
            for buy in buys:
                self.cursor.execute('''
                    INSERT INTO Cus_Purchases (
                        customer_id,
                        purchase_date,
                        cus_money_before,
                        discount_Total,
                        resource_name
                        )
                        VALUES (?, ?, ?, ?, ?);
                    ''',
                    (buy[0][0], date, self.get_cus_money_by_id(buy[0][0]), total_discounts[buys.index(buy)], supplier)
                )
                purchase_id = self.cursor.lastrowid
                
                
                total_price = 0
                total_quantity = 0
                for purchase in buy:
                    purchase = tuple(purchase)
                    self.cursor.execute(
                        '''
                        INSERT INTO Cus_PurchaseItems (
                                purchase_id,
                                product_id,
                                quantity,
                                price_per_piece,
                                discount_per_piece,
                                paid
                                )
                                VALUES (?, ?, ?, ?, ?, ?);
                        ''', (purchase_id, purchase[1], purchase[2], purchase[3], purchase[4],  purchase[5])
                    )
                    
                    
                    self.cursor.execute(
                        '''
                        UPDATE Products
                        SET current_quantity = current_quantity - ?,
                        WHERE product_id = ?;
                        '''
                        , (purchase[3], purchase[1])
                    )
                    
                    
                    if purchase[6] == 0:
                        total_price+= (float(purchase[2])-float(purchase[4])) * int(purchase[3])
                    total_quantity += int(purchase[3])
                    
                self.cursor.execute(
                    f'''
                    UPDATE Customers
                    SET {'Golden_Rose_amount_money' if supplier == 'golden rose' else 'Snow_White_amount_money'} = {'Golden_Rose_amount_money' if supplier == 'golden rose' else 'Snow_White_amount_money'} + ?, {'Golden_Rose_current_quantity' if supplier == 'golden rose' else 'Snow_White_current_quantity'} = {'Golden_Rose_current_quantity' if supplier == 'golden rose' else 'Snow_White_current_quantity'} + ?
                    WHERE customer_id = ?;
                    ''', (total_price,total_quantity, buy[0][0])
                )
                
                



            self.conn.commit()
            return True
        except Exception as e:
            print(f"there is an error in insert_buys_to_db: {e}")
            return False


