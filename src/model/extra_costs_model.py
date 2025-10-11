import datetime
class ExtraCostModel:
    def __init__(self, db_conn):
        self.conn = db_conn
        self.cursor = self.conn.cursor()


    def get_ExtraCosts(self):
        return self.cursor.execute("""
                                   SELECT 
                                        EC.description, 
                                        EC.date, 
                                        EC.amount, 
                                        WA.name  
                                    FROM 
                                        Costs as EC 
                                    INNER JOIN 
                                        Wallets AS WA 
                                        ON EC.wallet_id = WA.wallet_id
                                    """).fetchall()


    def get_wallets(self):
        data = self.cursor.execute("SELECT name FROM Wallets").fetchall()
        wallet_values =[] 
        for i in data:
            wallet_values.append(i[0])
        return wallet_values


    def get_wallet_id_from_name(self, name):
        self.cursor.execute("SELECT wallet_id FROM Wallets WHERE name = ?", (name,))
        return self.cursor.fetchone()[0]


    def save_adds(self, description, price,  wallet):
        try :
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute("INSERT INTO Costs (description, date, amount,  wallet_id) VALUES (?, ?, ?, ?);", (description,  date, price, self.get_wallet_id_from_name(wallet))) 
            self.conn.commit()
            return True, None
        except Exception as e:
            return False, e
    
    