import sqlite3
from sqlite3 import Error
import os 

class MainModel:
    def __init__(self):
        db_file = "IMS.db"
        if os.path.exists(db_file):
            print(f"Database {db_file} already exists. Skipping database setup.")
        else :
            print(f"Database {db_file} isn't exists. Setting up database.")
            self.main_setup_database(db_file)

    def create_connection(self,db_file):
        """ Create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print(f"SQLite version: {sqlite3.sqlite_version}")
            print(f"Successfully connected to {db_file}")
            conn.execute("PRAGMA foreign_keys = ON;")
        except Error as e:
            print(e)
        return conn

    def create_table(self, conn, create_table_sql):
        """ Create a table from the create_table_sql statement """
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
            print(f"Table created successfully: {create_table_sql.split('(')[0].replace('CREATE TABLE IF NOT EXISTS', '').strip()}")
        except Error as e:
            print(f"Error creating table: {e} SQL: {create_table_sql.split('(')[0].replace('CREATE TABLE IF NOT EXISTS', '').strip()}")


    def main_setup_database(self, database_file="inventory_management.db"):

        sql_create_factories_table='''
            CREATE TABLE IF NOT EXISTS Factories (
                factory_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                amount_money REAL DEFAULT 0 CHECK (amount_money >= 0),
                product_quantity INTEGER DEFAULT 0 CHECK (product_quantity >= 0)
            );
        '''
        # Create Products table
        sql_create_products_table= '''
            CREATE TABLE IF NOT EXISTS Products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL UNIQUE,
                color TEXT,
                current_quantity INTEGER DEFAULT 0 CHECK (current_quantity >= 0),
                cus_price_per_piece REAL NOT NULL DEFAULT 0 CHECK (cus_price_per_piece >= 0),
                fac_price_per_piece REAL NOT NULL DEFAULT 0 CHECK (fac_price_per_piece >= 0),
                resource_name TEXT NOT NULL check (resource_name == 'golden rose' or resource_name == 'snow white')
            );
        '''

        sql_create_fac_pays_table='''
            CREATE TABLE IF NOT EXISTS Fac_Pays (
                pay_id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL ,
                amount_money REAL NOT NULL,
                factory_id INTEGER NOT NULL,
                fac_money_before REAL DEFAULT 0 CHECK (fac_money_before >= 0),
                safe_id INTEGER NOT NULL,
                FOREIGN KEY (safe_id) REFERENCES Safe(safe_id),
                FOREIGN KEY (factory_id) REFERENCES Factories(factory_id) 
            );
        '''

        # Create Purchases table
        sql_create_fac_purchases_table='''
                    CREATE TABLE IF NOT EXISTS Fac_Purchases (
                        purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        purchas_date TEXT NOT NULL ,
                        fac_money_before REAL DEFAULT 0 CHECK (fac_money_before >= 0),
                        factory_id INTEGER NOT NULL,
                        paid boolean DEFAULT 0,
                        FOREIGN KEY (factory_id) REFERENCES Factories(factory_id) 
                    );
                '''
        
        
        # Create PurchaseItems table
        sql_create_fac_purchases_items_table='''
                    CREATE TABLE IF NOT EXISTS Fac_PurchaseItems (
                        purchase_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        purchase_id INTEGER NOT NULL,
                        product_id INTEGER NOT NULL,
                        quantity INTEGER NOT NULL CHECK (quantity >= 0),
                        price_per_piece REAL NOT NULL CHECK (price_per_piece >= 0),
                        discount_per_piece REAL DEFAULT 0 CHECK (discount_per_piece >= 0),
                        resource_name TEXT NOT NULL check (resource_name == 'golden rose' or resource_name == 'snow white'),
                        FOREIGN KEY (purchase_id) REFERENCES Fac_Purchases(purchase_id) ON DELETE CASCADE,
                        FOREIGN KEY (product_id) REFERENCES Products(product_id)
                    );
                       '''


        sql_create_fac_returned_items_table = '''
                    CREATE TABLE IF NOT EXISTS Fac_Returned_Items (
                        returned_process_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT NOT NULL ,
                        product_id INTEGER NOT NULL,
                        quantity INTEGER NOT NULL CHECK (quantity >= 0), 
                        price_per_piece REAL NOT NULL CHECK (price_per_piece >= 0),
                        reason TEXT ,
                        factory_id INTEGER NOT NULL,
                        FOREIGN KEY (factory_id) REFERENCES Factories(factory_id) ,
                        FOREIGN KEY (product_id) REFERENCES Products(product_id)
                    );
                    '''

        sql_create_customers_table= '''
            CREATE TABLE IF NOT EXISTS Customers (
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                Golden_Rose_amount_money REAL DEFAULT 0 CHECK (Golden_Rose_amount_money >= 0),
                Golden_Rose_current_quantity INTEGER DEFAULT 0 CHECK (Golden_Rose_current_quantity >= 0),
                Snow_White_amount_money REAL DEFAULT 0 CHECK (Snow_White_amount_money >= 0),
                Snow_White_current_quantity INTEGER DEFAULT 0 CHECK (Snow_White_current_quantity >= 0)
            );
        '''

        sql_create_customers_pays_table = '''
            CREATE TABLE IF NOT EXISTS  Cus_Pays (
                pay_id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL ,
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
            '''

        sql_create_customers_purchases_table =''' 
                        CREATE TABLE IF NOT EXISTS Cus_Purchases (
                            purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            purchase_date TEXT NOT NULL ,
                            discount_Total REAL DEFAULT 0 CHECK (discount_Total >= 0),
                            resource_name TEXT NOT NULL check (resource_name == 'golden rose' or resource_name == 'snow white'),
                            cus_money_before REAL DEFAULT 0 CHECK (cus_money_before >= 0),
                            paid boolean DEFAULT 0,
                            customer_id INTEGER NOT NULL,
                            FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
                        );'''


        sql_create_customers_purchases_items_table ='''
                    CREATE TABLE IF NOT EXISTS Cus_PurchaseItems (
                        purchase_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        purchase_id INTEGER NOT NULL,
                        product_id INTEGER NOT NULL,
                        quantity INTEGER NOT NULL CHECK (quantity >= 0),
                        price_per_piece REAL NOT NULL CHECK (price_per_piece >= 0),
                        discount_per_piece REAL DEFAULT 0 CHECK (discount_per_piece >= 0),
                        FOREIGN KEY (purchase_id) REFERENCES Cus_Purchases(purchase_id) ON DELETE CASCADE,
                        FOREIGN KEY (product_id) REFERENCES Products(product_id)
                    );'''

        sql_create_customers_returned_items_table = '''
                    CREATE TABLE IF NOT EXISTS Cus_Returned_Items (
                        returned_process_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT NOT NULL ,
                        product_id INTEGER NOT NULL,
                        quantity INTEGER NOT NULL CHECK (quantity >= 0), 
                        price_per_piece REAL NOT NULL CHECK (price_per_piece >= 0),
                        discount_per_piece REAL DEFAULT 0 CHECK (discount_per_piece >= 0),
                        resource_name TEXT NOT NULL check (resource_name == 'golden rose' or resource_name == 'snow white'),
                        reason TEXT ,
                        customer_id INTEGER NOT NULL,
                        FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ,
                        FOREIGN KEY (product_id) REFERENCES Products(product_id)
                    );'''

        sql_create_safe_table = '''
                    CREATE TABLE IF NOT EXISTS Safe (
                        safe_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        type TEXT NOT NULL UNIQUE,
                        amount_money REAL DEFAULT 0 CHECK (amount_money >= 0)
                        );
                    '''
        sql_create_notification_table = '''
                    CREATE TABLE IF NOT EXISTS Notifications (
                        notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        header TEXT NOT NULL ,
                        message TEXT NOT NULL ,
                        date TEXT NOT NULL
                        );
                    '''
        tables = [sql_create_customers_table, sql_create_safe_table, sql_create_factories_table, sql_create_products_table, sql_create_fac_pays_table, sql_create_fac_purchases_table, sql_create_fac_purchases_items_table, sql_create_fac_returned_items_table, sql_create_customers_table, sql_create_customers_pays_table, sql_create_customers_purchases_table, sql_create_customers_purchases_items_table, sql_create_customers_returned_items_table, sql_create_safe_table, sql_create_notification_table]

        # Create a database connection
        conn = self.create_connection(database_file)

        # Create tables
        if conn is not None:
            # Order matters due to Foreign Keys (Factories must exist before Products if Products references it)
            for table in tables:
                self.create_table(conn, table)

            conn.commit() # Commit changes
            conn.close()
            print(f"Database {database_file} and tables created/verified successfully.")
        else:
            print("Error! Cannot create the database connection.")






# import sqlite3
# from sqlite3 import Error

# def insert_sample_data(conn):
#     # This function remains the same as in the previous successful response.
#     # No changes needed here, as the issue is with table creation.
#     cursor = conn.cursor()

#     try:
#         # #############################################
#         # ### Independent Tables (can be inserted first)
#         # #############################################

#         # Safe Table
#         print("Inserting data into Safe table...")
#         safe_data = [
#             ('Main Safe', 100000.00),
#             ('Petty Cash', 5000.00),
#             ('Online Payments Safe', 25000.00)
#         ]
#         cursor.executemany("INSERT INTO Safe (type, amount_money) VALUES (?, ?)", safe_data)
#         print("Safe data inserted.")

#         # Factories Table
#         print("Inserting data into Factories table...")
#         factories_data = [
#             ('Bloomfield Manufacturing', 50000.00, 1000),
#             ('GreenValley Goods', 75000.00, 1500),
#             ('Sunrise Products Co.', 30000.00, 800)
#         ]
#         cursor.executemany("INSERT INTO Factories (name, amount_money, product_quantity) VALUES (?, ?, ?)", factories_data)
#         print("Factories data inserted.")

#         # Products Table
#         print("Inserting data into Products table...")
#         products_data = [
#             ('Premium Golden Rose Tea', 500, 15.00, 7.00, 'golden rose'),
#             ('Snow White Herbal Blend', 300, 12.50, 6.00, 'snow white'),
#             ('Golden Rose Extract', 100, 25.00, 12.00, 'golden rose'),
#             ('Snow White Calming Sachet', 200, 8.00, 3.50, 'snow white')
#         ]
#         cursor.executemany("INSERT INTO Products (type, current_quantity, cus_price_per_piece, fac_price_per_piece, resource_name) VALUES (?, ?, ?, ?, ?)", products_data)
#         print("Products data inserted.")

#         # Customers Table
#         print("Inserting data into Customers table...")
#         customers_data = [
#             ('Alice Wonderland', 250.00, 10, 180.00, 5),
#             ('Bob The Builder', 500.00, 20, 300.00, 15),
#             ('Charlie Brown', 150.00, 0, 90.00, 0)
#         ]
#         cursor.executemany("INSERT INTO Customers (name, Golden_Rose_amount_money, Golden_Rose_current_quantity, Snow_White_amount_money, Snow_White_current_quantity) VALUES (?, ?, ?, ?, ?)", customers_data)
#         print("Customers data inserted.")

#         # Notifications Table
#         print("Inserting data into Notifications table...")
#         notifications_data = [
#             ('Low Stock Alert', 'Product "Premium Golden Rose Tea" (ID 1) is running low. Current quantity: 500', '2023-10-26 10:00:00'),
#             ('Payment Received', 'Payment of $100.00 received from Customer "Alice Wonderland" (ID 1).', '2023-10-27 11:30:00'),
#             ('Factory Order Shipped', 'Order #FP001 from Bloomfield Manufacturing has been shipped.', '2023-10-28 14:00:00')
#         ]
#         cursor.executemany("INSERT INTO Notifications (header, message, date) VALUES (?, ?, ?)", notifications_data)
#         print("Notifications data inserted.")

#         # #############################################
#         # ### Dependent Tables (Factory related)
#         # #############################################

#         # Fac_Pays Table (FKs: factory_id, safe_id)
#         print("Inserting data into Fac_Pays table...")
#         fac_pays_data = [
#             ('2023-10-01 09:00:00', 5000.00, 1, 50000.00, 1),
#             ('2023-10-02 10:30:00', 7000.00, 2, 75000.00, 1),
#             ('2023-10-03 11:00:00', 200.00, 1, 45000.00, 2)
#         ]
#         cursor.executemany("INSERT INTO Fac_Pays (date, amount_money, factory_id, fac_money_before, safe_id) VALUES (?, ?, ?, ?, ?)", fac_pays_data)
#         print("Fac_Pays data inserted.")

#         # Fac_Purchases Table (FKs: factory_id)
#         print("Inserting data into Fac_Purchases table...")
#         fac_purchases_data = [
#             ('2023-09-15 14:00:00', 45000.00, 1),
#             ('2023-09-20 15:30:00', 68000.00, 2)
#         ]
#         cursor.executemany("INSERT INTO Fac_Purchases (purchas_date, fac_money_before, factory_id) VALUES (?, ?, ?)", fac_purchases_data)
#         print("Fac_Purchases data inserted.")

#         # Fac_PurchaseItems Table (FKs: purchase_id, product_id)
#         print("Inserting data into Fac_PurchaseItems table...")
#         fac_purchase_items_data = [
#             (1, 1, 200, 7.00, 0.50, 'golden rose'),
#             (1, 3, 50, 12.00, 1.00, 'golden rose'),
#             (2, 2, 150, 6.00, 0.25, 'snow white'),
#             (2, 4, 100, 3.50, 0.00, 'snow white')
#         ]
#         cursor.executemany("INSERT INTO Fac_PurchaseItems (purchase_id, product_id, quantity, price_per_piece, discount_per_piece, resource_name) VALUES (?, ?, ?, ?, ?, ?)", fac_purchase_items_data)
#         print("Fac_PurchaseItems data inserted.")

#         # Fac_Returned_Items Table (FKs: product_id, factory_id)
#         print("Inserting data into Fac_Returned_Items table...")
#         fac_returned_items_data = [
#             ('2023-09-25 10:00:00', 1, 10, 7.00, 1),
#             ('2023-09-28 11:00:00', 2, 5, 6.00, 2)
#         ]
#         cursor.executemany("INSERT INTO Fac_Returned_Items (date, product_id, quantity, price_per_piece, factory_id) VALUES (?, ?, ?, ?, ?)", fac_returned_items_data)
#         print("Fac_Returned_Items data inserted.")

#         # #############################################
#         # ### Dependent Tables (Customer related)
#         # #############################################

#         # Cus_Pays Table (FKs: customer_id, safe_id)
#         print("Inserting data into Cus_Pays table...")
#         cus_pays_data = [
#             ('2023-10-05 14:00:00', 100.00, 1, 'golden rose', 95000.00, 1, 250.00, 150.00),
#             ('2023-10-06 15:30:00', 50.00, 1, 'snow white', 95100.00, 1, 180.00, 130.00),
#             ('2023-10-07 16:00:00', 200.00, 2, 'golden rose', 25000.00, 3, 500.00, 300.00)
#         ]
#         cursor.executemany("INSERT INTO Cus_Pays (date, amount_money, customer_id, resource_name, safe_money_before, safe_id, customer_money_before, customer_money_after) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", cus_pays_data)
#         print("Cus_Pays data inserted.")

#         # Cus_Purchases Table (FKs: customer_id)
#         print("Inserting data into Cus_Purchases table...")
#         cus_purchases_data = [
#             ('2023-10-20 10:00:00', 5.00, 'golden rose', 150.00, 1),
#             ('2023-10-21 11:30:00', 2.50, 'snow white', 130.00, 1),
#             ('2023-10-22 12:00:00', 10.00, 'golden rose', 300.00, 2)
#         ]
#         cursor.executemany("INSERT INTO Cus_Purchases (purchase_date, discount_Total, resource_name, cus_money_before, customer_id) VALUES (?, ?, ?, ?, ?)", cus_purchases_data)
#         print("Cus_Purchases data inserted.")

#         # Cus_PurchaseItems Table (FKs: purchase_id, product_id)
#         print("Inserting data into Cus_PurchaseItems table...")
#         cus_purchase_items_data = [
#             (1, 1, 5, 15.00, 1.00),
#             (1, 3, 2, 25.00, 0.00),
#             (2, 2, 3, 12.50, 0.50),
#             (3, 1, 10, 15.00, 0.75),
#             (3, 3, 4, 25.00, 0.625)
#         ]
#         cursor.executemany("INSERT INTO Cus_PurchaseItems (purchase_id, product_id, quantity, price_per_piece, discount_per_piece) VALUES (?, ?, ?, ?, ?)", cus_purchase_items_data)
#         print("Cus_PurchaseItems data inserted.")

#         # Cus_Returned_Items Table (FKs: product_id, customer_id)
#         print("Inserting data into Cus_Returned_Items table...")
#         cus_returned_items_data = [
#             ('2023-10-25 09:00:00', 1, 1, 15.00, 1.00, 'golden rose', 1),
#             ('2023-10-26 14:30:00', 2, 1, 12.50, 0.50, 'snow white', 1)
#         ]
#         cursor.executemany("INSERT INTO Cus_Returned_Items (date, product_id, quantity, price_per_piece, discount_per_piece, resource_name, customer_id) VALUES (?, ?, ?, ?, ?, ?, ?)", cus_returned_items_data)
#         print("Cus_Returned_Items data inserted.")

#         conn.commit()
#         print("All data inserted successfully!")

#     except Error as e:
#         print(f"Error inserting data: {e}")
#         conn.rollback() # Rollback changes if an error occurs

# def create_connection(db_file):
#     """
#     Create a database connection to the SQLite database specified by db_file
#     """
#     conn = None
#     try:
#         conn = sqlite3.connect(db_file)
#         conn.execute("PRAGMA foreign_keys = ON;") # Enable foreign key enforcement
#         return conn
#     except Error as e:
#         print(f"Error connecting to database: {e}")
#     return conn

