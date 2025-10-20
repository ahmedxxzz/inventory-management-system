import sqlite3

class CustomerSalesModel:
    def __init__(self, db_conn):
        self.conn = db_conn
        self.cursor = self.conn.cursor()

    def get_distributor_id_by_name(self, distributor_name):
        try:
            self.cursor.execute("SELECT distributor_id FROM Distributor WHERE name = ?", (distributor_name,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"Database error in get_distributor_id_by_name: {e}")
            return None

    def get_customers_by_distributor(self, distributor_id):
        try:
            self.cursor.execute("""
                SELECT c.customer_id, c.name
                FROM Customer c
                LEFT JOIN Customer_Distributor_Accounts cda ON c.customer_id = cda.customer_id
                WHERE cda.distributor_id = ?
                ORDER BY c.name
            """, (distributor_id,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error in get_customers_by_distributor: {e}")
            return []

    def get_products_by_distributor(self, distributor_id):
        try:
            self.cursor.execute(
                "SELECT product_id, name, selling_price, available_quantity FROM Product WHERE distributor_id = ? ORDER BY name",
                (distributor_id,)
            )
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error in get_products_by_distributor: {e}")
            return []

    def add_sales_transaction(self, data):
        try:
            self.cursor.execute("BEGIN TRANSACTION")

            self.cursor.execute("""
                SELECT current_balance, current_quantity FROM Customer_Distributor_Accounts
                WHERE customer_id = ? AND distributor_id = ?
            """, (data['customer_id'], data['distributor_id']))
            balance_before, quantity_before = self.cursor.fetchone()

            balance_after = balance_before + data['total_amount'] if data['is_paid'] == 0 else balance_before

            self.cursor.execute("""
                INSERT INTO Customer_Sales_Bills (date, total_amount, is_paid, balance_before, balance_after, customer_id, distributor_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (data['date'], data['total_amount'], data['is_paid'], balance_before, balance_after, data['customer_id'], data['distributor_id']))
            
            sales_bill_id = self.cursor.lastrowid

            total_sold_quantity = 0
            for item in data['items_list']:
                total_sold_quantity += item['quantity']
                # --- MODIFIED: Save only the value discount per item ---
                self.cursor.execute("""
                    INSERT INTO Customer_Sales_Bill_Items (quantity, price_per_item, discount_per_item, product_id, sales_bill_id)
                    VALUES (?, ?, ?, ?, ?)
                """, (item['quantity'], item['price'], item['discount'], item['product_id'], sales_bill_id))
                
                self.cursor.execute(
                    "UPDATE Product SET available_quantity = available_quantity - ? WHERE product_id = ?",
                    (item['quantity'], item['product_id'])
                )
                
                if item['initial_price'] == 0:
                    self.cursor.execute(
                        "UPDATE Product SET selling_price = ? WHERE product_id = ?",
                        (item['price'], item['product_id'])
                    )

            quantity_after = quantity_before + total_sold_quantity
            self.cursor.execute("""
                UPDATE Customer_Distributor_Accounts
                SET current_balance = ?, current_quantity = ?
                WHERE customer_id = ? AND distributor_id = ?
            """, (balance_after, quantity_after, data['customer_id'], data['distributor_id']))

            self.conn.commit()
            return True, {'sales_bill_id': sales_bill_id, 'balance_before': balance_before, 'balance_after': balance_after}

        except sqlite3.Error as e:
            self.conn.rollback()
            print(f"Transaction failed in add_sales_transaction: {e}")
            return False, f"حدث خطأ أثناء حفظ الفاتورة: {e}"

    def get_distributor_logo_by_name(self, distributor_name):
        # This function might need adjustment if logo_path isn't in the Distributor table
        try:
            # Assuming a 'logo_path' column exists in the Distributor table
            self.cursor.execute("SELECT logo_path FROM Distributor WHERE name = ?", (distributor_name,))
            result = self.cursor.fetchone()
            return result[0] if result and result[0] else None
        except Exception as e:
            print(f"Error fetching logo path: {e}")
            return None