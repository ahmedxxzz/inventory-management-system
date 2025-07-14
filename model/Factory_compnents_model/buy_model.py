import sqlite3
from sqlite3 import Error
from datetime import datetime


class BuyModel:
    def __init__(self):
        self.conn = sqlite3.connect('IMS.db')
        self.cursor = self.conn.cursor()



    def get_factory_names_and_money(self):
        '''
        return_data = [ ('حماده طلبة', 50000.0), ('عمرو هلال', 75000.0), ('علاء احمد', 30000.0), ]
        '''        
        self.cursor.execute("SELECT name, amount_money FROM Factories")
        return self.cursor.fetchall()


    def get_products_codes(self):
        self.cursor.execute("SELECT type, 0 FROM Products")
        '''
        returned data = [ ('1001', 0), ('1002', 0), ('1003', 0), ]
        '''
        return self.cursor.fetchall()


    def get_buys_from_db(self ):

        '''
        data returned example :
        [ [facname, time, productcode, price, quantity, discount, total price, paid or not], ]
        
        '''
        self.cursor.execute(
            '''
            SELECT
            F.name,
            FP.purchas_date,
            P.type,
            FPI.price_per_piece ,
            FPI.quantity,
            FPI.discount_per_piece,
            (FPI.price_per_piece - FPI.discount_per_piece) * FPI.quantity AS total_price,
            CASE
                WHEN FPI.paid = 1 THEN 'نعم'
                ELSE 'لا'
                END AS paid_status
            FROM Factories AS F
            JOIN Fac_Purchases AS FP
            ON F.factory_id = FP.factory_id
            JOIN Fac_PurchaseItems AS FPI
            ON FP.purchase_id = FPI.purchase_id
            JOIN Products AS P
            ON FPI.product_id = P.product_id;
            '''
        )
        
        return self.cursor.fetchall()


    def get_fac_id_from_name(self, name):
        self.cursor.execute("SELECT factory_id FROM Factories WHERE name = ?", (name,))
        return self.cursor.fetchone()[0]


    def get_product_id_from_code(self, code):
        self.cursor.execute("SELECT product_id FROM Products WHERE type = ?", (code,))
        return self.cursor.fetchone()[0]


    def get_fac_money_by_id(self, id):
        self.cursor.execute("SELECT amount_money FROM Factories WHERE factory_id = ?", (id,))
        return self.cursor.fetchone()[0]
    

    def insert_buys_to_db(self, buys):
        '''
        buys = [
            {
                'facname': 'facname',
                'productcode': 'productcode',
                'price': 0,
                'quantity': 0,
                'discount': 0,
                'supplier': 'golden rose',
                'paid': 'paid or not',
            },
            {
                'facname': 'facname',
                'productcode': 'productcode',
                'price': 0,
                'quantity': 0,
                'discount': 0,
                'supplier': 'golden rose',
                'paid': 'paid or not',
            },
        ]
        '''
        
        
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for buy in buys:
            buy['facname'] = self.get_fac_id_from_name(buy['facname'])
            buy['productcode'] = self.get_product_id_from_code(buy['productcode'])
        buys.sort(key=lambda x: x['facname'])
        
        
        def group_by_factory(buys):
            fac_grouped_lists = []
            current_group = [buys[0]] 
            for i in range(1, len(buys)):
                if buys[i]['facname'] == current_group[0]['facname']:
                    current_group.append(buys[i])
                else:
                    
                    fac_grouped_lists.append(current_group)
                    current_group = [buys[i]]
            fac_grouped_lists.append(current_group) 
            return fac_grouped_lists
        
        buys = group_by_factory(buys)
        '''
        now buys = [
            # [ list of buys of the same factory ]
            
             [{'facname': 'facid', 'productcode': 'productcode id', 'price': 0, 'quantity': 0, 'discount': 0, 'supplier': 'golden rose', 'paid': 'paid or not', },{'facname': 'facname', 'productcode': 'productcode', 'price': 0, 'quantity': 0, 'discount': 0, 'supplier': 'golden rose', 'paid': 'paid or not', },],
             [{'facname': 'facid', 'productcode': 'productcode id', 'price': 0, 'quantity': 0, 'discount': 0, 'supplier': 'golden rose', 'paid': 'paid or not', },{'facname': 'facname', 'productcode': 'productcode', 'price': 0, 'quantity': 0, 'discount': 0, 'supplier': 'golden rose', 'paid': 'paid or not', },],
             ]
        '''
        try :
            for buy in buys:
                self.cursor.execute('''
                    INSERT INTO Fac_Purchases (
                        factory_id,
                        purchas_date,
                        fac_money_before
                        
                        )
                        VALUES (?, ?, ?);
                    ''',
                    (buy[0]['facname'], date, self.get_fac_money_by_id(buy[0]['facname']))
                )
                purchase_id = self.cursor.lastrowid
                
                
                total_price = 0
                total_quantity = 0
                for purchase in buy:
                    self.cursor.execute(
                        '''
                        INSERT INTO Fac_PurchaseItems (
                                purchase_id,
                                product_id,
                                quantity,
                                price_per_piece,
                                discount_per_piece,
                                resource_name,
                                paid
                                )
                                VALUES (?, ?, ?, ?, ?, ?, ?);
                        ''', (purchase_id, purchase['productcode'], purchase['quantity'], purchase['price'], purchase['discount'], purchase['supplier'], purchase['paid'])
                    )
                    
                    
                    self.cursor.execute(
                        '''
                        UPDATE Products
                        SET current_quantity = current_quantity + ?,
                        fac_price_per_piece = ?
                        WHERE product_id = ?;
                        '''
                        , (int(purchase['quantity']), float(purchase['price'])-float(purchase['discount']) , purchase['productcode'])
                    )
                    
                    
                    if purchase['paid'] != 0:
                        total_price+= (float(purchase['price'])-float(purchase['discount'])) * int(purchase['quantity'])
                    total_quantity += int(purchase['quantity'])
                    
                
                self.cursor.execute(
                    '''
                    UPDATE Fac_Purchases
                    SET cost_money = ?
                    WHERE purchase_id = ?;
                    ''', (total_price, purchase_id)
                )
                self.cursor.execute(
                    '''
                    UPDATE Factories
                    SET amount_money = amount_money + ?, current_quantity = current_quantity + ?
                    WHERE factory_id = ?;
                    ''', (total_price,total_quantity, buy[0]['facname'])
                )
                
                



            self.conn.commit()
            return True
        except Exception as e:
            print(f"there is an error in insert_buys_to_db: {e}")
            return False


    def get_supplier_from_procode(self, code):
        self.cursor.execute("SELECT resource_name FROM Products WHERE type = ?", (code,))
        return self.cursor.fetchone()[0]