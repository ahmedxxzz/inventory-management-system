import sqlite3, os


class MainModel:
    def __init__(self):
        db_file = "IMS.db"
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        if os.path.exists(db_file):
            print(f"Database {db_file} already exists. Skipping database setup.......")
        else :
            print(f"Database {db_file} isn't exists. Setting up database........")
            self.create_tables()

    
    def create_tables(self):
        try:

            self.cursor.execute('''
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

