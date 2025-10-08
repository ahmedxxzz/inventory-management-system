from view.Factory.factory_account_details_view import FactoryAccountDetailsView
from model.Factory.factory_account_details_model import FactoryAccountDetailsModel


class FactoryAccountDetailsController:
    def __init__(self, root, db_conn, factory_id, factory_frames_list):
        self.root = root 
        self.db_conn = db_conn
        self.factory_id = factory_id
        self.Frames = factory_frames_list
        self.model = FactoryAccountDetailsModel(self.db_conn, self.factory_id)
        self.view = FactoryAccountDetailsView(self.root, self.model.get_factory_name())
        
        self._bind_events()


    def _bind_events(self):
        self.fill_data()
        self.view.populate_treeview(self.model.get_factor_transactions())
        self.view.back_btn.configure(command=self.back)
        self.view.bind_table(self.get_selected_transaction)
        self.view.report_btn.configure(command=self.report)        


    def fill_data(self):
        fac_money, fac_quantity = self.model.get_factory_data()
        self.view.money_lbl.configure(text=f'الرصيد الحالي : \n{fac_money}')
        self.view.quantity_lbl.configure(text=f'الكمية الحالية : \n{fac_quantity}')


    def back(self):
        for frame in self.Frames:
            frame.destroy()
        self.Frames.clear()

        from controller.Factory.factory_account_controller import FactoryAccountController
        factories_accounts = FactoryAccountController(self.root, self.db_conn, self.Frames)
        self.Frames.append(factories_accounts.view)


    def get_selected_transaction(self, row_values):
        if row_values:
            pass


    def report(self):
        pass
        # from controller.Factory_compnents_controller.account_report_controller import AccountReportController
        # AccountReportController( self.factory_id)

