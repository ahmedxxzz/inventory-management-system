import sqlite3

class FactoryBuyModel:
    def __init__(self, db_conn):
        self.conn = db_conn
        
    def get_product_details_for_purchase(self, product_name, factory_name):
        """
        Fetches details for an existing product relevant to a new purchase.
        - Gets the distributor name.
        - Gets the last purchase price for this product FROM THIS SPECIFIC FACTORY.
        Returns a dictionary like {'distributor_name': '...', 'last_price': ...} or None.
        """
        details = {'distributor_name': None, 'last_price': None}
        cursor = self.conn.cursor()

        try:
            # First, get the product's distributor
            cursor.execute("""
                SELECT d.name 
                FROM Product p
                JOIN Distributor d ON p.distributor_id = d.distributor_id
                WHERE p.name = ?
            """, (product_name,))
            
            result = cursor.fetchone()
            if not result:
                return None # Product does not exist at all
            
            details['distributor_name'] = result[0]

            # Second, get the last purchase price from the specific factory
            query = """
                SELECT fpi.price_per_item - fpi.discount_per_item
                FROM Factory_Purchases_Bill_Items fpi
                JOIN Factory_Purchases_Bills fpb ON fpi.purchases_bill_id = fpb.purchases_bill_id
                JOIN Product p ON fpi.product_id = p.product_id
                JOIN Factories f ON fpb.factory_id = f.factory_id
                WHERE p.name = ? AND f.name = ?
                ORDER BY fpb.date DESC, fpb.purchases_bill_id DESC
                LIMIT 1
            """
            cursor.execute(query, (product_name, factory_name))
            price_result = cursor.fetchone()
            if price_result:
                details['last_price'] = price_result[0]
                
            return details

        except sqlite3.Error as e:
            print(f"Database error while fetching product details: {e}")
            return None

    def get_all_factories(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM Factories ORDER BY name")
            return [row[0] for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

    def get_all_distributors(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM Distributor ORDER BY name")
            return [row[0] for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
            
    def is_new_product(self, product_name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT 1 FROM Product WHERE name = ?", (product_name,))
        return cursor.fetchone() is None

    def save_purchase_bill(self, bill_data):
        cursor = self.conn.cursor()
        try:
            cursor.execute("BEGIN TRANSACTION")

            factory_name = bill_data['factory_name']
            cursor.execute("SELECT factory_id, current_balance FROM Factories WHERE name = ?", (factory_name,))
            factory_result = cursor.fetchone()
            if not factory_result:
                raise ValueError(f"المصنع '{factory_name}' غير موجود.")
            factory_id, factory_balance_before = factory_result
            
            factory_balance_after = factory_balance_before
            if bill_data['is_paid'] == 0:
                factory_balance_after += bill_data['total_amount']

            cursor.execute("""
                INSERT INTO Factory_Purchases_Bills (date, total_amount, is_paid, balance_before, balance_after, factory_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (bill_data['date'], bill_data['total_amount'], bill_data['is_paid'], factory_balance_before, factory_balance_after, factory_id))
            
            purchases_bill_id = cursor.lastrowid

            total_quantity_purchased = 0
            for item in bill_data['items']:
                product_id = None
                
                cursor.execute("SELECT product_id, available_quantity, weighted_average_cost, distributor_id FROM Product WHERE name = ?", (item['product_name'],))
                product_row = cursor.fetchone()
                
                if product_row:
                    product_id, old_qty, old_wac, dist_id = product_row
                else:
                    cursor.execute("SELECT distributor_id FROM Distributor WHERE name = ?", (item['distributor_name'],))
                    dist_row = cursor.fetchone()
                    if not dist_row:
                        raise ValueError(f"الموزع '{item['distributor_name']}' غير موجود.")
                    dist_id = dist_row[0]
                    
                    cursor.execute("INSERT INTO Product (name, distributor_id) VALUES (?, ?)", (item['product_name'], dist_id))
                    product_id = cursor.lastrowid
                    old_qty, old_wac = 0, 0.0
                
                cursor.execute("""
                    INSERT INTO Factory_Purchases_Bill_Items (quantity, price_per_item, discount_per_item, purchases_bill_id, product_id)
                    VALUES (?, ?, ?, ?, ?)
                """, (item['quantity'], item['price'], item['discount'], purchases_bill_id, product_id))

                new_qty = item['quantity']
                new_price = item['price'] - item['discount']
                
                if (old_qty + new_qty) > 0:
                    new_wac = ((old_qty * old_wac) + (new_qty * new_price)) / (old_qty + new_qty)
                else:
                    new_wac = new_price

                cursor.execute("""
                    UPDATE Product 
                    SET available_quantity = available_quantity + ?, weighted_average_cost = ?
                    WHERE product_id = ?
                """, (new_qty, new_wac, product_id))
                
                total_quantity_purchased += new_qty

            if bill_data['is_paid'] == 0:
                 cursor.execute("""
                    UPDATE Factories 
                    SET current_balance = ?, current_quantity = current_quantity + ?, last_purchase_date = ?
                    WHERE factory_id = ?
                """, (factory_balance_after, total_quantity_purchased, bill_data['date'], factory_id))
            else:
                 cursor.execute("""
                    UPDATE Factories 
                    SET current_quantity = current_quantity + ?, last_purchase_date = ?
                    WHERE factory_id = ?
                """, (total_quantity_purchased, bill_data['date'], factory_id))

            self.conn.commit()

        except Exception as e:
            cursor.execute("ROLLBACK")
            raise e

