from view.extra_costs_view import ExtraCostView
from model.extra_costs_model import ExtraCostModel

class ExtraCostController:
    def __init__(self, root, db_conn):
        self.root = root
        self.db_conn = db_conn
        self.model = ExtraCostModel(self.db_conn)
        self.view = ExtraCostView(self.root)

        self._bind_events()
        self.view.populate_treeview(self.model.get_ExtraCosts())


    def _bind_events(self):
        self.view.wallet_menu.configure(values=['اختار الخزنة'] + self.model.get_wallets())
        self.view.save_btn.configure(command=self.save_extra_cost)


    def save_extra_cost(self):
        if self.check_inputs():
            extracost = self.view.adds_type.get().strip()
            price = float(self.view.price.get())
            wallet = self.view.wallet.get()
            is_true, error = self.model.save_adds(extracost, price, wallet)
            if not is_true:
                self.view.message('showinfo', 'عملية فاشلة', f'حدث خطأ اثناء عملية الاضافة: {error}')
                return
            
            self.view.message('showinfo', 'عملية ناجحة', 'تمت عملية الاضافة بنجاح')
            self.view.populate_treeview(self.model.get_ExtraCosts())


    def check_inputs(self):
        extracost = self.view.adds_type.get().strip()
        price = float(self.view.price.get()) if self.view.price.get() != '' else 0
        wallet = self.view.wallet.get() if self.view.wallet.get() != 'اختار الخزنة' else None

        if extracost == '' or price == 0 :
            self.view.message('showinfo', ' خطاء', 'يرجى عدم ترك الحقول فارغة')
            return False
        if price <= 0.0:
            self.view.message('showinfo', 'عملية فاشلة', 'سعر المصروفات  يجب ان يكون اكبر من 0')
            return False
        if wallet == None:
            self.view.message('showinfo', 'عملية فاشلة', 'يجب اختيار خزنة')
            return False
        
        return True

