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

    def get_products_purchased_by_customer(self, customer_id, distributor_id):
        """
        Fetches all unique products a specific customer has ever purchased from a specific distributor.
        This is the core of the new requirement.
        """
        try:
            self.cursor.execute("""
                SELECT DISTINCT p.product_id, p.name, p.selling_price
                FROM Product p
                JOIN Customer_Sales_Bill_Items csbi ON p.product_id = csbi.product_id
                JOIN Customer_Sales_Bills csb ON csbi.sales_bill_id = csb.sales_bill_id
                WHERE csb.customer_id = ? AND csb.distributor_id = ?
                ORDER BY p.name
            """, (customer_id, distributor_id))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error in get_products_purchased_by_customer: {e}")
            return []

    def add_return_transaction(self, data):
        """
        Adds a customer return transaction, updating all relevant tables.
        (This function remains unchanged)
        """
        try:
            self.cursor.execute("BEGIN TRANSACTION")
            self.cursor.execute("SELECT current_balance, current_quantity FROM Customer_Distributor_Accounts WHERE customer_id = ? AND distributor_id = ?", (data['customer_id'], data['distributor_id']))
            balance_before, quantity_before = self.cursor.fetchone()
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