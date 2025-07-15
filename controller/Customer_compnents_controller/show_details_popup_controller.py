from view.Customer_compnents_view.show_details_popup_view import ShowDetailsPopupView
from model.Customer_compnents_model.show_details_popup_model import ShowDetailsPopupModel


class ShowDetailsPopupController:
    def __init__(self, root, operation_id, operation_type):
        self.root = root
        self.view = ShowDetailsPopupView(self.root, operation_type)
        self.model = ShowDetailsPopupModel(operation_id)
        
        self.show_details(operation_type)
        
        
    def show_details(self, operation_type):
        if operation_type =='شراء':
            self.view.populate_treeview(self.model.get_buy_details())


        elif operation_type == 'دفع':
            self.view.populate_treeview(self.model.get_pay_details())


        elif operation_type == 'مرتجع':
            self.view.populate_treeview(self.model.get_return_details())
