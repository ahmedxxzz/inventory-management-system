class DistributorModel:
    def __init__(self, db_conn):
        self.conn = db_conn
        self.cursor = self.conn.cursor()
    
    def get_distributors(self):
        """Fetches distributor names and their logo paths."""
        self.cursor.execute("SELECT name, logo_path FROM Distributor ORDER BY name")
        return self.cursor.fetchall()
    
    def add_distributor(self, distributor_name, logo_path=None):
        """Adds a new distributor with an optional logo path."""
        try:
            self.cursor.execute("INSERT INTO Distributor (name, logo_path) VALUES (?, ?)", (distributor_name, logo_path))
            self.conn.commit()
            return True, None
        except Exception as e:
            self.conn.rollback()
            return False, e

    def update_distributor(self, distributor_id, distributor_name, logo_path=None):
        """Updates an existing distributor's name and logo path."""
        try:
            self.cursor.execute("UPDATE Distributor SET name = ?, logo_path = ? WHERE distributor_id = ?", (distributor_name, logo_path, distributor_id))
            self.conn.commit()
            return True, None
        except Exception as e:
            self.conn.rollback()
            return False, e

    def get_logo_path(self, distributor_name):
        """Fetches the logo path for a given distributor name."""
        try:
            self.cursor.execute("SELECT logo_path FROM Distributor WHERE name = ?", (distributor_name,))
            result = self.cursor.fetchone()
            return result[0] if result and result[0] else None
        except Exception as e:
            print(f"Error fetching logo path: {e}")
            return None
            
    # --- Other methods remain unchanged ---
    def distributor_exists(self, distributor_name):
        self.cursor.execute("SELECT 1 FROM Distributor WHERE name = ?", (distributor_name,))
        return self.cursor.fetchone() is not None

    def new_distributor_name_exist(self, distributor_id, distributor_name):
        self.cursor.execute("SELECT 1 FROM Distributor WHERE name = ? AND distributor_id != ?", (distributor_name, distributor_id))
        return self.cursor.fetchone() is not None

    def get_distributor_id(self, distributor_name):
        self.cursor.execute("SELECT distributor_id FROM Distributor WHERE name = ?", (distributor_name,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def delete_distributor(self, distributor_id):
        try:
            self.cursor.execute("DELETE FROM Distributor WHERE distributor_id = ?", (distributor_id,))
            self.conn.commit()
            return True, None
        except Exception as e:
            self.conn.rollback()
            return False, e
