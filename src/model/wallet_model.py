

class WalletModel:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()


    def get_wallets(self):
        self.cursor.execute("SELECT name, current_balance FROM Wallets")
        return self.cursor.fetchall() # = [(name1, balance1), (name2, balance2), ...]


    def get_wallet_id(self, wallet_name):
        self.cursor.execute("SELECT wallet_id FROM Wallets WHERE name = ?", (wallet_name,))
        return self.cursor.fetchone() # = (wallet_id,)


    def wallet_exists(self, wallet_name):
        self.cursor.execute("SELECT name FROM Wallets WHERE name = ?", (wallet_name,))
        return self.cursor.fetchone()


    def add_wallet(self, wallet_name, wallet_balance):
        try:
            self.cursor.execute("INSERT INTO Wallets (name, current_balance) VALUES (?, ?)", (wallet_name, wallet_balance))
            self.conn.commit()
            return True, None
        
        except Exception as e:
            try:
                self.conn.rollback()
            except Exception as e:
                return False, e
            return False, e


    def delete_wallet(self, wallet_id):
        try:
            self.cursor.execute("DELETE FROM Wallets WHERE wallet_id = ?", (wallet_id,))
            self.conn.commit()
            return True, None
        
        except Exception as e:
            try:
                self.conn.rollback()
            except Exception as e:
                return False, e
            return False, e


    def update_wallet(self, wallet_id, wallet_name, wallet_balance):
        try:
            self.cursor.execute("UPDATE Wallets SET name = ?, current_balance = ? WHERE wallet_id = ?", (wallet_name, wallet_balance, wallet_id))
            self.conn.commit()
            return True, None
        
        except Exception as e:
            try:
                self.conn.rollback()
            except Exception as e:
                return False, e
            return False, e


    def new_wallet_name_exist(self, wallet_id, wallet_name):
        self.cursor.execute("SELECT name FROM Wallets WHERE wallet_id != ? AND name = ?", (wallet_id, wallet_name))
        return self.cursor.fetchone() is not None 

