class CustomerAccountModel:
    def __init__(self, db_conn, distributor):
        self.conn = db_conn
        self.cursor = self.conn.cursor()
        self.distributor = distributor


    def get_customers_accounts(self, name=None):
        if name :
            return self.cursor.execute("""SELECT
                                            C.name AS customer_name,
                                            CDA.current_balance AS outstanding_balance,
                                            CDA.current_quantity AS total_pieces
                                        FROM
                                            Customer_Distributor_Accounts AS CDA
                                        JOIN
                                            Customer AS C
                                            ON CDA.customer_id = C.customer_id
                                        JOIN
                                            Distributor AS D
                                            ON CDA.distributor_id = D.distributor_id
                                        WHERE
                                            D.name = ? and C.name LIKE ?; 
                                        """, (self.distributor, '%' + name + '%')).fetchall()
        
        return self.cursor.execute("""SELECT
                                            C.name AS customer_name,
                                            CDA.current_balance AS outstanding_balance,
                                            CDA.current_quantity AS total_pieces
                                        FROM
                                            Customer_Distributor_Accounts AS CDA
                                        JOIN
                                            Customer AS C
                                            ON CDA.customer_id = C.customer_id
                                        JOIN
                                            Distributor AS D
                                            ON CDA.distributor_id = D.distributor_id
                                        WHERE
                                            D.name = ?; 
                                        """, (self.distributor,)).fetchall()


    def customer_exists(self, customer_name):
        sql_query = """
        SELECT 
            CDA.account_id
        FROM 
            Customer_Distributor_Accounts AS CDA
        JOIN 
            Customer AS C
            ON CDA.customer_id = C.customer_id
        JOIN
            Distributor AS D
            ON CDA.distributor_id = D.distributor_id
        WHERE 
            C.name = ? AND D.name = ?; -- البحث باستخدام اسم الموزع واسم العميل
        """
        
        self.cursor.execute(sql_query, (customer_name, self.distributor)) 
        
        return self.cursor.fetchone() is not None


    def add_customer_account(self, customer_name, balance, quantity):
        distributor_id = self.cursor.execute("SELECT distributor_id FROM Distributor WHERE name = ?", (self.distributor,)).fetchone()[0]
            

        # 2. البحث عن معرف العميل (customer_id)
        customer_id_result =self.cursor.execute("SELECT customer_id FROM Customer WHERE name = ?", (customer_name,)).fetchone()
        
        # 3. إنشاء العميل إذا لم يكن موجودًا
        if customer_id_result is None:
            try:
                self.cursor.execute("INSERT INTO Customer (name) VALUES (?)", (customer_name,))
                # جلب المعرّف الجديد (لأن هذا هو الهدف الرئيسي)
                customer_id = self.cursor.lastrowid
            except Exception as e:
                self.conn.rollback()
                err = (f" حدث خطأ عند إضافة العميل: {e}")
                return False, err
        else:
            # استخراج المعرّف الموجود
            customer_id = customer_id_result[0] 

        # 4. التحقق من وجود الحساب المشترك (لمنع تعارض قيد UNIQUE)
        account_exists = self.cursor.execute("""SELECT account_id FROM Customer_Distributor_Accounts WHERE customer_id = ? AND distributor_id = ?""",(customer_id, distributor_id)).fetchone()

        # 5. إدخال الحساب الجديد
        if account_exists is None:
            try:
                self.cursor.execute("""INSERT INTO Customer_Distributor_Accounts (customer_id, distributor_id, current_balance, current_quantity) VALUES (?, ?, ?, ?)""", (customer_id, distributor_id, balance, quantity))
                self.conn.commit()
                return True, None
            except Exception as e:
                self.conn.rollback()
                return False, e
        else:
            return False, "حساب موجود بالفعل"


    def get_customer_id(self, customer_name):
        return self.cursor.execute("SELECT customer_id FROM Customer WHERE name = ?", (customer_name,)).fetchone()[0]