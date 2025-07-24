import sqlite3
from sqlite3 import Error
from datetime import datetime


class BuyModel:
    def __init__(self, supplier):
        self.conn = sqlite3.connect('IMS.db')
        self.cursor = self.conn.cursor()
        self.supplier = supplier


    def get_customer_names_and_money(self):
        self.cursor.execute(f"SELECT name, {'Golden_Rose_amount_money' if self.supplier == 'golden rose' else 'Snow_White_amount_money'}  FROM Customers")
        '''
        returned data = [('احمد', 550), ('محمد', 500)]
        '''
        return self.cursor.fetchall()


    def get_products_codes(self):
        self.cursor.execute("SELECT type, 0 FROM Products Where resource_name = ?", (self.supplier,))
        '''
        returned data = [ ('1001', 0), ('1002', 0), ('1003', 0), ]
        '''
        return self.cursor.fetchall()


    def get_buys_from_db(self):

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
            ''', (self.supplier,)
        )

        return self.cursor.fetchall()


    def get_cus_id_from_name(self, name):
        self.cursor.execute("SELECT customer_id FROM Customers WHERE name = ?", (name,))
        return self.cursor.fetchone()[0]


    def get_product_id_from_code(self, code):
        self.cursor.execute("SELECT product_id FROM Products WHERE type = ?", (code,))
        return self.cursor.fetchone()[0]


    def get_product_price_from_id(self, code):
        self.cursor.execute("SELECT cus_price_per_piece FROM Products WHERE product_id = ?", (int(code),))
        return self.cursor.fetchone()[0]


    def get_cus_money_by_id(self, id):
        self.cursor.execute(f"SELECT {'Golden_Rose_amount_money' if self.supplier == 'golden rose' else 'Snow_White_amount_money'} FROM Customers WHERE customer_id = ?", (id,))
        data = self.cursor.fetchone()
        if data :
            return data[0]
        else :
            return 0


    def insert_buys_to_db(self, buys):
        '''
        buys = [
            {'cusname' : cusname, 'productcode' : productcode, 'quantity' : quantity, 'discount' : discount, 'paid' : yes(1) or not(0)},
            {'cusname' : cusname, 'productcode' : productcode, 'quantity' : quantity, 'discount' : discount, 'paid' : yes(1) or not(0)},
        ]
        '''
        
        
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for buy in buys:
            buy['cusname'] = self.get_cus_id_from_name(buy['cusname'])
            print(f"buy['productcode'] :{buy['productcode'] }")
            buy['productcode'] = self.get_product_id_from_code(buy['productcode'])
            print(f"buy['productcode'] :{buy['productcode'] }")
            buy['price'] = self.get_product_price_from_id(buy['productcode']) # price befor the discount
            print(f"buy['price'] :{buy['price'] }")

        buys.sort(key=lambda x: x['cusname'])
        
        
        def group_by_customer(buys):
            cus_grouped_lists = []
            current_group = [buys[0]] 
            for i in range(1, len(buys)):
                if buys[i]['cusname'] == current_group[0]['cusname']:
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
             [{'cusname' : cus id, 'price': price before the discount, 'productcode' : productcode id, 'quantity' : quantity, 'discount' : discount, 'paid' : yes(1) or not(0)}, {'cusname' : cus id, 'productcode' : productcode id, 'quantity' : quantity, 'discount' : discount, 'paid' : yes(1) or not(0)},],
             [{'cusname' : cus id, 'price': price before the discount, 'productcode' : productcode id, 'quantity' : quantity, 'discount' : discount, 'paid' : yes(1) or not(0)}, {'cusname' : cus id, 'productcode' : productcode id, 'quantity' : quantity, 'discount' : discount, 'paid' : yes(1) or not(0)},],
             ]
        '''
        total_discounts = []
        
        for buy in buys:
            totaldiscount = 0
            for item in buy:
                totaldiscount+= float(item['discount'])
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
                    (buy[0]['cusname'], date, self.get_cus_money_by_id(buy[0]['cusname']), total_discounts[buys.index(buy)], self.supplier,)
                )
                purchase_id = self.cursor.lastrowid
                
                
                total_price = 0
                total_quantity = 0
                for purchase in buy:
                    self.cursor.execute(
                        '''
                        INSERT INTO Cus_PurchaseItems (
                                purchase_id,
                                product_id,
                                quantity,
                                price_per_piece,
                                discount_per_piece,
                                paid)
                                VALUES (?, ?, ?, ?, ?, ?);
                        ''', (purchase_id, purchase['productcode'], purchase['quantity'],purchase['price'] ,purchase['discount'], purchase['paid'],)
                    )


                    self.cursor.execute(
                        '''
                        UPDATE Products
                        SET current_quantity = current_quantity - ?
                        WHERE product_id = ? and resource_name = ?;
                        '''
                        , (int(purchase['quantity']), purchase['productcode'], self.supplier,)
                    )
                    
                    
                    if purchase['paid'] != 0:
                        total_price+= (float(purchase['price'])-float(purchase['discount'])) * int(purchase['quantity'])
                    total_quantity += int(purchase['quantity'])

                self.cursor.execute(
                    '''
                    UPDATE Cus_Purchases
                    SET cost_money = ?
                    WHERE purchase_id = ?;
                    ''', (total_price, purchase_id, )
                )
                
                self.cursor.execute(
                    f'''
                    UPDATE Customers
                    SET {'Golden_Rose_amount_money' if self.supplier == 'golden rose' else 'Snow_White_amount_money'} = {'Golden_Rose_amount_money' if self.supplier == 'golden rose' else 'Snow_White_amount_money'} + ?, {'Golden_Rose_current_quantity' if self.supplier == 'golden rose' else 'Snow_White_current_quantity'} = {'Golden_Rose_current_quantity' if self.supplier == 'golden rose' else 'Snow_White_current_quantity'} + ?
                    WHERE customer_id = ?;
                    ''', (total_price,total_quantity, buy[0]['cusname'], )
                )
                self.set_products_notification(buy) # [{product_id : quantity, product_id : quantity}, {product_id : quantity, product_id : quantity}]
                self.set_cutomer_limit_notification(buy)
            
                
                



            self.conn.commit()
            return True
        except Exception as e:
            print(f"there is an error in insert_buys_to_db: {e}")
            return False



    def set_products_notification(self, buys):
        # buys = [{product_id : quantity, product_id : quantity}, {product_id : quantity, product_id : quantity}]
        for buy in buys:
            product_id = buy['productcode']
            pro_type, product_quantity = self.cursor.execute('select type, current_quantity from Products where product_id = ?;',(product_id,)).fetchone()
            if product_quantity <= 12:
                noti_type = "golden_product" if self.supplier== 'golden rose' else 'snow_product'
                self.cursor.execute('select message from Notifications where type = ? AND entity_id = ?;', (noti_type,product_id,))
                message  = self.cursor.fetchone()
                if message is None:
                    message = f"الكمية المتوفرة من المنتج : {pro_type} = {product_quantity} قطعة"
                    self.cursor.execute("INSERT INTO Notifications (type, seen, entity_id, message) VALUES (?, ?, ?, ?)", (noti_type, 0, product_id, message))
                    self.conn.commit()
                else:
                    message = f"الكمية المتوفرة من المنتج : {pro_type} = {product_quantity} قطعة"
                    self.cursor.execute("UPDATE Notifications SET seen=0, message = ? WHERE type = ? AND entity_id = ?", (message, noti_type, product_id,))
                self.conn.commit()

    def set_cutomer_limit_notification(self, buys):
        # buys = [{cusname : cus id,}, {cusname : cus id,}, {cusname : cus id,},]
        cutomer_id = buys[0]['cusname']
        if self.supplier == 'golden rose':
            cus_amount_money = self.cursor.execute('select Golden_Rose_amount_money from Customers where customer_id = ?;',(cutomer_id,)).fetchone()[0]
        else:
            cus_amount_money = self.cursor.execute('select Snow_White_amount_money from Customers where customer_id = ?;',(cutomer_id,)).fetchone()[0]


        if cus_amount_money //50000 >=1:
            if self.supplier == 'golden rose':
                message, seen = self.cursor.execute('select message, seen from Notifications where type = ? AND entity_id = ?;', ("golden_cus_overdue",cutomer_id,)).fetchone()
                if message is None or seen == 1:
                    message = f"ديون المكتب {self.get_cus_name_by_id(cutomer_id)} ل {self.supplier} تجاوزت المبلغ : {cus_amount_money} جنيه"
                    self.cursor.execute("INSERT INTO Notifications (type, seen, entity_id, message) VALUES (?, ?, ?, ?)", ("golden_cus_overdue", 0, cutomer_id, message))
                else:
                    if seen == 0:
                        last_noti_amount = float(message.split(' ')[-2])
                        if last_noti_amount//50000 != cus_amount_money//50000:
                            message = f"ديون المكتب {self.get_cus_name_by_id(cutomer_id)} ل {self.supplier} تجاوزت المبلغ : {cus_amount_money} جنيه" 
                            self.cursor.execute("INSERT INTO Notifications (type, seen, entity_id, message) VALUES (?, ?, ?, ?)", ("golden_cus_overdue", 0, cutomer_id, message))
            else:
                message, seen = self.cursor.execute('select message, seen from Notifications where type = ? AND entity_id = ?;', ("snow_cus_overdue",cutomer_id,)).fetchone()
                if message is None or seen == 1:
                    message = f"ديون المكتب {self.get_cus_name_by_id(cutomer_id)} ل {self.supplier} تجاوزت المبلغ : {cus_amount_money} جنيه"
                    self.cursor.execute("INSERT INTO Notifications (type, seen, entity_id, message) VALUES (?, ?, ?, ?)", ("snow_cus_overdue", 0, cutomer_id, message))
                else:
                    if seen == 0:
                        last_noti_amount = float(message.split(' ')[-2])
                        if last_noti_amount//50000 != cus_amount_money//50000:
                            message = f"ديون المكتب {self.get_cus_name_by_id(cutomer_id)} ل {self.supplier} تجاوزت المبلغ : {cus_amount_money} جنيه" 
                            self.cursor.execute("INSERT INTO Notifications (type, seen, entity_id, message) VALUES (?, ?, ?, ?)", ("snow_cus_overdue", 0, cutomer_id, message))
                        

    def get_cus_name_by_id(self, id):
        self.cursor.execute("SELECT name FROM Customers WHERE customer_id = ?", (id,))
        return self.cursor.fetchone()[0]