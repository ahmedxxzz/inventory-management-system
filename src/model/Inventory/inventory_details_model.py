class InventoryDetailsModel:
    def __init__(self, db_conn):
        self.conn = db_conn
        self.cursor = self.conn.cursor()


    def get_products_info(self, distributor= None):
        if distributor:
            return self.cursor.execute("""
                                       SELECT 
                                            P.name, 
                                            P.available_quantity, 
                                            P.selling_price 
                                        FROM 
                                            Product P
                                        JOIN
                                            Distributor D
                                            ON P.distributor_id = D.distributor_id
                                        where
                                            D.name = ?
                                       """, (distributor,)).fetchall()
        return self.cursor.execute("SELECT name, available_quantity, selling_price FROM Product").fetchall()


    def search_product(self, product_code, distributor= None):
        if distributor:
            return self.cursor.execute("""
                                       SELECT 
                                            P.name, 
                                            P.available_quantity, 
                                            P.selling_price 
                                        FROM 
                                            Product P
                                        JOIN
                                            Distributor D
                                            ON P.distributor_id = D.distributor_id
                                        WHERE 
                                            P.name LIKE ? and D.name = ?
                                       """, ('%' + product_code + '%', distributor,)).fetchall()
        return self.cursor.execute("""
                                       SELECT 
                                            name, 
                                            available_quantity, 
                                            selling_price 
                                        FROM 
                                            Product 
                                        WHERE 
                                            name LIKE ? 
                                       """, ('%' + product_code + '%',)).fetchall()

