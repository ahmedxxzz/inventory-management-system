from view.Inventory.inventory_details_view import InventoryDetailsView
from model.Inventory.inventory_details_model import InventoryDetailsModel

class InventoryDetailsController:
    def __init__(self, frame, db_conn, title):
        self.frame = frame
        self.db_conn = db_conn
        self.distributor = title if title != 'كل الموزعين' else None
        self.model = InventoryDetailsModel(self.db_conn)
        self.view = InventoryDetailsView(self.frame)
        self.view.populate_treeview(self.model.get_products_info(self.distributor))
        self._bind_events()


    def _bind_events(self):
        self.view.search_entry.bind("<KeyRelease>", self.search_product)


    def search_product(self, event):
        self.view.populate_treeview(self.model.search_product(self.view.search_entry.get().strip(),self.distributor))

