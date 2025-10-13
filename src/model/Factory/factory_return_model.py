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

    def get_products_by_factory(self, factory_id):
        """
        Retrieves all unique products ever purchased from a specific factory.
        (This fulfills requirement #1)
        """
        try:
            self.cursor.execute("""
                SELECT DISTINCT p.product_id, p.name
                FROM Product p
                JOIN Factory_Purchases_Bill_Items fpi ON p.product_id = fpi.product_id
                JOIN Factory_Purchases_Bills fpb ON fpi.purchases_bill_id = fpb.purchases_bill_id
                WHERE fpb.factory_id = ?
                ORDER BY p.name
            """, (factory_id,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

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
        Args:
            items_list: A list of dictionaries, each with {'product_id', 'quantity', 'price_at_return'}
        Returns:
            Tuple (success_boolean, message_or_data)
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

