import sqlite3

class CustomerReturnModel:
    def __init__(self, db_conn):
        self.conn = db_conn
        self.cursor = self.conn.cursor()

    def get_customers_by_distributor(self, distributor_id):
        """Fetches all customers associated with a specific distributor."""
        try:
            self.cursor.execute("""
                SELECT c.customer_id, c.name
                FROM Customer c
                JOIN Customer_Distributor_Accounts cda ON c.customer_id = cda.customer_id
                WHERE cda.distributor_id = ?
                ORDER BY c.name
            """, (distributor_id,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error in get_customers_by_distributor: {e}")
            return []

    def get_product_by_name_and_distributor(self, product_name, distributor_id):
        """
        Fetches a product's ID and selling price by its name, ensuring it belongs to the specified distributor.
        """
        try:
            self.cursor.execute("""
                SELECT product_id, name, selling_price
                FROM Product
                WHERE name = ? AND distributor_id = ?
            """, (product_name, distributor_id))
            return self.cursor.fetchone() # Returns (product_id, name, selling_price) or None
        except sqlite3.Error as e:
            print(f"Database error in get_product_by_name_and_distributor: {e}")
            return None

    def check_if_customer_purchased_product(self, customer_id, product_id, distributor_id):
        """
        Checks if a specific customer has ever purchased a specific product from a distributor.
        Returns True if a purchase history exists, False otherwise.
        """
        try:
            self.cursor.execute("""
                SELECT 1
                FROM Customer_Sales_Bill_Items csbi
                JOIN Customer_Sales_Bills csb ON csbi.sales_bill_id = csb.sales_bill_id
                WHERE csb.customer_id = ? 
                  AND csb.distributor_id = ? 
                  AND csbi.product_id = ?
                LIMIT 1
            """, (customer_id, distributor_id, product_id))
            return self.cursor.fetchone() is not None # Returns True if a row is found
        except sqlite3.Error as e:
            print(f"Database error in check_if_customer_purchased_product: {e}")
            return False

    # <<< --- NEW FUNCTION TO GET LAST PURCHASE PRICE --- START --->
    def get_last_purchase_price(self, customer_id, product_id, distributor_id):
        """
        Fetches the most recent price a customer paid for a specific product from a distributor.
        """
        try:
            self.cursor.execute("""
                SELECT csbi.price_per_item
                FROM Customer_Sales_Bill_Items csbi
                JOIN Customer_Sales_Bills csb ON csbi.sales_bill_id = csb.sales_bill_id
                WHERE csb.customer_id = ? 
                  AND csb.distributor_id = ? 
                  AND csbi.product_id = ?
                ORDER BY csb.date DESC, csb.sales_bill_id DESC
                LIMIT 1
            """, (customer_id, distributor_id, product_id))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"Database error in get_last_purchase_price: {e}")
            return None
    # <<< --- NEW FUNCTION --- END --->

    def add_return_transaction(self, data):
        """
        Adds a customer return transaction, updating all relevant tables.
        (This function remains unchanged)
        """
        try:
            self.cursor.execute("BEGIN TRANSACTION")
            # Ensure the account exists before trying to fetch from it
            self.cursor.execute("SELECT COUNT(*) FROM Customer_Distributor_Accounts WHERE customer_id = ? AND distributor_id = ?", (data['customer_id'], data['distributor_id']))
            if self.cursor.fetchone()[0] == 0:
                # This is a safeguard, though the UI flow should prevent this.
                raise sqlite3.Error(f"Account for customer_id {data['customer_id']} and distributor_id {data['distributor_id']} does not exist.")

            self.cursor.execute("SELECT current_balance, current_quantity FROM Customer_Distributor_Accounts WHERE customer_id = ? AND distributor_id = ?", (data['customer_id'], data['distributor_id']))
            
            result = self.cursor.fetchone()
            if result is None:
                raise sqlite3.Error("Failed to fetch customer account balances.")
            
            balance_before, quantity_before = result
            balance_after = balance_before - data['total_amount']
            self.cursor.execute("INSERT INTO Customer_Returns (date, total_amount, balance_before, balance_after, customer_id, distributor_id, reason) VALUES (?, ?, ?, ?, ?, ?, ?)", (data['date'], data['total_amount'], balance_before, balance_after, data['customer_id'], data['distributor_id'], data['reason']))
            return_id = self.cursor.lastrowid
            total_returned_quantity = 0
            for item in data['items_list']:
                total_returned_quantity += item['quantity']
                self.cursor.execute("INSERT INTO Customer_Return_Items (quantity, price_at_return, return_id, product_id) VALUES (?, ?, ?, ?)", (item['quantity'], item['price_at_return'], return_id, item['product_id']))
                self.cursor.execute("UPDATE Product SET available_quantity = available_quantity + ? WHERE product_id = ?", (item['quantity'], item['product_id']))
            quantity_after = quantity_before - total_returned_quantity
            self.cursor.execute("UPDATE Customer_Distributor_Accounts SET current_balance = ?, current_quantity = ? WHERE customer_id = ? AND distributor_id = ?", (balance_after, quantity_after, data['customer_id'], data['distributor_id']))
            self.conn.commit()
            return True, {'return_id': return_id, 'balance_before': balance_before, 'balance_after': balance_after}
        except sqlite3.Error as e:
            self.conn.rollback()
            return False, f"حدث خطأ أثناء حفظ المرتجع: {e}"

    def get_distributor_id_by_name(self, distributor_name):
        """Fetches the ID of a distributor by their name."""
        try:
            self.cursor.execute("SELECT distributor_id FROM Distributor WHERE name = ?", (distributor_name,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"Database error in get_distributor_id_by_name: {e}")
            return None

    def get_distributor_logo_by_name(self, distributor_name):
        try:
            self.cursor.execute("SELECT logo_path FROM Distributor WHERE name = ?", (distributor_name,))
            result = self.cursor.fetchone()
            return result[0] if result and result[0] else None
        except Exception as e:
            print(f"Error fetching logo path: {e}")
            return None