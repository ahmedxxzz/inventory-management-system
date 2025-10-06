

class InventoryModel:
    def __init__(self, db_conn):
        self.db_conn = db_conn
        self.cursor = self.db_conn.cursor()
        
    def get_distributors(self):
        """get distributors names

        Returns:
            list: distributors names
        """
        self.cursor.execute("SELECT name FROM Distributor")
        distributors = self.cursor.fetchall() # = [(name1,), (name2,), ...]
        distributors_list_names = [distributor[0] for distributor in distributors]
        return distributors_list_names # = [name1, name2, ...]