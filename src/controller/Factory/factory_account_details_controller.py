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
        self.view.edit_name_btn.configure(command=self.edit_factory_name)

    def edit_factory_name(self):
        """Handles editing the factory name via popup."""
        current_name = self.model.get_factory_name()
        new_name = self.view.create_edit_name_popup(current_name)
        
        if new_name and new_name != current_name:
            success, error = self.model.update_factory_name(new_name)
            if success:
                self.view.update_name_label(new_name)
                self.view.message("showinfo", "نجاح", "تم تعديل اسم المصنع بنجاح")
            else:
                self.view.message("showinfo", "خطأ", f"فشل تعديل الاسم: {error}")        


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
            from controller.Factory.show_details_popup_controller import ShowDetailsPopupController
            popup = ShowDetailsPopupController(self.root, row_values[0], row_values[2], self.db_conn)

    def report(self):
        from controller.Factory.account_report_controller import AccountReportController
        AccountReportController( self.factory_id, self.db_conn)

