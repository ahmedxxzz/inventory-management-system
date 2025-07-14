from view.Inventory_components_view.golden_inv_view import GoldenInvView
from model.Inventory_components_model.golden_inv_model import GoldenInvModel



class GoldenInvController:
    def __init__(self, frame):
        self.root = frame
        self.view = GoldenInvView(self.root)
        self.model = GoldenInvModel()
        self.view.populate_treeview(self.model.get_products_info())
        self._bind_events()

    
    
    def _bind_events(self):
        self.view.search_entry.bind("<KeyRelease>", self.search_product)

    def search_product(self, event):
        self.view.populate_treeview(self.model.search_product(self.view.search_entry.get().strip()))
    

        
        
        
    