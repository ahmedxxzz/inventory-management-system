from view.Factory.factory_account_view import FactoryAccountView
from model.Factory.factory_account_model import FactoryAccountModel

class FactoryAccountController:
    def __init__(self, root, db_conn):
        self.root = root
        self.db_conn = db_conn
        self.view = FactoryAccountView(self.root)
        self.model = FactoryAccountModel(self.db_conn)
        self.factory_id = None
        
        self._bind_events()


    def _bind_events(self):
        self.view.populate_treeview(data = self.model.get_factories_accounts())
        
        self.view.bind_table(function = self.show_factory_details)
        
        self.view.search_entry.bind("<KeyRelease>", lambda e: self.view.populate_treeview(data = self.model.search_factories_accounts(self.view.search_var.get())))

        self.view.adding_btn.configure(command= self.adding_factory_account)


    def show_factory_details(self, row_values):
        if row_values:
            if self.view.message("yes_no", "تأكيد", "هل تريد عرض تفاصيل المصنع؟"):
                self.factory_id = self.model.get_factory_id(row_values[0])
                for widget in self.view.winfo_children():
                    widget.destroy()
                from controller.Factory.factory_account_details_controller import FactoryAccountDetailsController
                FactoryAccountDetailsController(self.view, self.db_conn, self.factory_id)


    def adding_factory_account(self):
        """adding factory account to database 
        
        Steps:
            # get information from view
            # check if inputs are empty
            # check if factory exist
            # add factory account to database
            # update the treeview
            # clear inputs and set factory id = None
            # show success message
        """
        factory_name = self.view.fac_name.get()
        factory_amount_money = float(self.view.amount_money.get()) if self.view.amount_money.get() != '' else 0
        factory_product_quantity = int(self.view.product_quantity.get()) if self.view.product_quantity.get() != '' else 0
        
        if factory_name == '' :
            return self.view.message("showinfo", "خطأ", "يرجى إدخال اسم المصنع بشكل صحيح")
        
        if self.model.factory_exists(factory_name): 
            return self.view.message("showinfo", "خطأ", "اسم المصنع موجود بالفعل")
        
        is_true, error = self.model.add_factory_account(factory_name, factory_amount_money, factory_product_quantity)
        self.view.message("showinfo", "نجاح" if is_true else "خطأ", "تم إضافة المصنع بنجاح" if is_true else f'حدث خطأ اثناء اضافة المصنع: {error}')
        
        self.view.populate_treeview(self.model.get_factories_accounts())
        if is_true:
            self.view.fac_name.set('')
            self.view.amount_money.set('')
            self.view.product_quantity.set('')
            self.factory_id = None

