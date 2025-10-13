# model/Factory/factory_pay_model.py

import sqlite3
from datetime import date

class FactoryPayModel:
    def __init__(self, db_conn):
        """
        Initializes the model with a database connection.
        Args:
            db_conn: An active sqlite3 connection object.
        """
        self.conn = db_conn
        self.cursor = self.conn.cursor()

    def get_all_factories(self):
        # ... (This function remains unchanged) ...
        try:
            self.cursor.execute("SELECT factory_id, name, current_balance FROM Factories ORDER BY name")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

    def get_all_wallets(self):
        # ... (This function remains unchanged) ...
        try:
            self.cursor.execute("SELECT wallet_id, name, current_balance FROM Wallets ORDER BY name")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

    def add_payment(self, factory_id, wallet_id, amount_paid, payment_date):
        """
        Adds a payment record for a factory and updates balances in a single transaction.
        Returns:
            A tuple (success_boolean, message_or_data).
            On success: (True, {'pay_id': ..., 'balance_before': ..., 'balance_after': ...})
            On failure: (False, error_message)
        """
        try:
            self.cursor.execute("BEGIN TRANSACTION")

            # Get factory's current balance
            self.cursor.execute("SELECT current_balance FROM Factories WHERE factory_id = ?", (factory_id,))
            factory_balance_before = self.cursor.fetchone()[0]

            # Check wallet's balance
            self.cursor.execute("SELECT current_balance FROM Wallets WHERE wallet_id = ?", (wallet_id,))
            wallet_balance = self.cursor.fetchone()[0]

            if wallet_balance < amount_paid:
                self.conn.rollback()
                return False, "رصيد الخزنة غير كافٍ لإتمام العملية."

            # Calculate and update balances
            factory_balance_after = factory_balance_before - amount_paid
            self.cursor.execute(
                "UPDATE Factories SET current_balance = ? WHERE factory_id = ?",
                (factory_balance_after, factory_id)
            )
            self.cursor.execute(
                "UPDATE Wallets SET current_balance = current_balance - ? WHERE wallet_id = ?",
                (amount_paid, wallet_id)
            )

            # Insert the payment record
            self.cursor.execute(
                """
                INSERT INTO Factory_Pays (amount_paid, date, balance_before, balance_after, factory_id, wallet_id)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (amount_paid, payment_date, factory_balance_before, factory_balance_after, factory_id, wallet_id)
            )
            
            # <<< --- START OF CHANGE --- >>>
            # Get the ID of the newly inserted payment record
            new_pay_id = self.cursor.lastrowid
            # <<< --- END OF CHANGE --- >>>

            self.conn.commit()
            
            # <<< --- START OF CHANGE --- >>>
            # Add the new_pay_id to the returned data dictionary
            payment_data = {
                'pay_id': new_pay_id,
                'balance_before': factory_balance_before,
                'balance_after': factory_balance_after
            }
            return True, payment_data
            # <<< --- END OF CHANGE --- >>>

        except sqlite3.Error as e:
            self.conn.rollback()
            print(f"Transaction failed: {e}")
            return False, f"حدث خطأ أثناء حفظ البيانات: {e}"