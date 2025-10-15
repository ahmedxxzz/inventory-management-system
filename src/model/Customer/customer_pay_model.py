import sqlite3

class CustomerPayModel:
    def __init__(self, db_conn):
        self.conn = db_conn
        self.cursor = self.conn.cursor()

    def get_customers_by_distributor(self, distributor_id):
        """Fetches all customers associated with a specific distributor and their balance."""
        try:
            self.cursor.execute("""
                SELECT c.customer_id, c.name, cda.current_balance
                FROM Customer c
                JOIN Customer_Distributor_Accounts cda ON c.customer_id = cda.customer_id
                WHERE cda.distributor_id = ?
                ORDER BY c.name
            """, (distributor_id,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error in get_customers_by_distributor: {e}")
            return []

    def get_all_wallets(self):
        """Retrieves all wallets with their current balance."""
        try:
            self.cursor.execute("SELECT wallet_id, name, current_balance FROM Wallets ORDER BY name")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error in get_all_wallets: {e}")
            return []

    def add_payment(self, customer_id, distributor_id, wallet_id, amount_paid, payment_date):
        """
        Adds a payment record from a customer and updates balances in a single transaction.
        """
        try:
            self.cursor.execute("BEGIN TRANSACTION")

            # 1. Get customer's account balance before the payment
            self.cursor.execute("""
                SELECT current_balance FROM Customer_Distributor_Accounts
                WHERE customer_id = ? AND distributor_id = ?
            """, (customer_id, distributor_id))
            balance_before = self.cursor.fetchone()[0]

            # 2. Calculate new customer balance (debt decreases)
            balance_after = balance_before - amount_paid

            # 3. Update customer's account balance and last payment date
            self.cursor.execute("""
                UPDATE Customer_Distributor_Accounts
                SET current_balance = ?, last_payment_date = ?
                WHERE customer_id = ? AND distributor_id = ?
            """, (balance_after, payment_date, customer_id, distributor_id))

            # 4. Update wallet's balance (money increases)
            self.cursor.execute(
                "UPDATE Wallets SET current_balance = current_balance + ? WHERE wallet_id = ?",
                (amount_paid, wallet_id)
            )

            # 5. Insert the payment record into Customer_Pays ledger
            self.cursor.execute("""
                INSERT INTO Customer_Pays (date, amount_paid, balance_before, balance_after, wallet_id, customer_id, distributor_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (payment_date, amount_paid, balance_before, balance_after, wallet_id, customer_id, distributor_id))
            
            pay_id = self.cursor.lastrowid

            self.conn.commit()
            return True, {'pay_id': pay_id, 'balance_before': balance_before, 'balance_after': balance_after}

        except sqlite3.Error as e:
            self.conn.rollback()
            print(f"Transaction failed in add_payment (Customer): {e}")
            return False, f"حدث خطأ أثناء حفظ الدفعة: {e}"

    def get_distributor_id_by_name(self, distributor_name):
        """Fetches the ID of a distributor by their name."""
        try:
            self.cursor.execute("SELECT distributor_id FROM Distributor WHERE name = ?", (distributor_name,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"Database error in get_distributor_id_by_name: {e}")
            return None