# def create_tables(conn):
#     """
#     Create tables based on the provided SQL schemas.
#     Corrected comment syntax from '#' to '--' for SQLite compatibility.
#     """
#     cursor = conn.cursor()

#     sql_create_safe_table = '''
#                     CREATE TABLE IF NOT EXISTS Safe (
#                         safe_id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         type TEXT NOT NULL UNIQUE,
#                         amount_money REAL DEFAULT 0 CHECK (amount_money >= 0)
#                         );
#                     '''
#     sql_create_factories_table='''
#             CREATE TABLE IF NOT EXISTS Factories (
#                 factory_id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 name TEXT NOT NULL UNIQUE,
#                 amount_money REAL DEFAULT 0 CHECK (amount_money >= 0),
#                 -- Corrected from 'current_quantity' in check to 'product_quantity' for consistency with column name.
#                 -- If 'current_quantity' in check was intentional for a column named 'product_quantity',
#                 -- please clarify. Using 'product_quantity' here to match the column name.
#                 product_quantity INTEGER DEFAULT 0 CHECK (product_quantity >= 0)
#             );
#         '''
#     sql_create_products_table= '''
#             CREATE TABLE IF NOT EXISTS Products (
#                 product_id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 type TEXT NOT NULL UNIQUE,
#                 current_quantity INTEGER DEFAULT 0 CHECK (current_quantity >= 0),
#                 cus_price_per_piece REAL NOT NULL DEFAULT 0 CHECK (cus_price_per_piece >= 0),
#                 fac_price_per_piece REAL NOT NULL DEFAULT 0 CHECK (fac_price_per_piece >= 0),
#                 resource_name TEXT NOT NULL check (resource_name == 'golden rose' or resource_name == 'snow white')
#             );
#         '''
#     sql_create_fac_pays_table='''
#             CREATE TABLE IF NOT EXISTS Fac_Pays (
#                 pay_id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 date TEXT NOT NULL ,
#                 amount_money REAL NOT NULL,
#                 factory_id INTEGER NOT NULL,
#                 fac_money_before REAL DEFAULT 0 CHECK (fac_money_before >= 0),
#                 safe_id INTEGER NOT NULL,
#                 FOREIGN KEY (safe_id) REFERENCES Safe(safe_id),
#                 FOREIGN KEY (factory_id) REFERENCES Factories(factory_id)
#             );
#         '''
#     sql_create_fac_purchases_table='''
#                     CREATE TABLE IF NOT EXISTS Fac_Purchases (
#                         purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         purchas_date TEXT NOT NULL ,
#                         fac_money_before REAL DEFAULT 0 CHECK (fac_money_before >= 0),
#                         factory_id INTEGER NOT NULL,
#                         FOREIGN KEY (factory_id) REFERENCES Factories(factory_id)
#                     );
#                 '''
#     sql_create_fac_purchases_items_table='''
#                     CREATE TABLE IF NOT EXISTS Fac_PurchaseItems (
#                         purchase_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         purchase_id INTEGER NOT NULL,
#                         product_id INTEGER NOT NULL,
#                         quantity INTEGER NOT NULL CHECK (quantity >= 0),
#                         price_per_piece REAL NOT NULL CHECK (price_per_piece >= 0),
#                         discount_per_piece REAL DEFAULT 0 CHECK (discount_per_piece >= 0),
#                         resource_name TEXT NOT NULL check (resource_name == 'golden rose' or resource_name == 'snow white'),
#                         FOREIGN KEY (purchase_id) REFERENCES Fac_Purchases(purchase_id) ON DELETE CASCADE,
#                         FOREIGN KEY (product_id) REFERENCES Products(product_id)
#                     );
#                         '''
#     sql_create_fac_returned_items_table = '''
#                     CREATE TABLE IF NOT EXISTS Fac_Returned_Items (
#                         returned_process_id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         date TEXT NOT NULL ,
#                         product_id INTEGER NOT NULL,
#                         quantity INTEGER NOT NULL CHECK (quantity >= 0),
#                         price_per_piece REAL NOT NULL CHECK (price_per_piece >= 0),
#                         factory_id INTEGER NOT NULL,
#                         FOREIGN KEY (factory_id) REFERENCES Factories(factory_id) ,
#                         FOREIGN KEY (product_id) REFERENCES Products(product_id)
#                     );
#                     '''
#     sql_create_customers_table= '''
#             CREATE TABLE IF NOT EXISTS Customers (
#                 customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 name TEXT NOT NULL UNIQUE,
#                 Golden_Rose_amount_money REAL DEFAULT 0 CHECK (Golden_Rose_amount_money >= 0),
#                 Golden_Rose_current_quantity INTEGER DEFAULT 0 CHECK (Golden_Rose_current_quantity >= 0),
#                 Snow_White_amount_money REAL DEFAULT 0 CHECK (Snow_White_amount_money >= 0),
#                 Snow_White_current_quantity INTEGER DEFAULT 0 CHECK (Snow_White_current_quantity >= 0)
#             );
#         '''
#     sql_create_customers_pays_table = '''
#             CREATE TABLE IF NOT EXISTS Cus_Pays (
#                 pay_id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 date TEXT NOT NULL ,
#                 amount_money REAL NOT NULL,
#                 customer_id INTEGER NOT NULL,
#                 resource_name TEXT NOT NULL check (resource_name == 'golden rose' or resource_name == 'snow white'),
#                 safe_money_before REAL DEFAULT 0 CHECK (safe_money_before >= 0),
#                 safe_id INTEGER NOT NULL,
#                 customer_money_before REAL DEFAULT 0 CHECK (customer_money_before >= 0),
#                 customer_money_after REAL DEFAULT 0 CHECK (customer_money_after >= 0),
#                 FOREIGN KEY (safe_id) REFERENCES Safe(safe_id),
#                 FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
#                 );
#             '''
#     sql_create_customers_purchases_table ='''
#                         CREATE TABLE IF NOT EXISTS Cus_Purchases (
#                             purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
#                             purchase_date TEXT NOT NULL ,
#                             discount_Total REAL DEFAULT 0 CHECK (discount_Total >= 0),
#                             resource_name TEXT NOT NULL check (resource_name == 'golden rose' or resource_name == 'snow white'),
#                             cus_money_before REAL DEFAULT 0 CHECK (cus_money_before >= 0),
#                             customer_id INTEGER NOT NULL,
#                             FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
#                         );'''
#     sql_create_customers_purchases_items_table ='''
#                     CREATE TABLE IF NOT EXISTS Cus_PurchaseItems (
#                         purchase_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         purchase_id INTEGER NOT NULL,
#                         product_id INTEGER NOT NULL,
#                         quantity INTEGER NOT NULL CHECK (quantity >= 0),
#                         price_per_piece REAL NOT NULL CHECK (price_per_piece >= 0),
#                         discount_per_piece REAL DEFAULT 0 CHECK (discount_per_piece >= 0),
#                         FOREIGN KEY (purchase_id) REFERENCES Cus_Purchases(purchase_id) ON DELETE CASCADE,
#                         FOREIGN KEY (product_id) REFERENCES Products(product_id)
#                     );'''
#     sql_create_customers_returned_items_table = '''
#                     CREATE TABLE IF NOT EXISTS Cus_Returned_Items (
#                         returned_process_id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         date TEXT NOT NULL ,
#                         product_id INTEGER NOT NULL,
#                         quantity INTEGER NOT NULL CHECK (quantity >= 0),
#                         price_per_piece REAL NOT NULL CHECK (price_per_piece >= 0),
#                         discount_per_piece REAL DEFAULT 0 CHECK (discount_per_piece >= 0),
#                         resource_name TEXT NOT NULL check (resource_name == 'golden rose' or resource_name == 'snow white'),
#                         customer_id INTEGER NOT NULL,
#                         FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ,
#                         FOREIGN KEY (product_id) REFERENCES Products(product_id)
#                     );'''
#     sql_create_notification_table = '''
#                     CREATE TABLE IF NOT EXISTS Notifications (
#                         notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         header TEXT NOT NULL ,
#                         message TEXT NOT NULL ,
#                         date TEXT NOT NULL
#                         );
#                     '''

