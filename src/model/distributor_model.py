import os

class DistributorModel:
    def __init__(self, db_conn):
        self.conn = db_conn
        self.cursor = self.conn.cursor()
    
    def get_distributors(self):
        """Fetches distributor names and their logo paths."""
        self.cursor.execute("SELECT name, logo_path FROM Distributor ORDER BY name")
        return self.cursor.fetchall()
    
    def get_distributor_by_id(self, distributor_id):
        """Fetches a single distributor's name and logo_path by their ID."""
        self.cursor.execute("SELECT name, logo_path FROM Distributor WHERE distributor_id = ?", (distributor_id,))
        return self.cursor.fetchone()

    def add_distributor(self, distributor_name, logo_path=None):
        """Adds a new distributor with an optional logo path."""
        try:
            db_logo_path = logo_path if logo_path else None
            self.cursor.execute("INSERT INTO Distributor (name, logo_path) VALUES (?, ?)", (distributor_name, db_logo_path))
            self.conn.commit()
            return True, None
        except Exception as e:
            self.conn.rollback()
            return False, e

    def update_distributor(self, distributor_id, distributor_name, logo_path=None):
        """Updates an existing distributor's name and logo path."""
        try:
            db_logo_path = logo_path if logo_path else None
            self.cursor.execute("UPDATE Distributor SET name = ?, logo_path = ? WHERE distributor_id = ?", (distributor_name, db_logo_path, distributor_id))
            self.conn.commit()
            return True, None
        except Exception as e:
            self.conn.rollback()
            return False, e

    def delete_distributor(self, distributor_id):
        """Deletes a distributor and their associated logo file."""
        try:
            # First, get the logo path to delete the associated file
            old_data = self.get_distributor_by_id(distributor_id)
            if old_data and old_data[1]: # old_data[1] is the logo_path
                old_logo_path = old_data[1]
                if os.path.exists(old_logo_path):
                    os.remove(old_logo_path)

            self.cursor.execute("DELETE FROM Distributor WHERE distributor_id = ?", (distributor_id,))
            self.conn.commit()
            return True, None
        except Exception as e:
            self.conn.rollback()
            return False, e
            
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