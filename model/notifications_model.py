import sqlite3



class NotificationsModel():
    def __init__(self):
        self.conn = sqlite3.connect('IMS.db')
        self.cursor = self.conn.cursor()
        
        
    def get_notifications(self, supplier):
        if supplier == 'snow white':
            self.cursor.execute("SELECT message FROM Notifications WHERE type !='golden_cus_unpaid' AND type !='golden_cus_overdue'  AND seen = 0 ")
        elif supplier == 'golden rose':
            self.cursor.execute("SELECT message FROM Notifications WHERE type !='snow_cus_unpaid' AND type !='snow_cus_overdue'  AND seen = 0 ")
        return self.cursor.fetchall()
        
    
    def seen_notification(self, message):
        noti_type = self.get_noti_type(message)
        if noti_type == 'factory_no_work' or noti_type == 'snow_cus_unpaid' or noti_type == 'golden_cus_unpaid':
            self.cursor.execute("UPDATE Notifications SET seen = 1 WHERE message = ?", (message,))
        else:
            self.cursor.execute("DELETE FROM Notifications WHERE message = ?", (message,))
        self.conn.commit()
    
    
    def get_noti_type(self, message):
        self.cursor.execute("SELECT type FROM Notifications WHERE message = ?", (message,))
        return self.cursor.fetchone()[0]