from view.wallet_view import WalletView
from model.wallet_model import WalletModel

class WalletController:
    def __init__(self, root, db_conn):
        self.root = root
        self.db_conn = db_conn
        self.model = WalletModel(self.db_conn)
        self.view = WalletView(self.root)
        self.wallet_id = None
        self._bind_events()


    def _bind_events(self):
        self.view.populate_treeview(self.model.get_wallets())
        
        self.view.bind_table(self.get_selected_wallet)
        
        buttons_maping = {
            'اضافة': self.add_wallet,
            'حذف': self.delete_wallet,
            'تعديل': self.update_wallet,
            'تنظيف المدخلات': self.clear_inputs,
        }
        
        for button in self.view.buttons:
            button.configure(command= lambda  title= button.cget("text"): buttons_maping[title]())


    def add_wallet(self):
        """add wallet to database

        Steps:
            # get wallet information from view
            # check if inputs are empty or money = 0
            # check if wallet exists
            # add wallet to database
            # update treeview
            # clear inputs and set wallet id = None
            # show success message
        """
        wallet_name = self.view.wallet_name_var.get()
        wallet_money = self.view.wallet_money_var.get()
        if wallet_name == '' or wallet_money <= 0:
            return self.view.message("showinfo", "خطأ", "يرجى إدخال اسم الخزنة والمبلغ بشكل صحيح")
        
        if self.model.wallet_exists(wallet_name): 
            return self.view.message("showinfo", "خطأ", "اسم الخزنة موجود بالفعل")
        
        is_true, error = self.model.add_wallet(wallet_name, wallet_money)
        self.view.message("showinfo", "نجاح" if is_true else "خطأ", "تم إضافة الخزنة بنجاح" if is_true else f'حدث خطأ اثناء اضافة الخزنة: {error}')
        
        self.view.populate_treeview(self.model.get_wallets())
        if is_true:
            self.view.wallet_name_var.set('')
            self.view.wallet_money_var.set(0)
            self.wallet_id = None


    def delete_wallet(self):
        """delete wallet from database

        Steps:
            # check if wallet id is selected
            # sure to delete
            # delete wallet from database
            # update treeview
            # clear inputs and wallet id = None
            # show success message
        """
        if self.wallet_id:
            if self.view.message("yes_no", "تأكيد", "هل تريد حذف الخزنة ؟"):
                is_true, error = self.model.delete_wallet(self.wallet_id)
                self.view.message("showinfo", "نجاح" if is_true else "خطأ", "تم حذف الخزنة بنجاح" if is_true else f'حدث خطأ اثناء حذف الخزنة: {error}')
                
                self.view.populate_treeview(self.model.get_wallets())
                if is_true:
                    self.view.wallet_name_var.set('')
                    self.view.wallet_money_var.set(0)
                    self.wallet_id = None
        else:
            return self.view.message("showinfo", "خطأ", "يرجى اختيار الخزنة المراد حذفه")


    def update_wallet(self):
        """update wallet name in database

        Steps:
            # check if wallet id is selected
            # get new wallet name from view
            # check if wallet name is empty and wallet money = 0
            # check if wallet exists with other id than selected
            # update wallet name in database
            # update treeview
            # clear inputs and wallet id = None
            # show success message
        """
        if self.wallet_id:
            new_wallet_name = self.view.wallet_name_var.get()
            new_wallet_money = self.view.wallet_money_var.get()
            if new_wallet_name == '':
                return self.view.message("showinfo", "خطأ", "يرجى إدخال اسم الخزنة الجديد")
            
            if self.model.new_wallet_name_exist(self.wallet_id, new_wallet_name):
                return self.view.message("showinfo", "خطأ", "اسم الخزنة موجود بالفعل")
            
            is_true, error = self.model.update_wallet(self.wallet_id, new_wallet_name, new_wallet_money)
            self.view.message("showinfo", "نجاح" if is_true else "خطأ", "تم تعديل اسم الخزنة بنجاح" if is_true else f'حدث خطأ اثناء تعديل اسم الخزنة: {error}')
            
            self.view.populate_treeview(self.model.get_wallets())
            if is_true:
                self.view.wallet_name_var.set('')
                self.view.wallet_money_var.set(0)
                self.wallet_id = None
        else:
            return self.view.message("showinfo", "خطأ", "يرجى اختيار الخزنة المراد تعديلها")


    def clear_inputs(self):
        self.view.wallet_name_var.set('')
        self.view.wallet_money_var.set(0)
        self.wallet_id = None
        self.view.message("showinfo", "نجاح", "تم تنظيف المدخلات ")
        self.view.populate_treeview(self.model.get_wallets())


    def get_selected_wallet(self, row_values):
        if row_values:
            self.view.wallet_name_var.set(row_values[0])
            self.view.wallet_money_var.set(row_values[1])
            self.wallet_id = self.model.get_wallet_id(wallet_name= row_values[0])[0]

