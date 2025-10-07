from model.distributor_model import DistributorModel
from view.distributor_view import DistributorView

class DistributorController:
    def __init__(self, root, db_conn):
        self.root = root
        self.db_conn = db_conn
        self.model = DistributorModel(self.db_conn)
        self.view = DistributorView(root)
        self.distributer_id = None
        self._bind_events()
    
    
    def _bind_events(self):
        self.view.populate_treeview(self.model.get_distributors())
        
        self.view.bind_table(self.get_selected_distributor)
        
        buttons_maping = {
            'اضافة': self.add_distributor,
            'حذف': self.delete_distributor,
            'تعديل': self.update_distributor,
            'تنظيف المدخلات': self.clear_inputs,
        }
        
        for button in self.view.buttons:
            button.configure(command= lambda  title= button.cget("text"): buttons_maping[title]())
    
        
    
    def add_distributor(self):
        """add distributor to database

        Steps:
            # get distributor information from view
            # check if inputs are empty
            # check if distributor exists
            # add distributor to database
            # update treeview
            # clear inputs and set distributor id = None
            # show success message
        """
        distributor_name = self.view.distributor_name_var.get()
        if distributor_name == '':
            return self.view.message("showinfo", "خطأ", "يرجى إدخال اسم الموزع")
        
        if self.model.distributor_exists(distributor_name): 
            return self.view.message("showinfo", "خطأ", "اسم الموزع موجود بالفعل")
        
        is_true, error = self.model.add_distributor(distributor_name)
        self.view.message("showinfo", "نجاح" if is_true else "خطأ", "تم إضافة الموزع بنجاح" if is_true else f'حدث خطأ اثناء اضافة الموزع: {error}')
        
        self.view.populate_treeview(self.model.get_distributors())
        if is_true:
            self.view.distributor_name_var.set('')
            self.distributer_id = None


    def delete_distributor(self):
        """delete distributor from database

        Steps:
            # check if distributor id is selected
            # sure to delete
            # delete distributor from database
            # update treeview
            # clear inputs and distributor id = None
            # show success message
        """
        if self.distributer_id:
            if self.view.message("yes_no", "تأكيد", "هل تريد حذف الموزع"):
                is_true, error = self.model.delete_distributor(self.distributer_id)
                self.view.message("showinfo", "نجاح" if is_true else "خطأ", "تم حذف الموزع بنجاح" if is_true else f'حدث خطأ اثناء حذف الموزع: {error}')
                
                self.view.populate_treeview(self.model.get_distributors())
                if is_true:
                    self.view.distributor_name_var.set('')
                    self.distributer_id = None
        else:
            return self.view.message("showinfo", "خطأ", "يرجى اختيار الموزع المراد حذفه")


    def update_distributor(self):
        """update distributor name in database

        Steps:
            # check if distributor id is selected
            # get new distributor name from view
            # check if distributor name is empty
            # check if distributor exists with other id than selected
            # update distributor name in database
            # update treeview
            # clear inputs and distributor id = None
            # show success message
        """
        if self.distributer_id:
            new_distributor_name = self.view.distributor_name_var.get()
            if new_distributor_name == '':
                return self.view.message("showinfo", "خطأ", "يرجى إدخال اسم الموزع الجديد")
            
            if self.model.new_distributor_name_exist(self.distributer_id, new_distributor_name):
                return self.view.message("showinfo", "خطأ", "اسم الموزع موجود بالفعل")
            
            is_true, error = self.model.update_distributor(self.distributer_id, new_distributor_name)
            self.view.message("showinfo", "نجاح" if is_true else "خطأ", "تم تعديل اسم الموزع بنجاح" if is_true else f'حدث خطأ اثناء تعديل اسم الموزع: {error}')
            
            self.view.populate_treeview(self.model.get_distributors())
            if is_true:
                self.view.distributor_name_var.set('')
                self.distributer_id = None
        else:
            return self.view.message("showinfo", "خطأ", "يرجى اختيار الموزع المراد تعديله")


    def clear_inputs(self):
        self.view.distributor_name_var.set('')
        self.distributer_id = None
        self.view.message("showinfo", "نجاح", "تم تنظيف المدخلات ")
        self.view.populate_treeview(self.model.get_distributors())


    def get_selected_distributor(self, row_values):
        if row_values:
            self.view.distributor_name_var.set(row_values[0])
            self.distributer_id = self.model.get_distributor_id(row_values[0])[0]

