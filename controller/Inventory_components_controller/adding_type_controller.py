from view.Inventory_components_view.adding_type_view import AddingTypeView
from model.Inventory_components_model.adding_type_model import AddingTypeModel

class AddingTypeController:
    def __init__(self, frame):
        self.view = AddingTypeView(frame)
        self.model = AddingTypeModel()
        
        
        
        self._bind_events()
        self.view.populate_treeview(self.model.get_products_info())
    
    
    def _bind_events(self):
        self.view.save_btn.configure(command=self.save_product)


    def save_product(self):
        if self.check_inputs():
            self.model.save_product(self.view.product_code.get(), self.view.price.get(), self.view.supplier.get())
            self.view.message('showinfo', 'عملية ناجحة', 'تمت عملية الاضافة بنجاح')
            self.clear_inputs()
            self.view.populate_treeview(self.model.get_products_info())


    def check_inputs(self):
        '''
        not empty
        product code should be not exist
        money should be + 0 
        
        '''
        if self.view.product_code.get().strip() == '' or self.view.price.get().strip() == '' or self.view.supplier.get().strip() == '':
            self.view.message('showinfo', ' خطاء', 'يرجى عدم ترك الحقول فارغة')
            return False
        
        if self.model.check_product_code_exist(self.view.product_code.get().strip()):
            self.view.message('showinfo', 'عملية فاشلة', 'كود المنتج موجود بالفعل')
            return False
        
        if float(self.view.price.get()) <= 0.0:
            self.view.message('showinfo', 'عملية فاشلة', 'سعر المنتج يجب ان يكون اكبر من 0')
            return False
        
        return True


    def clear_inputs(self):
        self.view.product_code.set('')
        self.view.price.set('')
        self.view.supplier.set('snow white')