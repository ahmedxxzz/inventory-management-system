import sqlite3
import os
from datetime import datetime, date, timedelta


class MainModel:

    def __init__(self):
        db_file = "IMS.db"
        if os.path.exists(db_file):
            print(f"Database {db_file} already exists. Skipping database setup.")
            self.conn = sqlite3.connect(db_file)
            self.cursor = self.conn.cursor()
        else :
            print(f"Database {db_file} isn't exists. Setting up database.")
            self.conn = sqlite3.connect(db_file)
            self.cursor = self.conn.cursor()
            self.create_tables()
    


    def create_tables(self):
        try:

            # Connect to SQLite database
            conn = self.conn
            cursor = self.cursor

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


            cursor.execute('''
                        CREATE TABLE IF NOT EXISTS Notifications (
                            notification_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            type TEXT NOT NULL ,-- type of notification ('snow_cus_unpaid', 'golden_cus_unpaid','snow_cus_overdue', 'golden_cus_overdue', 'snow_product', 'golden_product', 'factory_no_work')
                            seen boolean DEFAULT 0,
                            entity_id INTEGER NOT NULL,
                            message TEXT NOT NULL
                        );
                        ''')

            conn.commit()

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            self.conn.close()



    def check_notifications(self,):
        self.set_customer_not_paid()
        self.set_facs_no_work()


    def set_customer_not_paid(self):
        cuss_not_paid = self.get_customer_not_paid()
        for customer in cuss_not_paid:
            if customer['resource_name'] == 'golden rose':
                notification_type = 'golden_cus_unpaid'
                
            elif customer['resource_name'] == 'snow white':
                notification_type = 'snow_cus_unpaid'
            
            self.cursor.execute("Select message FROM Notifications Where type = ? AND entity_id = ?", (notification_type, customer['customer_id'],)) # check if the notification already exists
            message = self.cursor.fetchone()[0]
            if message is None:
                message = f"المكتب {self.get_cus_name_by_id(customer['customer_id'])} لم يدفع  ل {customer['resource_name']} لمدة {customer['difference']//7} اسبوع"
                self.cursor.execute("INSERT INTO Notifications (type, seen, entity_id, message) VALUES (?, ?, ?, ?)", (notification_type, 0, customer['customer_id'], message))
                self.conn.commit()
            else:
                weeks_number = int(message.split(' ')[-2])
                if customer['difference']//7 > weeks_number:
                    message = f"المكتب {self.get_cus_name_by_id(customer['customer_id'])} لم يدفع  ل {customer['resource_name']} لمدة {customer['difference']//7} اسبوع"
                    self.cursor.execute("UPDATE Notifications SET seen=0, message = ? WHERE type = ? AND entity_id = ?", (message, notification_type, customer['customer_id'],))
                    self.conn.commit()


    def get_cus_name_by_id(self, customer_id):
        self.cursor.execute("SELECT name FROM Customers WHERE customer_id = ?", (customer_id,))
        return self.cursor.fetchone()[0]


    def get_customer_not_paid(self,):
        self.cursor.execute('''SELECT customer_id, resource_name, MAX(date) AS last_payment_date FROM Cus_Pays GROUP BY customer_id, resource_name;''')
        last_payment = self.cursor.fetchall() # for each customer and resource name, get the last payment date [(customer_id, resource_name, last_payment_date), ...]
        today = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), "%Y-%m-%d").date()
        cuss_not_paid = []
        for customer in last_payment:
            pay_day = datetime.strptime(customer[2], "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d').date() # convert to object and then to year-month-day
            difference = today - pay_day

            if difference.days >= 7:
                cuss_not_paid.append(
                    {
                        'customer_id': customer[0],
                        'resource_name': customer[1],
                        'last_payment_date': customer[2],
                        'difference': difference.days
                    }
                )
        return cuss_not_paid


    def set_facs_no_work(self):
        facs_no_work = self.get_facs_no_work()
        for fac in facs_no_work:

            self.cursor.execute("Select message FROM Notifications Where type = 'factory_no_work' AND entity_id = ?", ( fac['factory_id'],)) # check if the notification already exists
            message = self.cursor.fetchone()[0]
            if message is None:
                message = f"المصنع {self.get_factory_name_byid(fac['factory_id'])} لم يعمل لمدة {fac['difference']//7} اسبوع"
                
                self.cursor.execute("INSERT INTO Notifications (type, seen, entity_id, message) VALUES (?, ?, ?, ?)", ('factory_no_work', 0, fac['factory_id'], message))
                self.conn.commit()
            else:
                weeks_number = int(message.split(' ')[-2])
                if fac['difference']//7 > weeks_number:
                    message = f"المصنع {self.get_factory_name_byid(fac['factory_id'])} لم يعمل لمدة {fac['difference']//7} اسبوع"
                    self.cursor.execute("UPDATE Notifications SET seen=0, message = ? WHERE type = 'factory_no_work' AND entity_id = ?", (message, fac['factory_id'],))
                    self.conn.commit()

    def get_factory_name_byid(self, factory_id):
        self.cursor.execute("SELECT name FROM Factories WHERE factory_id = ?", (factory_id,))
        return self.cursor.fetchone()[0]

    def get_facs_no_work(self):
        self.cursor.execute('''SELECT factory_id, MAX(purchas_date) AS last_payment_date FROM Fac_Purchases GROUP BY factory_id;''')
        last_payment = self.cursor.fetchall() # for each factory and resource name, get the last payment date [(factory_id, last_payment_date), ...]
        today = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), "%Y-%m-%d").date()
        facs_no_work = []
        for factory in last_payment:
            pay_day = datetime.strptime(factory[1], "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d').date() # convert to object and then to year-month-day
            difference = today - pay_day

            if difference.days >= 7:
                facs_no_work.append(
                    {
                        'factory_id': factory[0],
                        'last_payment_date': factory[1],
                        'difference': difference.days
                    }
                )
        return facs_no_work

