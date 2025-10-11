from view.Customer.customer_account_details_view import CustomerAccountDetailsView
from model.Customer.customer_account_details_model import CustomerAccountDetailsModel



class CustomerAccountDetailsController:
    def __init__(self, root, db_conn, customer_id, distributor, customer_frames_list):
        self.root = root
        self.db_conn = db_conn
        self.customer_id = customer_id
        self.distributor = distributor
        self.Frames = customer_frames_list
        
        self.model = CustomerAccountDetailsModel(self.db_conn, self.customer_id, self.distributor)
        self.view = CustomerAccountDetailsView(self.root, self.model.get_customer_name())
        
        self._bind_events()

    def _bind_events(self):
        self.fill_data()
        self.view.populate_treeview(self.model.get_customer_transactions())
        self.view.back_btn.configure(command=self.back)
        self.view.bind_table(self.get_selected_transaction)
        self.view.report_btn.configure(command=self.report)        


    def fill_data(self):
        cus_money, cus_quantity = self.model.get_customer_data()
        self.view.money_lbl.configure(text=f'الرصيد الحالي : \n{cus_money}')
        self.view.quantity_lbl.configure(text=f'الكمية الحالية : \n{cus_quantity}')


    def back(self):
        for frame in self.Frames:
            frame.destroy()
        self.Frames.clear()

        from controller.Customer.customer_account_controller import CustomerAccountController
        customers_accounts = CustomerAccountController(self.root, self.db_conn, self.distributor, self.Frames)
        self.Frames.append(customers_accounts.view)


    def get_selected_transaction(self, row_values):
        if row_values:
            from controller.Customer.show_details_popup_controller import ShowDetailsPopupController
            popup = ShowDetailsPopupController(self.root, row_values[0], row_values[2], self.db_conn, self.distributor, self.customer_id)


    def report(self):
        pass

