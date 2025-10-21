import os
import shutil
import uuid
from model.distributor_model import DistributorModel
from view.distributor_view import DistributorView

class DistributorController:
    def __init__(self, root, db_conn):
        self.root = root
        self.db_conn = db_conn
        self.model = DistributorModel(self.db_conn)
        self.view = DistributorView(root)
        self.distributer_id = None
        # This will hold the full path of a NEWLY selected image file for the current operation.
        self._newly_selected_logo_path = None
        self._bind_events()
    
    def _bind_events(self):
        self.view.populate_treeview(self.model.get_distributors())
        self.view.bind_table(self.get_selected_distributor)
        self.view.browse_button.configure(command=self._browse_and_set_path)
        
        buttons_map = {'اضافة': self.add_distributor, 'حذف': self.delete_distributor,
                         'تعديل': self.update_distributor, 'تنظيف المدخلات': self.clear_inputs}
        for button in self.view.buttons:
            button.configure(command=lambda title=button.cget("text"): buttons_map[title]())
    
    def _browse_and_set_path(self):
        """Handles the file dialog and updates the UI and internal state."""
        file_path = self.view.browse_for_image()
        if file_path:
            self._newly_selected_logo_path = file_path
            self.view.logo_path_var.set(os.path.basename(file_path))

    def _copy_image_and_get_path(self, source_path):
        """Copies an image to a local project folder and returns the new relative path."""
        if not source_path or not os.path.exists(source_path): return None
        dest_folder = "Z_Files/images"
        os.makedirs(dest_folder, exist_ok=True)
        _, extension = os.path.splitext(source_path)
        unique_filename = f"logo_{uuid.uuid4().hex}{extension}"
        destination_path = os.path.join(dest_folder, unique_filename)
        try:
            shutil.copy(source_path, destination_path)
            return destination_path.replace("\\", "/")
        except Exception as e:
            self.view.message("showinfo", "خطأ في النسخ", f"فشل نسخ ملف الصورة: {e}")
            return None

    def _delete_logo_file(self, logo_path):
        """Safely deletes a logo file if it exists."""
        if logo_path and os.path.exists(logo_path):
            try:
                os.remove(logo_path)
            except Exception as e:
                self.view.message("showinfo", "تنبيه", f"لم يتمكن البرنامج من حذف الصورة القديمة:\n{e}")

    def add_distributor(self):
        distributor_name = self.view.distributor_name_var.get().strip()
        if not distributor_name:
            return self.view.message("showinfo", "خطأ", "يرجى إدخال اسم الموزع")
        if self.model.distributor_exists(distributor_name): 
            return self.view.message("showinfo", "خطأ", "اسم الموزع موجود بالفعل")
        
        final_logo_path = None
        if self._newly_selected_logo_path:
            final_logo_path = self._copy_image_and_get_path(self._newly_selected_logo_path)
        
        is_true, error = self.model.add_distributor(distributor_name, final_logo_path)
        if is_true:
            self.view.message("showinfo", "نجاح", "تم إضافة الموزع بنجاح")
            self.clear_inputs()
            self.view.populate_treeview(self.model.get_distributors())
        else:
            self.view.message("showinfo", "خطأ", f"حدث خطأ أثناء الإضافة: {error}")

    def update_distributor(self):
        if not self.distributer_id:
            return self.view.message("showinfo", "خطأ", "يرجى اختيار الموزع المراد تعديله")
            
        new_name = self.view.distributor_name_var.get().strip()
        if not new_name:
            return self.view.message("showinfo", "خطأ", "يرجى إدخال اسم الموزع الجديد")
        if self.model.new_distributor_name_exist(self.distributer_id, new_name):
            return self.view.message("showinfo", "خطأ", "اسم الموزع موجود بالفعل")

        # Get the original data from DB to know the old logo path
        old_data = self.model.get_distributor_by_id(self.distributer_id)
        old_logo_path = old_data[1] if old_data else None
        
        final_logo_path = old_logo_path # Start with the old path as default

        # If a new logo was selected during this operation, process it
        if self._newly_selected_logo_path:
            new_path = self._copy_image_and_get_path(self._newly_selected_logo_path)
            if new_path: # If copy was successful
                self._delete_logo_file(old_logo_path) # Delete the old file
                final_logo_path = new_path # Set the final path to the new one
        
        is_true, error = self.model.update_distributor(self.distributer_id, new_name, final_logo_path)
        if is_true:
            self.view.message("showinfo", "نجاح", "تم تعديل بيانات الموزع بنجاح")
            self.clear_inputs()
            self.view.populate_treeview(self.model.get_distributors())
        else:
            self.view.message("showinfo", "خطأ", f"حدث خطأ أثناء التعديل: {error}")

    def clear_inputs(self):
        self.view.distributor_name_var.set('')
        self.view.logo_path_var.set('')
        self.distributer_id = None
        self._newly_selected_logo_path = None # Reset the state
        if self.view.tree.selection():
            self.view.tree.selection_remove(self.view.tree.selection()[0])

    def get_selected_distributor(self, row_values):
        if row_values:
            # The order in the view tree is ('logo_path', 'distributor_name')
            dist_name, logo_path  = row_values[0], row_values[1]
            self.view.distributor_name_var.set(dist_name)
            self.view.logo_path_var.set(logo_path) # Display the relative path from DB
            self.distributer_id = self.model.get_distributor_id(dist_name)
            self._newly_selected_logo_path = None # IMPORTANT: Reset state on new selection
            
    def delete_distributor(self):
        if self.distributer_id:
            if self.view.message("yes_no", "تأكيد الحذف", "هل تريد حذف الموزع وكل البيانات المرتبطة به؟ سيتم حذف الصورة نهائياً."):
                # The model now handles deleting the file as well
                is_true, error = self.model.delete_distributor(self.distributer_id)
                if is_true:
                    self.view.message("showinfo", "نجاح", "تم حذف الموزع بنجاح")
                    self.clear_inputs()
                    self.view.populate_treeview(self.model.get_distributors())
                else:
                    self.view.message("showinfo", "خطأ", f"حدث خطأ أثناء الحذف: {error}")
        else:
            self.view.message("showinfo", "خطأ", "يرجى اختيار الموزع المراد حذفه")