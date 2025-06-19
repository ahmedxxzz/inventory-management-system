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
        sql_create_products_table = """
        CREATE TABLE IF NOT EXISTS Products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            colors TEXT,
            current_quantity INTEGER NOT NULL DEFAULT 0,
            low_stock_threshold INTEGER NOT NULL DEFAULT 5,
            average_cost_price REAL NOT NULL DEFAULT 0.0,
            default_sale_price REAL NOT NULL DEFAULT 0.0,
            main_factory_id INTEGER NULLABLE,
            FOREIGN KEY (main_factory_id) REFERENCES Factories(factory_id) ON DELETE SET NULL
        );"""

        sql_create_factories_table = """
        CREATE TABLE IF NOT EXISTS Factories (
            factory_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            location TEXT,
            contact_person TEXT,
            phone TEXT,
            email TEXT,
            balance REAL NOT NULL DEFAULT 0.0
        );"""

        sql_create_suppliers_table = """
        CREATE TABLE IF NOT EXISTS Suppliers (
            supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            contact_person TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            balance REAL NOT NULL DEFAULT 0.0
        );"""

        sql_create_purchases_table = """
        CREATE TABLE IF NOT EXISTS Purchases (
            purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
            supplier_id INTEGER NOT NULL,
            invoice_number TEXT UNIQUE NOT NULL,
            purchase_date TEXT NOT NULL,
            total_amount REAL NOT NULL DEFAULT 0.0,
            amount_paid REAL NOT NULL DEFAULT 0.0,
            status TEXT NOT NULL DEFAULT 'unpaid' CHECK(status IN ('unpaid', 'partially_paid', 'paid', 'cancelled')),
            notes TEXT,
            FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id) ON DELETE RESTRICT
        );"""

        sql_create_purchase_items_table = """
        CREATE TABLE IF NOT EXISTS PurchaseItems (
            purchase_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            purchase_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            cost_price_per_unit REAL NOT NULL,
            total_cost REAL NOT NULL,
            FOREIGN KEY (purchase_id) REFERENCES Purchases(purchase_id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE RESTRICT
        );"""

        sql_create_customers_table = """
        CREATE TABLE IF NOT EXISTS Customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT UNIQUE,
            email TEXT,
            address TEXT,
            balance REAL NOT NULL DEFAULT 0.0,
            credit_limit REAL DEFAULT 0.0,
            payment_terms TEXT,
            alert_debt_threshold REAL NULLABLE
        );"""

        sql_create_sales_table = """
        CREATE TABLE IF NOT EXISTS Sales (
            sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NULLABLE,
            invoice_number TEXT UNIQUE NOT NULL,
            sale_date TEXT NOT NULL,
            total_amount REAL NOT NULL DEFAULT 0.0,
            amount_paid REAL NOT NULL DEFAULT 0.0,
            payment_type TEXT NOT NULL CHECK(payment_type IN ('cash', 'credit')),
            due_date TEXT NULLABLE,
            status TEXT NOT NULL DEFAULT 'unpaid' CHECK(status IN ('unpaid', 'partially_paid', 'paid', 'overdue', 'cancelled')),
            notes TEXT,
            FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE SET NULL
        );"""

        sql_create_sale_items_table = """
        CREATE TABLE IF NOT EXISTS SaleItems (
            sale_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            sale_price_per_unit REAL NOT NULL,
            cost_price_at_sale REAL NOT NULL,
            total_price REAL NOT NULL,
            FOREIGN KEY (sale_id) REFERENCES Sales(sale_id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE RESTRICT
        );"""

        sql_create_factory_deliveries_table = """
        CREATE TABLE IF NOT EXISTS FactoryDeliveries (
            delivery_id INTEGER PRIMARY KEY AUTOINCREMENT,
            factory_id INTEGER NOT NULL,
            document_number TEXT UNIQUE NOT NULL,
            delivery_date TEXT NOT NULL,
            document_type TEXT NOT NULL CHECK(document_type IN ('receipt', 'invoice')),
            total_cost REAL NOT NULL DEFAULT 0.0,
            amount_paid REAL NOT NULL DEFAULT 0.0,
            status TEXT NOT NULL DEFAULT 'unpaid' CHECK(status IN ('unpaid', 'partially_paid', 'paid', 'cancelled')),
            notes TEXT,
            FOREIGN KEY (factory_id) REFERENCES Factories(factory_id) ON DELETE RESTRICT
        );"""

        sql_create_factory_delivery_items_table = """
        CREATE TABLE IF NOT EXISTS FactoryDeliveryItems (
            delivery_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            delivery_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            cost_price_per_unit REAL NOT NULL,
            total_item_cost REAL NOT NULL,
            FOREIGN KEY (delivery_id) REFERENCES FactoryDeliveries(delivery_id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE RESTRICT
        );"""

        sql_create_payments_table = """
        CREATE TABLE IF NOT EXISTS Payments (
            payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            payment_date TEXT NOT NULL,
            amount REAL NOT NULL,
            payment_method TEXT,
            direction TEXT NOT NULL CHECK(direction IN ('inflow', 'outflow')),
            party_type TEXT NOT NULL CHECK(party_type IN ('customer', 'supplier', 'factory')),
            party_id INTEGER NOT NULL,
            related_sale_id INTEGER NULLABLE,
            related_purchase_id INTEGER NULLABLE,
            related_delivery_id INTEGER NULLABLE,
            notes TEXT,
            FOREIGN KEY (related_sale_id) REFERENCES Sales(sale_id) ON DELETE SET NULL,
            FOREIGN KEY (related_purchase_id) REFERENCES Purchases(purchase_id) ON DELETE SET NULL,
            FOREIGN KEY (related_delivery_id) REFERENCES FactoryDeliveries(delivery_id) ON DELETE SET NULL
        );"""
        # Note: party_id will be programmatically linked to Customers, Suppliers, or Factories tables.

        sql_create_returns_table = """
        CREATE TABLE IF NOT EXISTS Returns (
            return_id INTEGER PRIMARY KEY AUTOINCREMENT,
            return_date TEXT NOT NULL,
            return_type TEXT NOT NULL CHECK(return_type IN ('sale_return', 'purchase_return')),
            original_sale_id INTEGER NULLABLE,
            original_purchase_id INTEGER NULLABLE,
            customer_id INTEGER NULLABLE,
            supplier_id INTEGER NULLABLE,
            reason_category TEXT,
            reason_details TEXT,
            total_value REAL NOT NULL DEFAULT 0.0,
            notes TEXT,
            FOREIGN KEY (original_sale_id) REFERENCES Sales(sale_id) ON DELETE SET NULL,
            FOREIGN KEY (original_purchase_id) REFERENCES Purchases(purchase_id) ON DELETE SET NULL,
            FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE SET NULL,
            FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id) ON DELETE SET NULL
        );"""

        sql_create_return_items_table = """
        CREATE TABLE IF NOT EXISTS ReturnItems (
            return_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            return_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price_at_return REAL NOT NULL,
            total_item_value REAL NOT NULL,
            FOREIGN KEY (return_id) REFERENCES Returns(return_id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE RESTRICT
        );"""

        sql_create_expenses_table = """
        CREATE TABLE IF NOT EXISTS Expenses (
            expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
            expense_date TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            notes TEXT
        );"""

        sql_create_users_table = """
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            full_name TEXT,
            is_active INTEGER NOT NULL DEFAULT 1
        );"""
        
        sql_create_stock_movements_table = """
        CREATE TABLE IF NOT EXISTS StockMovements (
            movement_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            movement_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            movement_type TEXT NOT NULL CHECK(movement_type IN (
                'purchase', 'sale', 'sale_return', 'purchase_return', 
                'factory_delivery', 'stock_adjustment_in', 'stock_adjustment_out', 
                'initial_stock'
            )),
            quantity_change INTEGER NOT NULL,
            reference_id INTEGER NULLABLE,
            reference_table TEXT NULLABLE,
            notes TEXT,
            FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE
        );"""

        # Create a database connection
        conn = self.create_connection(database_file)

        # Create tables
        if conn is not None:
            # Order matters due to Foreign Keys (Factories must exist before Products if Products references it)
            self.create_table(conn, sql_create_factories_table)
            self.create_table(conn, sql_create_products_table) # Products references Factories
            self.create_table(conn, sql_create_suppliers_table)
            self.create_table(conn, sql_create_purchases_table) # Purchases references Suppliers
            self.create_table(conn, sql_create_purchase_items_table) # PurchaseItems references Purchases and Products
            self.create_table(conn, sql_create_customers_table)
            self.create_table(conn, sql_create_sales_table) # Sales references Customers
            self.create_table(conn, sql_create_sale_items_table) # SaleItems references Sales and Products
            self.create_table(conn, sql_create_factory_deliveries_table) # FactoryDeliveries references Factories
            self.create_table(conn, sql_create_factory_delivery_items_table) # FactoryDeliveryItems references FactoryDeliveries and Products
            self.create_table(conn, sql_create_payments_table) # Payments references Sales, Purchases, FactoryDeliveries
            self.create_table(conn, sql_create_returns_table) # Returns references Sales, Purchases, Customers, Suppliers
            self.create_table(conn, sql_create_return_items_table) # ReturnItems references Returns and Products
            self.create_table(conn, sql_create_expenses_table)
            self.create_table(conn, sql_create_users_table)
            self.create_table(conn, sql_create_stock_movements_table) # StockMovements references Products

            conn.commit() # Commit changes
            conn.close()
            print(f"Database {database_file} and tables created/verified successfully.")
        else:
            print("Error! Cannot create the database connection.")

