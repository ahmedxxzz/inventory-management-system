from view.additional_costs_view import AdditionalCostsView
from model.additional_costs_model import AdditionalCostsModel

class AdditionalCostsController:

    def __init__(self, frame):
        self.view = AdditionalCostsView(frame)
        self.model = AdditionalCostsModel()



        self._bind_events()
        self.view.populate_treeview(self.model.get_Adds())


    def _bind_events(self):
        self.view.save_btn.configure(command=self.save_product)
        self.view.safe_combo.configure(values=self.model.get_safes())


    def save_product(self):
        if self.check_inputs():
            self.model.save_adds(self.view.adds_type.get(), self.view.price.get(), self.view.safe.get())
            self.view.message('showinfo', 'عملية ناجحة', 'تمت عملية الاضافة بنجاح')
            self.view.populate_treeview(self.model.get_Adds())


    def check_inputs(self):

        if self.view.adds_type.get().strip() == '' or self.view.price.get() == '' :
            self.view.message('showinfo', ' خطاء', 'يرجى عدم ترك الحقول فارغة')
            return False
        
        if float(self.view.price.get()) <= 0.0:
            self.view.message('showinfo', 'عملية فاشلة', 'سعر المصروفات  يجب ان يكون اكبر من 0')
            return False
        if self.view.safe.get() not in self.model.get_safes():
            self.view.message('showinfo', 'عملية فاشلة', 'يجب اختيار خزنة')
            return False
        
        return True

