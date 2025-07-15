from view.Customer_compnents_view.customer_account_view  import CustomerAccountView
from model.Customer_compnents_model.customer_account_model import CustomerAccountModel
from controller.Customer_compnents_controller.customer_account_details_controller import CustomerAccountDetailsController

class CustomerAccountController:
    def __init__(self, root, supplier, root_frames):
        self.root = root
        self.frames = root_frames
        self.supplier = supplier
        self.view = CustomerAccountView(self.root, self.supplier)
        self.model = CustomerAccountModel(self.supplier)
        self.search_key_release()
        self._bind_events()
        
    def _bind_events(self):

        self.view.search_entry.bind('<KeyRelease>', lambda event: self.search_key_release())
        self.view.adding_btn.configure(command=self.add_new_cus)
    
    
    

    def search_key_release(self):
        self.view.delete_customer_frames()
        
        
        for row in self.model.get_customers_data(self.view.search_var.get().strip()):
            self.view.add_customer_frame(*row, self.zeros_customer, CustomerAccountDetailsController, self.frames)


    def zeros_customer(self, customer_name ):
        if self.view.message('yes_no', 'تصفير المكتب', f'هل تريد تصفير حساب المكتب : {customer_name} ؟'):
            self.view.delete_customer_frames()
            self.model.zeros_customer_account(customer_name)
            
            self.search_key_release()


    def add_new_cus(self):
        if self.check_inputs():
            self.model.adding_new_cus(self.view.cus_name.get().strip(), float(self.view.amount_money.get()), int(self.view.product_quantity.get()))
            self.view.message('showinfo', 'عملية ناجحة', 'تمت عملية الاضافة بنجاح')
            self.clear_inputs()
            self.search_key_release()
        

    def check_inputs(self):
        # self.view.cus_name    self.view.amount_money   self.view.product_quantity
        if self.view.cus_name.get().strip() == '' or self.view.amount_money.get().strip() == '' or self.view.product_quantity.get().strip() == '':
            self.view.message('showinfo', ' خطاء', 'يرجى عدم ترك الحقول فارغة')
            return False

        if self.model.check_customer_name_exist(self.view.cus_name.get().strip()):
            self.view.message('showinfo', 'عملية فاشلة', 'اسم المكتب موجود بالفعل')
            return False

        return True

    def clear_inputs(self):
        self.view.search_var.set('')
        self.view.cus_name.set('')
        self.view.amount_money.set('')
        self.view.product_quantity.set('')