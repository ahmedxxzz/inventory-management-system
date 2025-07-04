from view.Customer_compnents_view.customer_account_details_view import CustomerAccountDetailsView
from model.Customer_compnents_model.customer_account_details_model import CustomerAccountDetailsModel

class CustomerAccountDetailsController:
    def __init__(self, root, frames, customer_name, supplier ):
        self.root = root
        self.frames = frames
        self.supplier = supplier
        self.customer_name = customer_name
        self.view = CustomerAccountDetailsView(self.root, self.customer_name)
        self.model = CustomerAccountDetailsModel(self.customer_name, self.supplier)
        
        
        self.fill_data()
        self.view.populate_treeview(self.model.get_customer_account_details())
        
        self._bind_events()
                
    
    
    def _bind_events(self):
        self.view.back_btn.configure(command=self.back)
        self.view.report_btn.configure(command=self.report)
    
    def fill_data(self ):
        cus_money, cus_quantity = self.model.get_customer_data()
        self.view.money_lbl.configure(text=f'الرصيد الحالي : \n{cus_money}')
        self.view.quantity_lbl.configure(text=f'الكمية الحالية : \n{cus_quantity}')
    
    
    
    def back(self):
        for frame in self.frames:
            frame.destroy()
        from controller.Customer_compnents_controller.customer_account_controller import CustomerAccountController
        
        customers_accounts = CustomerAccountController(self.root, self.supplier, self.frames)
        self.frames.append(customers_accounts.view)


    def report(self):
        from controller.Customer_compnents_controller.report_controller import ReportController
        customer_accounts = ReportController( self.customer_name)
