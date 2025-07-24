import sqlite3
import datetime

class DashboardModel:
    def __init__(self):
        self.conn = sqlite3.connect('IMS.db')
        self.cursor = self.conn.cursor()
        
        
        

    def get_product_sales_by_period(self, period_type: str, supplier) -> list[tuple[str, int]]:
        """
        Retrieves the total sales quantity for each product within a specified period,
        including sales up to the current second of today.

        Args:
            period_type (str): The period type. Must be one of 'اسبوعيا', 'شهريا', 'سنويا'.
            supplier (str): The name of the resource/supplier.

        Returns:
            list[tuple[str, int]]: A list of tuples, where each tuple contains
                                    (product_type, total_sales_quantity),
                                    sorted by total_sales_quantity in descending order.
        """
        current_datetime = datetime.datetime.now()
        
        start_date_period = None # هنستخدمها لتحديد بداية الفترة (أسبوع، شهر، سنة)

        if period_type == 'اسبوعيا':
            start_date_period = current_datetime - datetime.timedelta(days=current_datetime.weekday())
            start_date_period = start_date_period.replace(hour=0, minute=0, second=0, microsecond=0)
            
        elif period_type == 'شهريا':
            start_date_period = current_datetime.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            
        elif period_type == 'سنويا':
            start_date_period = current_datetime.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            
        else:
            print("Invalid period_type. Please use 'اسبوعيا', 'شهريا', or 'سنويا'.")
            return []

        start_of_today = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        
        start_date_query = start_date_period 

        start_date_str = start_date_query.strftime('%Y-%m-%d %H:%M:%S')
        end_date_str = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

        
        sales_data = []
        try:
            query = """
            SELECT
                P.type,
                COALESCE(SUM(CPI.quantity), 0) AS total_quantity_sold
            FROM
                Products AS P
            LEFT JOIN
                Cus_PurchaseItems AS CPI ON P.product_id = CPI.product_id
            LEFT JOIN
                Cus_Purchases AS CP ON CPI.purchase_id = CP.purchase_id
            WHERE
                P.resource_name = ?
                AND (CP.purchase_date BETWEEN ? AND ? OR CP.purchase_date IS NULL)
            GROUP BY
                P.type
            ORDER BY
                total_quantity_sold DESC;
            """
            self.cursor.execute(query, (supplier, start_date_str, end_date_str ))
            sales_data = self.cursor.fetchall()

        except sqlite3.Error as e:
            print(f"An SQLite error occurred during database query: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        return sales_data






    def get_profit(self, period_type, supplier):
        """
        Retrieves a financial summary (Purchases, Sales, Additional Costs, Total)
        for a specified period and resource name, up to the current second.

        Args:
            period_type (str): The period type. Must be one of 'اسبوعيا', 'شهريا', 'سنويا'.
            supplier (str): The resource name to filter by ('golden rose' or 'snow white').

        Returns:
            list[tuple[str, float]]: A list of 4 tuples, each containing
                                     (Operation Type, Amount).
        """
        # بجيب التاريخ والوقت الحالي بالثانية
        current_datetime = datetime.datetime.now()
        start_date = None

        if period_type == 'اسبوعيا':
            # بداية الأسبوع (الإثنين) الساعة 00:00:00
            start_date = current_datetime - datetime.timedelta(days=current_datetime.weekday())
            start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period_type == 'شهريا':
            # بداية الشهر (يوم 1) الساعة 00:00:00
            start_date = current_datetime.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        elif period_type == 'سنويا':
            # بداية السنة (يوم 1 شهر 1) الساعة 00:00:00
            start_date = current_datetime.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            print("Invalid period_type. Please use 'اسبوعيا', 'شهريا', or 'سنويا'.")
            return []

        if supplier not in ['golden rose', 'snow white']:
            print("Invalid resource_name. Please use 'golden rose' or 'snow white'.")
            return []

        # تنسيق التواريخ لتشمل الوقت بالثواني
        start_date_str = start_date.strftime('%Y-%m-%d %H:%M:%S')
        end_date_str = current_datetime.strftime('%Y-%m-%d %H:%M:%S') # حتى هذه الثانية بالظبط

        purchase_cost = 0.0
        sales_revenue = 0.0
        additional_costs = 0.0
        
        try:
            # 1. Calculate total purchase cost (from Fac_PurchaseItems)
            purchase_query = """
            SELECT SUM(T1.quantity * T1.price_per_piece)
            FROM Fac_PurchaseItems AS T1
            JOIN Fac_Purchases AS T2 ON T1.purchase_id = T2.purchase_id
            WHERE T2.purchas_date BETWEEN ? AND ? AND T1.resource_name = ?;
            """
            self.cursor.execute(purchase_query, (start_date_str, end_date_str, supplier))
            result = self.cursor.fetchone()[0]
            purchase_cost = result if result is not None else 0.0

            # 2. Calculate total sales revenue (from Cus_PurchaseItems)
            sales_query = """
            SELECT SUM(T1.quantity * T1.price_per_piece)
            FROM Cus_PurchaseItems AS T1
            JOIN Cus_Purchases AS T2 ON T1.purchase_id = T2.purchase_id
            JOIN Products AS P ON T1.product_id = P.product_id
            WHERE T2.purchase_date BETWEEN ? AND ? AND P.resource_name = ?;
            """
            self.cursor.execute(sales_query, (start_date_str, end_date_str, supplier))
            result = self.cursor.fetchone()[0]
            sales_revenue = result if result is not None else 0.0

            # 3. Calculate total additional costs (from Additional_Costs)
            additional_costs_query = """
            SELECT SUM(amount_of_money)
            FROM Additional_Costs
            WHERE date BETWEEN ? AND ?;
            """
            self.cursor.execute(additional_costs_query, (start_date_str, end_date_str))
            result = self.cursor.fetchone()[0]
            additional_costs = result if result is not None else 0.0

        except sqlite3.Error as e:
            print(f"An SQLite error occurred during database query: {e}")
            return []
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return []

        # 4. Calculate the total (Sales - (Purchases + Additional Costs))
        total_balance = sales_revenue - (purchase_cost + additional_costs)

        summary = [
            ("الشراء", round(purchase_cost, 2)),
            ("البيع", round(sales_revenue, 2)),
            ("التكاليف الاضافية", round(additional_costs, 2)),
            ("المجموع", round(total_balance, 2))
        ]
        
        return summary