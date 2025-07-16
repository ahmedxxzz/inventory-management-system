import sqlite3
import os
import datetime
import random


class MainModel:

    def __init__(self):
        db_file = "IMS.db"
        if os.path.exists(db_file):
            print(f"Database {db_file} already exists. Skipping database setup.")
        else :
            print(f"Database {db_file} isn't exists. Setting up database.")
            self.create_tables(db_file)
            # self.add_fake_data(db_file)

    


    def create_tables(self, filename):
        try:

            # Connect to SQLite database
            conn = sqlite3.connect(filename)
            cursor = conn.cursor()

            # Enable foreign key constraints
            cursor.execute("PRAGMA foreign_keys = ON;")

            # Create Factories table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Factories (
                    factory_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL ,
                    amount_money REAL DEFAULT 0 CHECK (amount_money >= 0),
                    current_quantity INTEGER DEFAULT 0 CHECK (current_quantity >= 0)
                );
            ''')

            # Create Products table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Products (
                    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT NOT NULL ,
                    current_quantity INTEGER DEFAULT 0 CHECK (current_quantity >= 0),
                    cus_price_per_piece REAL DEFAULT 0 CHECK (cus_price_per_piece >= 0),
                    fac_price_per_piece REAL DEFAULT 0 CHECK (fac_price_per_piece >= 0),
                    resource_name TEXT  check (resource_name == 'golden rose' or resource_name == 'snow white')
                );
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Fac_Pays (
                    pay_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    factory_id INTEGER NOT NULL,
                    safe_id INTEGER NOT NULL,
                    date TEXT NOT NULL ,
                    amount_money REAL NOT NULL,
                    fac_money_before REAL DEFAULT 0 CHECK (fac_money_before >= 0),
                    FOREIGN KEY (safe_id) REFERENCES Safe(safe_id),
                    FOREIGN KEY (factory_id) REFERENCES Factories(factory_id)
                );
            ''')

            # Create Purchases table
            cursor.execute('''
                        CREATE TABLE IF NOT EXISTS Fac_Purchases (
                            purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            purchas_date TEXT NOT NULL ,
                            fac_money_before REAL DEFAULT 0 CHECK (fac_money_before >= 0),
                            cost_money REAL Default 0 CHECK (cost_money >= 0),
                            factory_id INTEGER NOT NULL,
                            FOREIGN KEY (factory_id) REFERENCES Factories(factory_id) 
                        );
                    ''')


            # Create PurchaseItems table
            cursor.execute('''
                        CREATE TABLE IF NOT EXISTS Fac_PurchaseItems (
                            purchase_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            purchase_id INTEGER NOT NULL,
                            product_id INTEGER NOT NULL,
                            quantity INTEGER NOT NULL CHECK (quantity >= 0),
                            price_per_piece REAL NOT NULL CHECK (price_per_piece >= 0),
                            discount_per_piece REAL DEFAULT 0 CHECK (discount_per_piece >= 0),
                            paid boolean DEFAULT 0,
                            resource_name TEXT NOT NULL check (resource_name == 'golden rose' or resource_name == 'snow white'),
                            FOREIGN KEY (purchase_id) REFERENCES Fac_Purchases(purchase_id) ON DELETE CASCADE,
                            FOREIGN KEY (product_id) REFERENCES Products(product_id)
                        );
                        ''')


            cursor.execute('''
                        CREATE TABLE IF NOT EXISTS Fac_Returned_Items (
                            returned_process_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            date TEXT NOT NULL ,
                            product_id INTEGER NOT NULL,
                            quantity INTEGER NOT NULL CHECK (quantity >= 0), 
                            price_per_piece REAL NOT NULL CHECK (price_per_piece >= 0),
                            factory_id INTEGER NOT NULL,
                            reason TEXT ,
                            FOREIGN KEY (factory_id) REFERENCES Factories(factory_id) ,
                            FOREIGN KEY (product_id) REFERENCES Products(product_id)
                        );
                        ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Customers (
                    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL ,
                    Golden_Rose_amount_money REAL DEFAULT 0 CHECK (Golden_Rose_amount_money >= 0),
                    Golden_Rose_current_quantity INTEGER DEFAULT 0 CHECK (Golden_Rose_current_quantity >= 0),
                    Snow_White_amount_money REAL DEFAULT 0 CHECK (Snow_White_amount_money >= 0),
                    Snow_White_current_quantity INTEGER DEFAULT 0 CHECK (Snow_White_current_quantity >= 0)
                );
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS  Cus_Pays (
                    pay_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    amount_money REAL NOT NULL,
                    customer_id INTEGER NOT NULL,
                    resource_name TEXT NOT NULL check (resource_name == 'golden rose' or resource_name == 'snow white'),
                    safe_money_before REAL DEFAULT 0 CHECK (safe_money_before >= 0),
                    safe_id INTEGER NOT NULL,
                    customer_money_before REAL DEFAULT 0 CHECK (customer_money_before >= 0),
                    customer_money_after REAL DEFAULT 0 CHECK (customer_money_after >= 0),
                    FOREIGN KEY (safe_id) REFERENCES Safe(safe_id),
                    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
                    );
                ''')

            cursor.execute(''' 
                            CREATE TABLE IF NOT EXISTS Cus_Purchases (
                                purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                customer_id INTEGER NOT NULL,
                                purchase_date TEXT NOT NULL ,
                                discount_Total REAL DEFAULT 0 CHECK (discount_Total >= 0),
                                cost_money REAL Default 0 CHECK (cost_money >= 0),
                                cus_money_before REAL DEFAULT 0 CHECK (cus_money_before >= 0),
                                resource_name TEXT NOT NULL check (resource_name == 'golden rose' or resource_name == 'snow white'),
                                FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
                            );''')
            # Create PurchaseItems table
            cursor.execute('''
                        CREATE TABLE IF NOT EXISTS Cus_PurchaseItems (
                            purchase_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            purchase_id INTEGER NOT NULL,
                            product_id INTEGER NOT NULL,
                            quantity INTEGER NOT NULL CHECK (quantity >= 0),
                            price_per_piece REAL NOT NULL CHECK (price_per_piece >= 0),
                            discount_per_piece REAL DEFAULT 0 CHECK (discount_per_piece >= 0),
                            paid boolean DEFAULT 0,
                            FOREIGN KEY (purchase_id) REFERENCES Cus_Purchases(purchase_id) ON DELETE CASCADE,
                            FOREIGN KEY (product_id) REFERENCES Products(product_id)
                        );''')

            cursor.execute('''
                        CREATE TABLE IF NOT EXISTS Cus_Returned_Items (
                            returned_process_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            date TEXT NOT NULL ,
                            product_id INTEGER NOT NULL,
                            quantity INTEGER NOT NULL CHECK (quantity >= 0), 
                            price_per_piece REAL NOT NULL CHECK (price_per_piece >= 0),
                            resource_name TEXT NOT NULL check (resource_name == 'golden rose' or resource_name == 'snow white'),
                            reason TEXT ,
                            customer_id INTEGER NOT NULL,
                            FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ,
                            FOREIGN KEY (product_id) REFERENCES Products(product_id)
                        );''')

            cursor.execute('''
                        CREATE TABLE IF NOT EXISTS Safe (
                            safe_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            type TEXT NOT NULL UNIQUE,
                            amount_money REAL DEFAULT 0 CHECK (amount_money >= 0)
                            );
                        ''')
            
            cursor.execute('''
                        CREATE TABLE IF NOT EXISTS Additional_Costs (
                            addcost_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            type TEXT NOT NULL ,
                            date TEXT NOT NULL ,
                            amount_of_money REAL NOT NULL CHECK (amount_of_money >= 0),
                            safe_id INTEGER NOT NULL,
                            FOREIGN KEY (safe_id) REFERENCES Safe(safe_id)
                        );
                        ''')

            conn.commit()

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            # Close the connection
            conn.close()
