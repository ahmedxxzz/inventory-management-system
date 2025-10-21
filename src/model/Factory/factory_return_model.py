import sqlite3

class FactoryReturnModel:
    def __init__(self, db_conn):
        self.conn = db_conn
        self.cursor = self.conn.cursor()

    def get_all_factories(self):
        """Retrieves all factories from the database."""
        try:
            self.cursor.execute("SELECT factory_id, name, current_balance FROM Factories ORDER BY name")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

    # <<<--- NEW, MORE SPECIFIC FUNCTION FOR VALIDATION --- START --->
    def get_purchased_product_by_name(self, product_name, factory_id):
        """
        Checks if a product exists AND has been purchased by the specified factory.
        Returns the product_id if valid, otherwise None.
        """
        try:
            self.cursor.execute("""
                SELECT p.product_id
                FROM Product p
                JOIN Factory_Purchases_Bill_Items fpi ON p.product_id = fpi.product_id
                JOIN Factory_Purchases_Bills fpb ON fpi.purchases_bill_id = fpb.purchases_bill_id
                WHERE p.name = ? AND fpb.factory_id = ?
                LIMIT 1
            """, (product_name, factory_id))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"Database error in get_purchased_product_by_name: {e}")
            return None
    # <<<--- NEW, MORE SPECIFIC FUNCTION FOR VALIDATION --- END --->

    def get_last_purchase_price(self, factory_id, product_id):
        """
        Gets the price of the last purchase for a specific product from a specific factory.
        """
        try:
            self.cursor.execute("""
                SELECT fpi.price_per_item
                FROM Factory_Purchases_Bill_Items fpi
                JOIN Factory_Purchases_Bills fpb ON fpi.purchases_bill_id = fpb.purchases_bill_id
                WHERE fpb.factory_id = ? AND fpi.product_id = ?
                ORDER BY fpb.date DESC, fpb.purchases_bill_id DESC
                LIMIT 1
            """, (factory_id, product_id))
            result = self.cursor.fetchone()
            return result[0] if result else 0.00
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return 0.00

    def add_return_transaction(self, factory_id, return_date, reason, items_list, total_amount):
        """
        Adds a return bill and its items, and updates factory and product balances in a single transaction.
        """
        try:
            self.cursor.execute("BEGIN TRANSACTION")

            self.cursor.execute("SELECT current_balance, current_quantity FROM Factories WHERE factory_id = ?", (factory_id,))
            balance_before, quantity_before = self.cursor.fetchone()
            
            balance_after = balance_before - total_amount
            
            self.cursor.execute("""
                INSERT INTO Factory_Returns (date, total_amount, balance_before, balance_after, factory_id, reason)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (return_date, total_amount, balance_before, balance_after, factory_id, reason))
            
            return_id = self.cursor.lastrowid
            
            total_returned_quantity = 0
            for item in items_list:
                total_returned_quantity += item['quantity']
                self.cursor.execute("""
                    INSERT INTO Factory_Return_Items (quantity, price_at_return, return_id, product_id)
                    VALUES (?, ?, ?, ?)
                """, (item['quantity'], item['price_at_return'], return_id, item['product_id']))
                
                self.cursor.execute(
                    "UPDATE Product SET available_quantity = available_quantity - ? WHERE product_id = ?",
                    (item['quantity'], item['product_id'])
                )
            
            quantity_after = quantity_before - total_returned_quantity
            self.cursor.execute(
                "UPDATE Factories SET current_balance = ?, current_quantity = ? WHERE factory_id = ?",
                (balance_after, quantity_after, factory_id)
            )

            self.conn.commit()
            return_data = { 'return_id': return_id, 'balance_before': balance_before, 'balance_after': balance_after, 'total_amount': total_amount }
            return True, return_data

        except sqlite3.Error as e:
            self.conn.rollback()
            print(f"Transaction failed: {e}")
            return False, f"حدث خطأ أثناء حفظ البيانات: {e}"