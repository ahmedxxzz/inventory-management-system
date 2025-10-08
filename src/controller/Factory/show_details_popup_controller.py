from view.Factory.show_details_popup_view import ShowDetailsPopupView
from model.Factory.show_details_popup_model import ShowDetailsPopupModel


class ShowDetailsPopupController:
    def __init__(self, root, operation_id, operation_type, db_conn):
        self.root = root
        self.view = ShowDetailsPopupView(self.root,  operation_type)
        self.model = ShowDetailsPopupModel(operation_id, db_conn)
        self.show_details(operation_type)




    def show_details(self, operation_type):
        if operation_type =='فاتورة شراء':
            self.view.populate_treeview(self.model.get_buy_details())


        elif operation_type == 'دفعة':
            self.view.populate_treeview(self.model.get_pay_details())


        elif operation_type == 'مرتجع':
            self.view.populate_treeview(self.model.get_return_details())
