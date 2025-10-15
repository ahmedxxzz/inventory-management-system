import sqlite3

class NotificationModel:
    def __init__(self, db_conn):
        self.conn = db_conn
        self.cursor = self.conn.cursor()

    def get_notifications_by_distributor(self, distributor_name=None):
        """
        Fetches notifications, filtered by distributor name if provided.
        If distributor_name is 'الجميع' or None, fetches all notifications.
        """
        base_query = """
            SELECT n.notification_id, n.date, n.message, n.status, n.type
            FROM Notifications n
        """
        params = []

        if distributor_name and distributor_name != 'الجميع':
            # This is a complex query to link notifications back to a distributor
            # We will filter for notification types that are related to distributors
            # ('late_payment' and 'low_stock')
            base_query += """
                LEFT JOIN Customer_Distributor_Accounts cda ON n.type = 'late_payment' AND n.reference_id = cda.account_id
                LEFT JOIN Product p ON n.type = 'low_stock' AND n.reference_id = p.product_id
                LEFT JOIN Distributor d ON d.distributor_id = COALESCE(cda.distributor_id, p.distributor_id)
                WHERE d.name = ? OR n.type = 'stale_factory' -- stale_factory is general and should appear for all
            """
            params.append(distributor_name)
        
        base_query += " ORDER BY n.notification_id DESC"
        
        try:
            self.cursor.execute(base_query, params)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error in get_notifications_by_distributor: {e}")
            return []

    def mark_all_as_seen(self):
        """Marks all 'unseen' notifications as 'seen'."""
        try:
            self.cursor.execute("UPDATE Notifications SET status = 'seen' WHERE status = 'unseen'")
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error in mark_all_as_seen: {e}")
            return False
