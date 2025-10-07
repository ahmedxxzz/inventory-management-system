

class DistributorModel:
    def __init__(self, db_conn):
        self.conn = db_conn
        self.cursor = self.conn.cursor()
    
    
    def get_distributors(self):
        """get distributors names

        Returns:
            list of tuples: distributors names
        """
        self.cursor.execute("SELECT name FROM Distributor")
        return self.cursor.fetchall()  # = [(name1,), (name2,), ...]
    
    
    def distributor_exists(self, distributor_name):
        self.cursor.execute("SELECT name FROM Distributor WHERE name = ?", (distributor_name,))
        return self.cursor.fetchone()


    def new_distributor_name_exist(self, distributer_id, distributor_name):
        self.cursor.execute("SELECT distributor_id FROM Distributor WHERE name = ? AND distributor_id != ?", (distributor_name, distributer_id,))
        return self.cursor.fetchone() is not None 


    def get_distributor_id(self, distributor_name):
        self.cursor.execute("SELECT distributor_id FROM Distributor WHERE name = ?", (distributor_name,))
        return self.cursor.fetchone()


    def add_distributor(self, distributor_name):
        try:
            self.cursor.execute("INSERT INTO Distributor (name) VALUES (?)", (distributor_name,))
            self.conn.commit()
            return True, None
        
        except Exception as e:
            try:
                self.conn.rollback()
            except Exception as e:
                return False, e
            return False, e


    def update_distributor(self, distributor_id, distributor_name):
        try:
            self.cursor.execute("UPDATE Distributor SET name = ? WHERE distributor_id = ?", (distributor_name, distributor_id,))
            self.conn.commit()
            return True, None
        
        except Exception as e:
            try:
                self.conn.rollback()
            except Exception as e:
                return False, e
            return False, e


    def delete_distributor(self, distributor_id):
        try:
            self.cursor.execute("DELETE FROM Distributor WHERE distributor_id = ?", (distributor_id,))
            self.conn.commit()
            return True, None
        
        except Exception as e:
            try:
                self.conn.rollback()
            except Exception as e:
                return False, e
            return False, e