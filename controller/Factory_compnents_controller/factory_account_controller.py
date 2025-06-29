from view.Factory_compnents_view.factory_account_view  import FactoryAccountView
from model.Factory_compnents_model.factory_account_model import FactoryAccountModel
from controller.Factory_compnents_controller.report_controller import ReportController

class FactoryAccountController:
    def __init__(self, root):
        self.root = root
        self.view = FactoryAccountView(self.root)
        self.model = FactoryAccountModel()
        self.search_key_release()
        self._bind_events()
        
    def _bind_events(self):

        self.view.search_entry.bind('<KeyRelease>', lambda event: self.search_key_release())
        self.view.adding_btn.configure(command=self.add_new_fac)
    
    
    
    
    def search_key_release(self):
        self.view.delete_factory_frames()
        
        
        for row in self.model.get_factories_data(self.view.search_var.get().strip()):
            self.view.add_factory_frame(*row, self.zeros_factory, ReportController)


    def zeros_factory(self, factory_name ):
        if self.view.message('yes_no', 'تصفير المصنع', f'هل تريد تصفير حساب المصنع : {factory_name} ؟'):
            self.view.delete_factory_frames()
            self.model.zeros_factory_account(factory_name)
            
            self.search_key_release()


    def add_new_fac(self):
        if self.check_inputs():
            self.model.adding_new_fac(self.view.fac_name.get().strip(), float(self.view.amount_money.get()), int(self.view.product_quantity.get()))
            self.view.message('showinfo', 'عملية ناجحة', 'تمت عملية الاضافة بنجاح')
            self.search_key_release()
        

    def check_inputs(self):
        # self.view.fac_name    self.view.amount_money   self.view.product_quantity
        if self.view.fac_name.get().strip() == '' or self.view.amount_money.get().strip() == '' or self.view.product_quantity.get().strip() == '':
            self.view.message('showinfo', ' خطاء', 'يرجى عدم ترك الحقول فارغة')
            return False

        if self.model.check_factory_name_exist(self.view.fac_name.get().strip()):
            self.view.message('showinfo', 'عملية فاشلة', 'اسم المصنع موجود بالفعل')
            return False

        return True