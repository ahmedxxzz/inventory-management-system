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
            self.add_fake_data(db_file)

    


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
                    name TEXT NOT NULL UNIQUE,
                    amount_money REAL DEFAULT 0 CHECK (amount_money >= 0),
                    current_quantity INTEGER DEFAULT 0 CHECK (current_quantity >= 0)
                );
            ''')

            # Create Products table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Products (
                    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT NOT NULL UNIQUE,
                    current_quantity INTEGER DEFAULT 0 CHECK (current_quantity >= 0),
                    cus_price_per_piece REAL DEFAULT 0 CHECK (cus_price_per_piece >= 0),
                    fac_price_per_piece REAL DEFAULT 0 CHECK (fac_price_per_piece >= 0),
                    resource_name TEXT  check (resource_name == 'golden rose' or resource_name == 'snow white')
                );
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Fac_Pays (
                    pay_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL UNIQUE,
                    amount_money REAL NOT NULL,
                    factory_id INTEGER NOT NULL,
                    fac_money_before REAL DEFAULT 0 CHECK (fac_money_before >= 0),
                    safe_id INTEGER NOT NULL,
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
                            date TEXT NOT NULL UNIQUE,
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
                    name TEXT NOT NULL UNIQUE,
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
                                purchase_date TEXT NOT NULL UNIQUE,
                                discount_Total REAL DEFAULT 0 CHECK (discount_Total >= 0),
                                resource_name TEXT NOT NULL check (resource_name == 'golden rose' or resource_name == 'snow white'),
                                cus_money_before REAL DEFAULT 0 CHECK (cus_money_before >= 0),
                                customer_id INTEGER NOT NULL,
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
                            date TEXT NOT NULL UNIQUE,
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

            conn.commit()

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            # Close the connection
            conn.close()


    def add_fake_data(self, filename):
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()
            

        # Helper to generate sequential dates to ensure uniqueness
        def generate_dates(start_date_str, num_records):
            base_time = datetime.datetime.strptime(start_date_str, '%Y-%m-%d %H:%M:%S')
            return [(base_time + datetime.timedelta(days=i, hours=random.randint(1,5), minutes=random.randint(1,59))).strftime('%Y-%m-%d %H:%M:%S') for i in range(num_records)]

        # --- Data Generation ---
        num_records = 10

        # ==============================================================================
        # == FACTORY RELATED DATA
        # ==============================================================================

        # --- Fac_Purchases (10 records) ---
        # Simulates 10 separate purchase orders from our factories.
        fac_purchases_dates = generate_dates('2023-10-01 09:00:00', num_records)
        fac_purchases_data = [
            # (purchas_date, fac_money_before, factory_id)
            (fac_purchases_dates[0], 64000, 3),  # From سعد المجرد (GR)
            (fac_purchases_dates[1], 10000, 2),  # From احمد جمعه (SW)
            (fac_purchases_dates[2], 5000, 1),   # From حمادة طلبة (GR)
            (fac_purchases_dates[3], 4400, 4),   # From هوبا سيد (SW)
            (fac_purchases_dates[4], 64000, 3),  # From سعد المجرد (GR)
            (fac_purchases_dates[5], 10000, 2),  # From احمد جمعه (SW)
            (fac_purchases_dates[6], 5000, 1),   # From حمادة طلبة (GR)
            (fac_purchases_dates[7], 4400, 4),   # From هوبا سيد (SW)
            (fac_purchases_dates[8], 64000, 3),  # From سعد المجرد (GR)
            (fac_purchases_dates[9], 10000, 2),  # From احمد جمعه (SW)
        ]

        # --- Fac_PurchaseItems (More than 10 records to populate the 10 purchases) ---
        # Items associated with the factory purchases above.
        fac_purchase_items_data = [
            # (purchase_id, product_id, quantity, price_per_piece, discount_per_piece, resource_name)
            (1, 1, 50, 180, 10, 'golden rose'),  # p_id 1 is '1001'
            (1, 3, 100, 15, 0, 'golden rose'), # p_id 3 is '1003'
            (2, 2, 80, 30, 2, 'snow white'),   # p_id 2 is '0001'
            (3, 5, 200, 20, 1, 'golden rose'), # p_id 5 is '1004'
            (4, 4, 150, 45, 5, 'snow white'),   # p_id 4 is '0005'
            (5, 7, 30, 85, 0, 'golden rose'),   # p_id 7 is '1008'
            (6, 6, 120, 70, 7, 'snow white'),   # p_id 6 is '0050'
            (7, 9, 250, 5, 0.5, 'golden rose'), # p_id 9 is '1007'
            (8, 8, 400, 220, 20, 'snow white'), # p_id 8 is '0006'
            (9, 11, 60, 130, 15, 'golden rose'),# p_id 11 is '1010'
            (10, 10, 90, 25, 0, 'snow white'),  # p_id 10 is '0010'
            (10, 12, 70, 35, 3, 'snow white'),  # p_id 12 is '0100'
        ]

        # --- Fac_Pays (10 records) ---
        # Simulates 10 payments made to our factories.
        fac_pays_dates = generate_dates('2023-10-15 14:00:00', num_records)
        fac_pays_data = [
            # (date, amount_money, factory_id, fac_money_before, safe_id)
            (fac_pays_dates[0], 20000, 3, 64000, 1), # Pay سعد المجرد from cash
            (fac_pays_dates[1], 5000, 2, 10000, 2),  # Pay احمد جمعه from vodafone cash
            (fac_pays_dates[2], 2500, 1, 5000, 1),   # Pay حمادة طلبة from cash
            (fac_pays_dates[3], 2000, 4, 4400, 2),   # Pay هوبا سيد from vodafone cash
            (fac_pays_dates[4], 30000, 3, 64000, 1), # Pay سعد المجرد from cash
            (fac_pays_dates[5], 4000, 2, 10000, 1),  # Pay احمد جمعه from cash
            (fac_pays_dates[6], 2500, 1, 5000, 2),   # Pay حمادة طلبة from vodafone cash
            (fac_pays_dates[7], 2400, 4, 4400, 1),   # Pay هوبا سيد from cash
            (fac_pays_dates[8], 14000, 3, 64000, 2), # Pay سعد المجرد from vodafone cash
            (fac_pays_dates[9], 1000, 2, 10000, 1),  # Pay احمد جمعه from cash
        ]

        # Simulates returning items to factories.
        fac_returned_dates = generate_dates('2023-10-20 11:00:00', num_records)
        fac_returned_items_data = [
            # (date, product_id, quantity, price_per_piece, factory_id, reason)
            (fac_returned_dates[0], 1, 5, 170, 3, 'علشان عبيط'),     # Return '1001' to سعد المجرد
            (fac_returned_dates[1], 2, 10, 28, 2, 'علشان عبيط'),     # Return '0001' to احمد جمعه
            (fac_returned_dates[2], 5, 15, 19, 1, 'علشان عبيط'),     # Return '1004' to حمادة طلبة
            (fac_returned_dates[3], 4, 8, 40, 4, 'علشان عبيط'),      # Return '0005' to هوبا سيد
            (fac_returned_dates[4], 7, 2, 85, 3, 'علشان عبيط'),      # Return '1008' to سعد المجرد
            (fac_returned_dates[5], 6, 20, 63, 2, 'علشان عبيط'),     # Return '0050' to احمد جمعه
            (fac_returned_dates[6], 9, 30, 4.5, 1, 'علشان عبيط'),    # Return '1007' to حمادة طلبة
            (fac_returned_dates[7], 8, 50, 200, 4, 'علشان عبيط'),    # Return '0006' to هوبا سيد
            (fac_returned_dates[8], 11, 4, 115, 3, 'علشان عبيط'),    # Return '1010' to سعد المجرد
            (fac_returned_dates[9], 10, 7, 25, 2, 'علشان عبيط'),     # Return '0010' to احمد جمعه
        ]


        # ==============================================================================
        # == CUSTOMER RELATED DATA
        # ==============================================================================

        # --- Cus_Purchases (10 records) ---
        # Simulates 10 sales to our customers.
        # Note: discount_Total is calculated from the items below.
        cus_purchases_dates = generate_dates('2023-11-01 10:00:00', num_records)
        cus_purchases_data = [
            # (purchase_date, discount_Total, resource_name, cus_money_before, customer_id)
            (cus_purchases_dates[0], 250, 'golden rose', 7500, 1),  # أحمد حسن (GR) - Discount: 10*25=250
            (cus_purchases_dates[1], 150, 'snow white', 4800, 2),   # فاطمة علي (SW) - Discount: 5*30=150
            (cus_purchases_dates[2], 0, 'golden rose', 2100, 3),    # محمد السيد (GR)
            (cus_purchases_dates[3], 80, 'snow white', 5500, 4),    # نورهان إبراهيم (SW) - Discount: 2*40=80
            (cus_purchases_dates[4], 120, 'golden rose', 2900, 5),  # خالد محمود (GR) - Discount: 12*10=120
            (cus_purchases_dates[5], 90, 'snow white', 4100, 6),    # سارة طارق (SW) - Discount: 3*30=90
            (cus_purchases_dates[6], 0, 'golden rose', 2700, 7),    # يوسف جمال (GR)
            (cus_purchases_dates[7], 500, 'snow white', 6000, 8),   # هنا عادل (SW) - Discount: 10*50=500
            (cus_purchases_dates[8], 150, 'golden rose', 3400, 9),  # عمر مصطفى (GR) - Discount: 5*30=150
            (cus_purchases_dates[9], 100, 'snow white', 4500, 10),  # ليلى فؤاد (SW) - Discount: 10*10=100
        ]

        # --- Cus_PurchaseItems (More than 10 records to populate the 10 purchases) ---
        # Items associated with the customer purchases above.
        cus_purchase_items_data = [
            # (purchase_id, product_id, quantity, price_per_piece, discount_per_piece)
            (1, 1, 10, 250, 25),   # For أحمد حسن (p_id 1 is '1001')
            (2, 2, 5, 50, 30),     # For فاطمة علي (p_id 2 is '0001')
            (3, 3, 20, 25, 0),     # For محمد السيد (p_id 3 is '1003')
            (3, 5, 30, 35, 0),     # For محمد السيد (p_id 5 is '1004')
            (4, 4, 2, 70, 40),     # For نورهان إبراهيم (p_id 4 is '0005')
            (5, 7, 12, 120, 10),   # For خالد محمود (p_id 7 is '1008')
            (6, 6, 3, 100, 30),    # For سارة طارق (p_id 6 is '0050')
            (7, 9, 5, 10, 0),      # For يوسف جمال (p_id 9 is '1007')
            (8, 8, 10, 300, 50),   # For هنا عادل (p_id 8 is '0006')
            (9, 11, 5, 180, 30),   # For عمر مصطفى (p_id 11 is '1010')
            (10, 10, 10, 40, 10),  # For ليلى فؤاد (p_id 10 is '0010')
            (10, 12, 15, 60, 0),   # For ليلى فؤاد (p_id 12 is '0100')
        ]

        # --- Cus_Returned_Items (10 records) ---
        # Simulates customers returning items.
        cus_returned_dates = generate_dates('2023-11-10 16:00:00', num_records)
        cus_returned_items_data = [
            # (date, product_id, quantity, price_per_piece, discount_per_piece, resource_name, customer_id)
            (cus_returned_dates[0], 1, 1, 250, 25, 'golden rose', 1),   # أحمد حسن returns '1001'
            (cus_returned_dates[1], 2, 1, 50, 30, 'snow white', 2),    # فاطمة علي returns '0001'
            (cus_returned_dates[2], 5, 5, 35, 0, 'golden rose', 3),     # محمد السيد returns '1004'
            (cus_returned_dates[3], 4, 1, 70, 40, 'snow white', 4),    # نورهان إبراهيم returns '0005'
            (cus_returned_dates[4], 7, 2, 120, 10, 'golden rose', 5),   # خالد محمود returns '1008'
            (cus_returned_dates[5], 6, 1, 100, 30, 'snow white', 6),    # سارة طارق returns '0050'
            (cus_returned_dates[6], 9, 2, 10, 0, 'golden rose', 7),     # يوسف جمال returns '1007'
            (cus_returned_dates[7], 8, 3, 300, 50, 'snow white', 8),    # هنا عادل returns '0006'
            (cus_returned_dates[8], 11, 1, 180, 30, 'golden rose', 9),  # عمر مصطفى returns '1010'
            (cus_returned_dates[9], 10, 2, 40, 10, 'snow white', 10),   # ليلى فؤاد returns '0010'
        ]

        # --- Cus_Pays (10 records) ---
        # Simulates customers making payments.
        cus_pays_dates = generate_dates('2023-11-20 18:00:00', num_records)
        cus_pays_data = [
            # (date, amount, customer_id, resource_name, safe_money_before, safe_id, cus_money_before, cus_money_after)
            (cus_pays_dates[0], 2000, 1, 'golden rose', 100000, 1, 7500, 5500),  
            (cus_pays_dates[1], 1500, 2, 'snow white', 50000, 2, 4800, 3300),    
            (cus_pays_dates[2], 1000, 3, 'golden rose', 100000, 1, 2100, 1100),  
            (cus_pays_dates[3], 3000, 4, 'snow white', 50000, 2, 5500, 2500),    
            (cus_pays_dates[4], 1200, 5, 'golden rose', 100000, 1, 2900, 1700),  
            (cus_pays_dates[5], 2000, 6, 'snow white', 50000, 2, 4100, 2100),    
            (cus_pays_dates[6], 1500, 7, 'golden rose', 100000, 1, 2700, 1200),  
            (cus_pays_dates[7], 4000, 8, 'snow white', 50000, 2, 6000, 2000),    
            (cus_pays_dates[8], 1800, 9, 'golden rose', 100000, 1, 3400, 1600),  
            (cus_pays_dates[9], 2500, 10, 'snow white', 50000, 2, 4500, 2000),   
        ]


        data_dict = {
            'Factories' : [('حمادة طلبة', 5000, 50),('احمد جمعه', 10000, 100),('سعد المجرد', 64000, 150),('هوبا سيد', 4400, 10)],
            'Products' : [('1001', 75, 250, 180, 'golden rose'),('0001', 120, 50, 30, 'snow white'),('1003', 30, 25, 15, 'golden rose'),('0005', 90, 70, 45, 'snow white'),('1004', 60, 35, 20, 'golden rose'),('0050', 40, 100, 70, 'snow white'),('1008', 55, 120, 85, 'golden rose'),('0006', 20, 300, 220, 'snow white'),('1007', 200, 10, 5, 'golden rose'),('0010', 80, 40, 25, 'snow white'),('1010', 25, 180, 130, 'golden rose'),('0100', 110, 60, 35, 'snow white'),('1011', 150, 20, 12, 'golden rose'),('0150', 15, 400, 300, 'snow white'),('1012', 70, 45, 28, 'golden rose'),('0200', 35, 90, 60, 'snow white'),('1013', 45, 150, 110, 'golden rose'),('0250', 10, 500, 380, 'snow white'),('1017', 95, 30, 18, 'golden rose'),('0300', 50, 200, 150, 'snow white')],
            'Customers' : [('أحمد حسن', 7500, 120, 3200, 65), ('فاطمة علي', 9200, 180, 4800, 90), ('محمد السيد', 5100, 85, 2100, 40),('نورهان إبراهيم', 8800, 150, 5500, 110),('خالد محمود', 6300, 95, 2900, 55),('سارة طارق', 7900, 130, 4100, 75),('يوسف جمال', 5900, 105, 2700, 48),('هنا عادل', 9500, 190, 6000, 120),('عمر مصطفى', 6800, 115, 3400, 60),('ليلى فؤاد', 8200, 140, 4500, 80),('عمرو وائل', 7100, 125, 3000, 62),('مريم عماد', 9000, 170, 5200, 100),('مصطفى سمير', 5400, 90, 2300, 45),('دنيا هاني', 8600, 160, 5000, 95),('زياد شريف', 6600, 110, 3100, 58),('روان هشام', 8400, 145, 4700, 85),('كريم رضا', 7300, 135, 3600, 70),('ملك أشرف', 9100, 175, 5300, 105),('تامر سعيد', 6000, 100, 2500, 50),('سلمى أيمن', 8700, 155, 4900, 92)],
            'Safe' : [('cash', '100000'), ('vodafone cash', '50000')],
            'Fac_Purchases' : fac_purchases_data ,
            'Fac_PurchaseItems' : fac_purchase_items_data,
            'Fac_Pays' : fac_pays_data ,
            'Fac_Returned_Items' : fac_returned_items_data ,
            'Cus_Pays' : cus_pays_data,
            'Cus_Returned_Items' : cus_returned_items_data,
            'Cus_Purchases' : cus_purchases_data,
            'Cus_PurchaseItems' : cus_purchase_items_data            
        }
        sql_insert_statements = {
        'Factories': "INSERT INTO Factories (name, amount_money, current_quantity) VALUES (?, ?, ?);",
        'Products': "INSERT INTO Products (type, current_quantity, cus_price_per_piece, fac_price_per_piece, resource_name) VALUES (?, ?, ?, ?, ?);",
        'Customers': "INSERT INTO Customers (name, Golden_Rose_amount_money, Golden_Rose_current_quantity, Snow_White_amount_money, Snow_White_current_quantity) VALUES (?, ?, ?, ?, ?);",
        'Safe': "INSERT INTO Safe (type, amount_money) VALUES (?, ?);",
        'Fac_Purchases': "INSERT INTO Fac_Purchases (purchas_date, fac_money_before, factory_id) VALUES (?, ?, ?);",
        'Fac_PurchaseItems': "INSERT INTO Fac_PurchaseItems (purchase_id, product_id, quantity, price_per_piece, discount_per_piece, resource_name) VALUES (?, ?, ?, ?, ?, ?);",
        'Fac_Pays': "INSERT INTO Fac_Pays (date, amount_money, factory_id, fac_money_before, safe_id) VALUES (?, ?, ?, ?, ?);",
        'Fac_Returned_Items': "INSERT INTO Fac_Returned_Items (date, product_id, quantity, price_per_piece, factory_id, reason) VALUES (?, ?, ?, ?, ?, ?);",
        'Cus_Purchases': "INSERT INTO Cus_Purchases (purchase_date, discount_Total, resource_name, cus_money_before, customer_id) VALUES (?, ?, ?, ?, ?);",
        'Cus_PurchaseItems': "INSERT INTO Cus_PurchaseItems (purchase_id, product_id, quantity, price_per_piece, discount_per_piece) VALUES (?, ?, ?, ?, ?);",
        'Cus_Returned_Items': "INSERT INTO Cus_Returned_Items (date, product_id, quantity, price_per_piece, discount_per_piece, resource_name, customer_id) VALUES (?, ?, ?, ?, ?, ?, ?);",
        'Cus_Pays': "INSERT INTO Cus_Pays (date, amount_money, customer_id, resource_name, safe_money_before, safe_id, customer_money_before, customer_money_after) VALUES (?, ?, ?, ?, ?, ?, ?, ?);"
    }
        insertion_order = [
        'Safe', 'Factories', 'Products', 'Customers',
        'Fac_Purchases', 'Cus_Purchases',
        'Fac_PurchaseItems', 'Cus_PurchaseItems',
        'Fac_Pays', 'Fac_Returned_Items',
        'Cus_Pays', 'Cus_Returned_Items'
    ]

        print("\nStarting data insertion...")
        for table_name in insertion_order:
            if table_name in data_dict and table_name in sql_insert_statements:
                try:
                    records_to_insert = data_dict[table_name]
                    sql = sql_insert_statements[table_name]
                    cursor.executemany(sql, records_to_insert)
                    print(f"  - Successfully inserted {len(records_to_insert)} records into {table_name}.")
                except sqlite3.Error as e:
                    print(f"  - ERROR inserting into {table_name}: {e}")
                    # Optional: Stop execution if an error occurs
                    return False 
        conn.commit()
        
        return True


