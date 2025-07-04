from view.Factory_compnents_view.factory_account_details_view import FactoryAccountDetailsView
from model.Factory_compnents_model.factory_account_details_model import FactoryAccountDetailsModel

class FactoryAccountDetailsController:
    def __init__(self, root, frames, factory_name):
        self.root = root
        self.frames = frames
        self.factory_name = factory_name
        self.view = FactoryAccountDetailsView(self.root, self.factory_name)
        self.model = FactoryAccountDetailsModel(self.factory_name)
        
        
        self.fill_data()
        self.view.populate_treeview(self.model.get_factory_account_details())
        
        self._bind_events()
                
    
    
    def _bind_events(self):
        self.view.back_btn.configure(command=self.back)
        self.view.report_btn.configure(command=self.report)
    
    def fill_data(self ):
        fac_money, fac_quantity = self.model.get_factory_data()
        self.view.money_lbl.configure(text=f'الرصيد الحالي : \n{fac_money}')
        self.view.quantity_lbl.configure(text=f'الكمية الحالية : \n{fac_quantity}')
    
    
    
    def back(self):
        from controller.Factory_compnents_controller.factory_account_controller import FactoryAccountController
        for frame in self.frames:
            frame.destroy()
        
        factory_accounts = FactoryAccountController(self.root, self.frames)
        self.frames.append(factory_accounts.view)


    def report(self):
        from controller.Factory_compnents_controller.report_controller import ReportController
        factory_accounts = ReportController( self.factory_name)