from view.safe_view import SafeView
from model.safe_model import SafeModel

class SafeController:
    def __init__(self, root_window):
        self.root = root_window
        self.view = SafeView(self.root)
        self.model = SafeModel()
        
        self._bind_events()
        self.view.populate_treeview(self.model.get_safes_info()) 

    
    def _bind_events(self):
        self.view.search_entry.bind('<KeyRelease>', lambda event: self.search_key_release())
        self.view.tree.bind('<Double-1>', lambda event: self.select_safe())
        
        # btns = ['اضافة', 'حذف', 'تعديل', 'تنظيف المدخلات']
        for i, btn in enumerate(self.view.buttons):
            if i == 0:
                btn.configure(command=self.adding_safe)
            elif i == 1:
                btn.configure(command=self.delete_safe)
            elif i == 2:
                btn.configure(command=self.edit_safe)
            elif i == 3:
                btn.configure(command=self.clear_inputs)


    def search_key_release(self):
        self.view.populate_treeview(self.model.get_safes_info(self.view.search_var.get().strip()))
    
    
    def select_safe(self):
        selected_item = self.view.tree.focus()
        if selected_item:
            row_data = self.view.tree.item(selected_item)['values'] # [2, 'vodafone cash', '50000.0']
            self.view.safe_name.set(row_data[1])
            self.view.amount_money.set(row_data[2])


    def adding_safe(self):
        if self.check_inputs():
            if self.model.adding_new_safe(self.view.safe_name.get(), float(self.view.amount_money.get())):
                self.view.message('showinfo', 'عملية ناجحة', 'تمت عملية الاضافة بنجاح')
                self.clear_inputs()
                self.view.populate_treeview(self.model.get_safes_info())


    def check_inputs(self):
        if self.view.safe_name.get().strip() == '' or self.view.amount_money.get().strip() == '':
            self.view.message('showinfo', ' خطاء', 'يرجى عدم ترك الحقول فارغة')
            return False

        if self.model.check_safe_name_exist(self.view.safe_name.get()):
            self.view.message('showinfo', 'عملية فاشلة', 'اسم الخزنة موجود بالفعل')
            return False
        
        
        return True


    def clear_inputs(self):
        self.view.search_var.set('')
        self.view.safe_name.set('')
        self.view.amount_money.set('')
        self.view.populate_treeview(self.model.get_safes_info())


    def delete_safe(self):
        if self.view.safe_name.get().strip() != '':
            if self.model.check_safe_name_exist(self.view.safe_name.get()):
                if self.view.message('yes_no', 'حذف', 'هل تريد حذف الخزنة؟ '):
                    if self.model.delete_safe(self.view.safe_name.get().strip()):
                        self.view.message('showinfo', 'عملية ناجحة', 'تمت عملية الحذف بنجاح')
                        self.clear_inputs()
                        self.view.populate_treeview(self.model.get_safes_info())
                    else:
                        self.view.message('showinfo', 'عملية فاشلة', 'لم يتم حذف الخزنة')
            else:
                self.view.message('showinfo', 'عملية فاشلة', 'اسم الخزنة غير موجود')

        else:
            self.view.message('showinfo', 'عملية فاشلة', 'يرجى عدم ترك الحقول فارغة')


    def edit_safe(self):
        if self.view.safe_name.get().strip() != '':
            if self.model.check_safe_name_exist(self.view.safe_name.get()):
                if self.view.message('yes_no', 'تعديل', 'هل تريد تعديل الخزنة؟ '):
                    if self.model.update_safe(self.view.safe_name.get().strip(), float(self.view.amount_money.get())):
                        self.view.message('showinfo', 'عملية ناجحة', 'تمت عملية التعديل بنجاح')
                        self.clear_inputs()
                        self.view.populate_treeview(self.model.get_safes_info())
                    else:
                        self.view.message('showinfo', 'عملية فاشلة', 'لم يتم تعديل الخزنة')
            else:
                self.view.message('showinfo', 'عملية فاشلة', 'اسم الخزنة غير موجود')

        else:
            self.view.message('showinfo', 'عملية فاشلة', 'يرجى عدم ترك الحقول فارغة')