#     try:
#         # Create tables in order of dependency
#         cursor.execute(sql_create_safe_table)
#         cursor.execute(sql_create_factories_table)
#         cursor.execute(sql_create_products_table)
#         cursor.execute(sql_create_customers_table)
#         cursor.execute(sql_create_notification_table)
#         cursor.execute(sql_create_fac_pays_table)
#         cursor.execute(sql_create_fac_purchases_table)
#         cursor.execute(sql_create_fac_purchases_items_table)
#         cursor.execute(sql_create_fac_returned_items_table)
#         cursor.execute(sql_create_customers_pays_table)
#         cursor.execute(sql_create_customers_purchases_table)
#         cursor.execute(sql_create_customers_purchases_items_table)
#         cursor.execute(sql_create_customers_returned_items_table)
#         conn.commit()
#         print("All tables created successfully (if they didn't exist).")
#     except Error as e:
#         print(f"Error creating tables: {e}")
#         conn.rollback()

# if __name__ == '__main__':
#     database = "IMS.db" # You can change the database file name

#     # Create a database connection
#     conn = create_connection(database)

#     if conn:
#         # Create tables (only if they don't exist, as per your request)
#         print("Ensuring tables exist and foreign keys are enabled...")
#         create_tables(conn)

#         # Insert sample data
#         insert_sample_data(conn)

#         # Optional: Verify data insertion by querying a table
#         try:
#             cursor = conn.cursor()
#             cursor.execute("SELECT * FROM Safe")
#             rows = cursor.fetchall()
#             print("\nData in Safe table:")
#             for row in rows:
#                 print(row)

#             cursor.execute("SELECT * FROM Customers")
#             rows = cursor.fetchall()
#             print("\nData in Customers table:")
#             for row in rows:
#                 print(row)

#             cursor.execute("SELECT name, product_quantity FROM Factories")
#             rows = cursor.fetchall()
#             print("\nData in Factories table (name, product_quantity):")
#             for row in rows:
#                 print(row)

#             cursor.execute("SELECT purchase_id, product_id, quantity FROM Fac_PurchaseItems")
#             rows = cursor.fetchall()
#             print("\nData in Fac_PurchaseItems table (purchase_id, product_id, quantity):")
#             for row in rows:
#                 print(row)

#         except Error as e:
#             print(f"Error verifying data: {e}")
#         finally:
#             conn.close()
#     else:
#         print("Failed to create database connection.")