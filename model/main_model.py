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


    # def add_fake_data(self, filename):
    #     conn = sqlite3.connect(filename)
    #     cursor = conn.cursor()

    #     # بيانات ثابتة باللغة العربية
    #     factory_names = ["مصنع الأمل", "مصنع النور", "مصنع الحياة", "مصنع التقدم", "مصنع الريادة"]
    #     customer_names = ["أحمد علي", "سارة محمد", "محمود حسن", "ليلى إبراهيم", "خالد سمير"]
    #     product_types = ["صنف 1", "صنف 2", "صنف 3", "صنف 4", "صنف 5", "صنف 6"]
    #     resource_names = ['golden rose', 'snow white']
    #     safe_types = ["خزنة رئيسية", "خزنة فرعية"]

    #     # إدخال خزنة
    #     for stype in safe_types:
    #         amount = round(random.uniform(10000, 50000), 2)
    #         cursor.execute("INSERT INTO Safe (type, amount_money) VALUES (?, ?)", (stype, amount))

    #     # إدخال المصانع
    #     for name in factory_names:
    #         amount_money = round(random.uniform(1000, 5000), 2)
    #         quantity = random.randint(100, 300)
    #         cursor.execute('''
    #             INSERT INTO Factories (name, amount_money, current_quantity)
    #             VALUES (?, ?, ?)
    #         ''', (name, amount_money, quantity))

    #     # إدخال العملاء
    #     for name in customer_names:
    #         gr_money = round(random.uniform(500, 3000), 2)
    #         gr_qty = random.randint(50, 300)
    #         sw_money = round(random.uniform(500, 3000), 2)
    #         sw_qty = random.randint(50, 300)
    #         cursor.execute('''
    #             INSERT INTO Customers (name, Golden_Rose_amount_money, Golden_Rose_current_quantity,
    #                                 Snow_White_amount_money, Snow_White_current_quantity)
    #             VALUES (?, ?, ?, ?, ?)
    #         ''', (name, gr_money, gr_qty, sw_money, sw_qty))

    #     # إدخال منتجات
    #     for i, ptype in enumerate(product_types):
    #         quantity = random.randint(50, 200)
    #         cus_price = round(random.uniform(5, 20), 2)
    #         fac_price = round(random.uniform(3, 15), 2)
    #         res = random.choice(resource_names)
    #         cursor.execute('''
    #             INSERT INTO Products (type, current_quantity, cus_price_per_piece,
    #                                 fac_price_per_piece, resource_name)
    #             VALUES (?, ?, ?, ?, ?)
    #         ''', (ptype, quantity, cus_price, fac_price, res))

    #     # جلب المعرفات
    #     cursor.execute("SELECT factory_id FROM Factories")
    #     factory_ids = [row[0] for row in cursor.fetchall()]
    #     cursor.execute("SELECT customer_id FROM Customers")
    #     customer_ids = [row[0] for row in cursor.fetchall()]
    #     cursor.execute("SELECT safe_id FROM Safe")
    #     safe_ids = [row[0] for row in cursor.fetchall()]

    #     # إدخال دفعات للمصانع
    #     for _ in range(10):
    #         fid = random.choice(factory_ids)
    #         sid = random.choice(safe_ids)
    #         amount = round(random.uniform(500, 2000), 2)
    #         fac_before = round(random.uniform(1000, 3000), 2)
    #         date = datetime.date.today() - datetime.timedelta(days=random.randint(0, 30))
    #         cursor.execute('''
    #             INSERT INTO Fac_Pays (date, amount_money, factory_id, fac_money_before, safe_id)
    #             VALUES (?, ?, ?, ?, ?)
    #         ''', (str(date), amount, fid, fac_before, sid))

    #     # إدخال دفعات للعملاء
    #     for _ in range(10):
    #         cid = random.choice(customer_ids)
    #         sid = random.choice(safe_ids)
    #         amount = round(random.uniform(300, 1500), 2)
    #         res_name = random.choice(resource_names)
    #         safe_before = round(random.uniform(5000, 10000), 2)
    #         cus_before = round(random.uniform(1000, 3000), 2)
    #         cus_after = cus_before + amount
    #         date = datetime.date.today() - datetime.timedelta(days=random.randint(0, 30))
    #         cursor.execute('''
    #             INSERT INTO Cus_Pays (date, amount_money, customer_id, resource_name, safe_money_before,
    #                                 safe_id, customer_money_before, customer_money_after)
    #             VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    #         ''', (str(date), amount, cid, res_name, safe_before, sid, cus_before, cus_after))

    #     conn.commit()
    #     conn.close()
