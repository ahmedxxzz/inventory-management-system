from view.Inventory_components_view.snow_inv_view import SnowInvView
from model.Inventory_components_model.snow_inv_model import SnowInvModel

class SnowInvController:
    def __init__(self, frame):
        self.root = frame
        self.view = SnowInvView(self.root)
        self.model = SnowInvModel()
        self.view.populate_treeview(self.model.get_products_info())
        
        
        
    