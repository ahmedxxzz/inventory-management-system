
class FactoryAccountDetailsController:
    def __init__(self, root, db_conn, factory_id):
        self.root = root
        self.db_conn = db_conn
        self.factory_id = factory_id
        pass