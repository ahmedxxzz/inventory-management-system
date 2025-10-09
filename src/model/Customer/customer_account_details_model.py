
class CustomerAccountDetailsModel:
    def __init__(self, db_conn, customer_id, distributor):
        self.conn = db_conn
        self.cursor = self.conn.cursor()
        self.customer_id = customer_id
        self.distributor = distributor


    def get_customer_name(self):
        return self.cursor.execute("SELECT name FROM Customer WHERE customer_id = ?", (self.customer_id,)).fetchone()[0]


    def get_customer_data(self):
        sql_query = """
                    SELECT
                        CDA.current_balance,
                        CDA.current_quantity
                    FROM
                        Customer_Distributor_Accounts AS CDA
                    JOIN
                        Distributor AS D
                        ON CDA.distributor_id = D.distributor_id
                    WHERE
                        CDA.customer_id = ? AND D.name = ?;
                    """

        return self.cursor.execute(sql_query, (self.customer_id, self.distributor)).fetchone()


    def get_customer_transactions(self):
        distributor_id  = self.cursor.execute("SELECT distributor_id FROM Distributor WHERE name = ?", (self.distributor,)).fetchone()[0]
        params = (self.customer_id, distributor_id)
        purchases_transactions  = self.cursor.execute("SELECT sales_bill_id, date, 'فاتورة شراء', total_amount FROM Customer_Sales_Bills  WHERE customer_id = ? AND distributor_id = ?", params).fetchall()
        pays_transactions = self.cursor.execute("SELECT pay_id, date, 'دفعة', amount_paid FROM Customer_Pays  WHERE customer_id = ? AND distributor_id = ?", params).fetchall()
        returns_transactions = self.cursor.execute("SELECT return_id, date, 'مرتجع', total_amount FROM Customer_Returns  WHERE customer_id = ? AND distributor_id = ?", params).fetchall()
        all_transactions = purchases_transactions  + pays_transactions + returns_transactions
        return sorted(all_transactions, key=lambda t: t[1], reverse=True)

