import datetime   

class InventoryDashboardModel:
    def __init__(self, db_conn):
        self.conn = db_conn
        self.cursor = self.conn.cursor()


    def get_distributors(self):
        self.cursor.execute("SELECT name FROM Distributor")
        distributors = self.cursor.fetchall() # = [(name1,), (name2,), ...]
        distributors_list_names = [distributor[0] for distributor in distributors]
        return distributors_list_names # = [name1, name2, ...]


    def get_product_sales_by_period(self, period_type: str, distributor) -> list[tuple[str, int]]:
        """
        Retrieves the total sales quantity for each product within a specified period,
        including sales up to the current second of today.

        Args:
            period_type (str): The period type. Must be one of 'اسبوعيا', 'شهريا', 'سنويا'.
            distributor (str): The name of the distributor.

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

        
        start_date_query = start_date_period 
        start_date_str = start_date_query.strftime('%Y-%m-%d %H:%M:%S')
        end_date_str = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

        
        sales_data = []
        try:
            distributor_id = None
            if distributor != 'الجميع':
                distributor_id = self.cursor.execute("SELECT distributor_id FROM Distributor WHERE name = ?", (distributor,)).fetchone()[0]
            distributor_filter = "CSB.distributor_id = ?" if distributor_id is not None else "1=1"

            query = f"""
            SELECT
                P.name,
                COALESCE(SUM(CSBI.quantity), 0) AS total_quantity_sold
            FROM
                Product AS P
            LEFT JOIN
                Customer_Sales_Bill_Items AS CSBI ON P.product_id = CSBI.product_id
            LEFT JOIN
                Customer_Sales_Bills AS CSB ON CSBI.sales_bill_id = CSB.sales_bill_id
            WHERE
                {distributor_filter}
                AND CSB.date BETWEEN ? AND ?
            GROUP BY
                P.product_id, P.name
            ORDER BY
                total_quantity_sold DESC;
            """
            if distributor_id is not None:
                params = (distributor_id, start_date_str, end_date_str)
            else:
                params = (start_date_str, end_date_str)
            self.cursor.execute(query, params)
            sales_data = self.cursor.fetchall()


        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        return sales_data


    def get_profit(self, period_type, distributor):
        """
        Retrieves a financial summary (Purchases, Sales, Additional Costs, Total)
        for a specified period and distributor name, up to the current second.

        Args:
            period_type (str): The period type. Must be one of 'اسبوعيا', 'شهريا', 'سنويا'.
            distributor (str): The distributor name .

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


        # تنسيق التواريخ لتشمل الوقت بالثواني
        start_date_str = start_date.strftime('%Y-%m-%d %H:%M:%S')
        end_date_str = current_datetime.strftime('%Y-%m-%d %H:%M:%S') # حتى هذه الثانية بالظبط

        purchase_cost = 0.0
        sales_revenue = 0.0
        additional_costs = 0.0
        
        try:
            # 1. Calculate total purchase cost (from Fac_PurchaseItems)
            distributor_id = None
            if distributor != 'الجميع':
                distributor_id = self.cursor.execute("SELECT distributor_id FROM Distributor WHERE name = ?", (distributor,)).fetchone()[0]
            purchase_query = """
            SELECT COALESCE(SUM(total_amount), 0.0)
            FROM Factory_Purchases_Bills
            WHERE date BETWEEN ? AND ?;
            """
            self.cursor.execute(purchase_query, (start_date_str, end_date_str))
            result = self.cursor.fetchone()[0]
            purchase_cost = result if result is not None else 0.0

            # 2. Calculate total sales revenue (from Cus_PurchaseItems)
            if distributor_id is not None:
                sales_filter = "AND distributor_id = ?"
                sales_params = (start_date_str, end_date_str, distributor_id)
            else:
                sales_filter = ""
                sales_params = (start_date_str, end_date_str)
            sales_query = f"""
            SELECT COALESCE(SUM(total_amount), 0.0)
            FROM Customer_Sales_Bills
            WHERE date BETWEEN ? AND ? {sales_filter};
            """
            self.cursor.execute(sales_query, sales_params)
            result = self.cursor.fetchone()[0]
            sales_revenue = result if result is not None else 0.0

            # 3. Calculate total additional costs (from Additional_Costs)
            additional_costs_query = """
            SELECT COALESCE(SUM(amount), 0.0)
            FROM Costs
            WHERE date BETWEEN ? AND ?;
            """
            self.cursor.execute(additional_costs_query, (start_date_str, end_date_str))
            result = self.cursor.fetchone()[0]
            additional_costs = result if result is not None else 0.0

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

