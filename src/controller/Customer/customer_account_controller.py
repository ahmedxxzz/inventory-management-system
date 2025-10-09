from view.Customer.customer_account_view import CustomerAccountView
from model.Customer.customer_account_model import CustomerAccountModel

class CustomerAccountController:
    def __init__(self, root, db_conn, distributor, customer_frames_list):
        self.root = root
        self.db_conn = db_conn
        self.distributor = distributor
        self.Frames = customer_frames_list
        self.view = CustomerAccountView(self.root)
        self.model = CustomerAccountModel(self.db_conn, self.distributor)
        
        self._bind_events()


    def _bind_events(self):
        self.view.populate_treeview(data = self.model.get_customers_accounts())
        
        self.view.bind_table(function = self.show_customer_details)
        
        self.view.search_entry.bind("<KeyRelease>", lambda e: self.view.populate_treeview(data = self.model.get_customers_accounts(self.view.search_var.get())))

        self.view.adding_btn.configure(command= self.adding_customer_account)


    def show_customer_details(self, row_values):
        if row_values:
            if self.view.message("yes_no", "تأكيد", "هل تريد عرض تفاصيل المكتب؟"):
                self.customer_id = self.model.get_customer_id(row_values[0])
                for frame in self.Frames:
                    frame.destroy()
                self.Frames.clear()
                
                from controller.Customer.customer_account_details_controller import CustomerAccountDetailsController
                customer_account_details = CustomerAccountDetailsController(self.root, self.db_conn, self.customer_id, self.distributor, self.Frames)
                self.Frames.append(customer_account_details.view) 


    def adding_customer_account(self):
        """adding customer account to database 
        
        Steps:
            # get information from view
            # check if inputs are empty
            # check if customer exist
            # add customer account to database and create customer account for distributor
            # update the treeview
            # clear inputs and set customer id = None
            # show success message
        """
        customer_name = self.view.customer_name.get()
        customer_amount_money = float(self.view.amount_money.get()) if self.view.amount_money.get() != '' else 0
        customer_product_quantity = int(self.view.product_quantity.get()) if self.view.product_quantity.get() != '' else 0
        
        if customer_name == '' :
            return self.view.message("showinfo", "خطأ", "يرجى إدخال اسم المكتب بشكل صحيح")
        
        if self.model.customer_exists(customer_name): 
            return self.view.message("showinfo", "خطأ", "اسم المكتب موجود بالفعل")
        
        is_true, error = self.model.add_customer_account(customer_name, customer_amount_money, customer_product_quantity)
        self.view.message("showinfo", "نجاح" if is_true else "خطأ", "تم إضافة المكتب بنجاح" if is_true else f'حدث خطأ اثناء اضافة المكتب: {error}')
        
        self.view.populate_treeview(self.model.get_customers_accounts())
        if is_true:
            self.view.customer_name.set('')
            self.view.amount_money.set('')
            self.view.product_quantity.set('')
            self.customer_id = None

