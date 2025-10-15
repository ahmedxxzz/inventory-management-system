import sqlite3, os
from datetime import datetime, timedelta

class MainModel:
    def __init__(self):
        self.db_file = "IMS.db"
        is_exist = False
        if os.path.exists(self.db_file):
            print(f"Database {self.db_file} already exists. Skipping database setup.......")
            is_exist = True
        self.conn = sqlite3.connect(self.db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()
        if not is_exist:
            print(f"Database {self.db_file} isn't exists. Setting up database........")
            self.create_tables()

    
    def create_tables(self):
        try:

            self.cursor.executescript('''
                    -- #####################################################################
                    -- #      SQLite3 Database Schema - Final Version with AUTOINCREMENT     #
                    -- #####################################################################

                    -- IMPORTANT: This PRAGMA should be executed at the start of each database connection
                    -- to enforce foreign key constraints in SQLite.
                    PRAGMA foreign_keys = ON;

                    -- =====================================================================
                    -- 1. Core Entity Tables
                    -- =====================================================================

                    CREATE TABLE Distributor (
                    distributor_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE
                    );

                    CREATE TABLE Wallets (
                    wallet_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    current_balance NUMERIC NOT NULL DEFAULT 0.00
                    );

                    CREATE TABLE Factories (
                    factory_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    current_balance NUMERIC NOT NULL DEFAULT 0.00,
                    current_quantity INTEGER NOT NULL DEFAULT 0,
                    last_purchase_date TEXT
                    );

                    CREATE TABLE Product (
                    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    weighted_average_cost NUMERIC NOT NULL DEFAULT 0.00,
                    selling_price NUMERIC NOT NULL DEFAULT 0.00,
                    available_quantity INTEGER NOT NULL DEFAULT 0,
                    low_stock_threshold INTEGER NOT NULL DEFAULT 20,
                    distributor_id INTEGER NOT NULL,
                    FOREIGN KEY (distributor_id) REFERENCES Distributor(distributor_id)
                    );

                    CREATE TABLE Customer (
                    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE
                    );

                    CREATE TABLE Customer_Distributor_Accounts (
                        account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        customer_id INTEGER NOT NULL,
                        distributor_id INTEGER NOT NULL,
                        current_balance NUMERIC NOT NULL DEFAULT 0.00,
                        current_quantity INTEGER NOT NULL DEFAULT 0,
                        last_payment_date TEXT,
                        UNIQUE(customer_id, distributor_id),
                        FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
                        FOREIGN KEY (distributor_id) REFERENCES Distributor(distributor_id)
                    );

                    -- =====================================================================
                    -- 2. Factory Transaction Tables (with Ledger Fields)
                    -- =====================================================================

                    CREATE TABLE Factory_Purchases_Bills (
                    purchases_bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    total_amount NUMERIC NOT NULL,
                    is_paid INTEGER NOT NULL DEFAULT 0,
                    balance_before NUMERIC NOT NULL,
                    balance_after NUMERIC NOT NULL,
                    factory_id INTEGER NOT NULL,
                    FOREIGN KEY (factory_id) REFERENCES Factories(factory_id)
                    );

                    CREATE TABLE Factory_Purchases_Bill_Items (
                    bill_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    quantity INTEGER NOT NULL,
                    price_per_item NUMERIC NOT NULL,
                    discount_per_item NUMERIC NOT NULL DEFAULT 0.00,
                    purchases_bill_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    FOREIGN KEY (purchases_bill_id) REFERENCES Factory_Purchases_Bills(purchases_bill_id) ON DELETE CASCADE,
                    FOREIGN KEY (product_id) REFERENCES Product(product_id)
                    );

                    CREATE TABLE Factory_Pays (
                    pay_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount_paid NUMERIC NOT NULL,
                    date TEXT NOT NULL,
                    balance_before NUMERIC NOT NULL,
                    balance_after NUMERIC NOT NULL,
                    factory_id INTEGER NOT NULL,
                    wallet_id INTEGER NOT NULL,
                    FOREIGN KEY (factory_id) REFERENCES Factories(factory_id),
                    FOREIGN KEY (wallet_id) REFERENCES Wallets(wallet_id)
                    );

                    CREATE TABLE Factory_Returns (
                    return_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    total_amount NUMERIC NOT NULL,
                    balance_before NUMERIC NOT NULL,
                    balance_after NUMERIC NOT NULL,
                    factory_id INTEGER NOT NULL,
                    reason TEXT DEFAULT NULL,
                    FOREIGN KEY (factory_id) REFERENCES Factories(factory_id)
                    );

                    CREATE TABLE Factory_Return_Items (
                    return_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    quantity INTEGER NOT NULL,
                    price_at_return NUMERIC NOT NULL,
                    return_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    FOREIGN KEY (return_id) REFERENCES Factory_Returns(return_id) ON DELETE CASCADE,
                    FOREIGN KEY (product_id) REFERENCES Product(product_id)
                    );

                    -- =====================================================================
                    -- 3. Customer Transaction Tables (with Ledger Fields)
                    -- =====================================================================

                    CREATE TABLE Customer_Sales_Bills (
                    sales_bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    total_amount NUMERIC NOT NULL,
                    is_paid INTEGER NOT NULL DEFAULT 0,
                    balance_before NUMERIC NOT NULL,
                    balance_after NUMERIC NOT NULL,
                    customer_id INTEGER NOT NULL,
                    distributor_id INTEGER NOT NULL,
                    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
                    FOREIGN KEY (distributor_id) REFERENCES Distributor(distributor_id)
                    );

                    CREATE TABLE Customer_Sales_Bill_Items (
                    bill_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    quantity INTEGER NOT NULL,
                    price_per_item NUMERIC NOT NULL,
                    discount_per_item NUMERIC NOT NULL DEFAULT 0.00,
                    product_id INTEGER NOT NULL,
                    sales_bill_id INTEGER NOT NULL,
                    FOREIGN KEY (product_id) REFERENCES Product(product_id),
                    FOREIGN KEY (sales_bill_id) REFERENCES Customer_Sales_Bills(sales_bill_id) ON DELETE CASCADE
                    );

                    CREATE TABLE Customer_Pays (
                    pay_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    amount_paid NUMERIC NOT NULL,
                    balance_before NUMERIC NOT NULL,
                    balance_after NUMERIC NOT NULL,
                    wallet_id INTEGER NOT NULL,
                    customer_id INTEGER NOT NULL,
                    distributor_id INTEGER NOT NULL,
                    FOREIGN KEY (wallet_id) REFERENCES Wallets(wallet_id),
                    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
                    FOREIGN KEY (distributor_id) REFERENCES Distributor(distributor_id)
                    );

                    CREATE TABLE Customer_Returns (
                    return_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    total_amount NUMERIC NOT NULL,
                    balance_before NUMERIC NOT NULL,
                    balance_after NUMERIC NOT NULL,
                    customer_id INTEGER NOT NULL,
                    distributor_id INTEGER NOT NULL,
                    reason TEXT DEFAULT NULL,
                    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
                    FOREIGN KEY (distributor_id) REFERENCES Distributor(distributor_id)
                    );

                    CREATE TABLE Customer_Return_Items (
                    return_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    price_at_return NUMERIC NOT NULL,
                    quantity INTEGER NOT NULL,
                    return_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    FOREIGN KEY (return_id) REFERENCES Customer_Returns(return_id) ON DELETE CASCADE,
                    FOREIGN KEY (product_id) REFERENCES Product(product_id)
                    );

                    -- =====================================================================
                    -- 4. General & Notification Tables
                    -- =====================================================================

                    CREATE TABLE Costs (
                    cost_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount NUMERIC NOT NULL,
                    date TEXT NOT NULL,
                    description TEXT NOT NULL,
                    wallet_id INTEGER NOT NULL,
                    FOREIGN KEY (wallet_id) REFERENCES Wallets(wallet_id)
                    );

                    CREATE TABLE Notifications (
                    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    message TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'unseen',
                    type TEXT NOT NULL,
                    reference_id INTEGER
                    );
                    ''')
        
            self.conn.commit()

        except Exception as e:
            print(f"there is an error in creating tables: {e}")


    def get_distributors(self):
        """get distributors names

        Returns:
            list: distributors names
        """
        self.cursor.execute("SELECT name FROM Distributor")
        distributors = self.cursor.fetchall() # = [(name1,), (name2,), ...]
        distributors_list_names = [distributor[0] for distributor in distributors]
        return distributors_list_names # = [name1, name2, ...]


    def generate_all_notifications(self):
        """
        Master function to generate all types of notifications.
        This version is THREAD-SAFE as it creates its own database connection.
        """
        conn = None  # Ensure conn is defined in case the try block fails early
        try:
            # Create a NEW connection specifically for this thread's execution
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            # Call the helper methods, but pass the new cursor to them
            self._check_stale_factories(cursor)
            self._check_late_customer_payments(cursor)
            self._check_low_stock(cursor)
            
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error during notification generation in thread: {e}")
        finally:
            # CRITICAL: Always close the connection for this thread when done
            if conn:
                conn.close()

    def _check_stale_factories(self, cursor):
        """Generates notifications for stale factories using the provided cursor."""
        one_week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        # Use the passed cursor, NOT self.cursor
        cursor.execute("SELECT factory_id, name FROM Factories WHERE last_purchase_date < ?", (one_week_ago,))
        stale_factories = cursor.fetchall()
        for factory_id, name in stale_factories:
            cursor.execute("SELECT 1 FROM Notifications WHERE type = 'stale_factory' AND reference_id = ? AND status = 'unseen'", (factory_id,))
            if cursor.fetchone() is None:
                message = f"لم تتم أي عملية شراء من مصنع '{name}' منذ أكثر من أسبوع."
                cursor.execute("INSERT INTO Notifications (date, message, type, reference_id) VALUES (?, ?, 'stale_factory', ?)", (datetime.now().strftime('%Y-%m-%d %H:%M'), message, factory_id))

    def _check_late_customer_payments(self, cursor):
        """Generates notifications for late payments using the provided cursor."""
        cursor.execute("""
            SELECT cda.account_id, c.name, d.name, cda.last_payment_date
            FROM Customer_Distributor_Accounts cda
            JOIN Customer c ON c.customer_id = cda.customer_id
            JOIN Distributor d ON d.distributor_id = cda.distributor_id
            WHERE cda.current_balance > 0 AND cda.last_payment_date IS NOT NULL
        """)
        late_accounts = cursor.fetchall()
        for account_id, customer_name, dist_name, last_payment_str in late_accounts:
            weeks_late = (datetime.now() - datetime.strptime(last_payment_str, '%Y-%m-%d')).days // 7
            if weeks_late > 0:
                cursor.execute("SELECT notification_id FROM Notifications WHERE type = 'late_payment' AND reference_id = ? AND status = 'unseen'", (account_id,))
                existing_notification = cursor.fetchone()
                message = f"العميل '{customer_name}' (موزع: {dist_name}) لم يدفع منذ {weeks_late} أسابيع."
                if existing_notification:
                    cursor.execute("UPDATE Notifications SET message = ? WHERE notification_id = ?", (message, existing_notification[0]))
                else:
                    cursor.execute("SELECT message FROM Notifications WHERE type = 'late_payment' AND reference_id = ? ORDER BY notification_id DESC LIMIT 1", (account_id,))
                    last_msg = cursor.fetchone()
                    if not last_msg or f"منذ {weeks_late} أسابيع" not in last_msg[0]:
                         cursor.execute("INSERT INTO Notifications (date, message, type, reference_id) VALUES (?, ?, 'late_payment', ?)", (datetime.now().strftime('%Y-%m-%d %H:%M'), message, account_id))

    def _check_low_stock(self, cursor):
        """Generates notifications for low stock using the provided cursor."""
        cursor.execute("SELECT product_id, name, available_quantity FROM Product WHERE available_quantity < low_stock_threshold")
        low_stock_products = cursor.fetchall()
        for product_id, name, qty in low_stock_products:
            cursor.execute("SELECT 1 FROM Notifications WHERE type = 'low_stock' AND reference_id = ? AND status = 'unseen'", (product_id,))
            if cursor.fetchone() is None:
                message = f"تنبيه نقص مخزون: الصنف '{name}' لديه {qty} قطعة متبقية فقط."
                cursor.execute("INSERT INTO Notifications (date, message, type, reference_id) VALUES (?, ?, 'low_stock', ?)", (datetime.now().strftime('%Y-%m-%d %H:%M'), message, product_id))

    # --- Functions below will still use self.cursor as they are called from the main thread ---
    def get_unseen_notification_count(self):
        self.cursor.execute("SELECT COUNT(*) FROM Notifications WHERE status = 'unseen'")
        return self.cursor.fetchone()[0]

    def get_unseen_notifications(self):
        self.cursor.execute("SELECT date, message FROM Notifications WHERE status = 'unseen' ORDER BY notification_id DESC")
        return self.cursor.fetchall()

    def mark_all_as_seen(self):
        self.cursor.execute("UPDATE Notifications SET status = 'seen' WHERE status = 'unseen'")
        self.conn.commit()
