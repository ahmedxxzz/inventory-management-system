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
        # This variable will hold the path selected by the user, which might be temporary.
        self._selected_logo_source_path = None
        self._bind_events()
    
    def _bind_events(self):
        self.view.populate_treeview(self.model.get_distributors())
        self.view.bind_table(self.get_selected_distributor)
        # Bind the browse button to its own handler in the controller
        self.view.browse_button.configure(command=self._browse_and_set_path)
        
        buttons_maping = {'اضافة': self.add_distributor, 'حذف': self.delete_distributor,
                          'تعديل': self.update_distributor, 'تنظيف المدخلات': self.clear_inputs}
        for button in self.view.buttons:
            button.configure(command=lambda title=button.cget("text"): buttons_maping[title]())
    
    def _browse_and_set_path(self):
        """Handles the file dialog and stores the selected source path."""
        # The view now returns the selected path
        file_path = self.view.browse_for_image()
        if file_path:
            # Store the original path selected by the user
            self._selected_logo_source_path = file_path
            # Display only the filename to the user for neatness
            self.view.logo_path_var.set(os.path.basename(file_path))

    def _copy_image_and_get_path(self, source_path):
        """Copies the image to the project's image folder and returns the new relative path."""
        if not source_path or not os.path.exists(source_path):
            return None

        # Define the destination folder
        dest_folder = "Z_Files/images"
        os.makedirs(dest_folder, exist_ok=True)
        
        # Create a unique filename to avoid conflicts
        _, extension = os.path.splitext(source_path)
        unique_filename = f"logo_{uuid.uuid4().hex}{extension}"
        
        destination_path = os.path.join(dest_folder, unique_filename)
        
        try:
            shutil.copy(source_path, destination_path)
            # Return the relative path to be stored in the database
            return destination_path.replace("\\", "/") # Use forward slashes for consistency
        except Exception as e:
            self.view.message("showinfo", "خطأ في النسخ", f"فشل نسخ ملف الصورة: {e}")
            return None

    def add_distributor(self):
        distributor_name = self.view.distributor_name_var.get().strip()
        if not distributor_name:
            return self.view.message("showinfo", "خطأ", "يرجى إدخال اسم الموزع")
        
        if self.model.distributor_exists(distributor_name): 
            return self.view.message("showinfo", "خطأ", "اسم الموزع موجود بالفعل")
        
        # Copy the image if a new one was selected
        final_logo_path = self._copy_image_and_get_path(self._selected_logo_source_path)
        
        is_true, error = self.model.add_distributor(distributor_name, final_logo_path)
        
        if is_true:
            self.view.message("showinfo", "نجاح", "تم إضافة الموزع بنجاح")
            self.clear_inputs()
            self.view.populate_treeview(self.model.get_distributors())
        else:
            self.view.message("showinfo", "خطأ", f"حدث خطأ أثناء إضافة الموزع: {error}")

    def update_distributor(self):
        if not self.distributer_id:
            return self.view.message("showinfo", "خطأ", "يرجى اختيار الموزع المراد تعديله")
            
        new_distributor_name = self.view.distributor_name_var.get().strip()
        if not new_distributor_name:
            return self.view.message("showinfo", "خطأ", "يرجى إدخال اسم الموزع الجديد")
        
        if self.model.new_distributor_name_exist(self.distributer_id, new_distributor_name):
            return self.view.message("showinfo", "خطأ", "اسم الموزع موجود بالفعل")

        # Determine the final logo path
        final_logo_path = self.view.logo_path_var.get() # The currently stored path
        # If the user selected a NEW image, copy it and update the path
        if self._selected_logo_source_path:
            final_logo_path = self._copy_image_and_get_path(self._selected_logo_source_path)
        
        is_true, error = self.model.update_distributor(self.distributer_id, new_distributor_name, final_logo_path)
        
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
        self._selected_logo_source_path = None # Reset the temporary path
        self.view.tree.selection_remove(self.view.tree.selection())

    def get_selected_distributor(self, row_values):
        if row_values:
            # The order from the model is (name, logo_path)
            # The order in the view tree is (logo_path, name)
            logo_path = row_values[0]
            dist_name = row_values[1]

            self.view.distributor_name_var.set(dist_name)
            self.view.logo_path_var.set(logo_path if logo_path and logo_path != 'None' else '')
            self.distributer_id = self.model.get_distributor_id(dist_name)
            self._selected_logo_source_path = None # Clear temp path when selecting from table
            
    def delete_distributor(self):
        # ... (This function remains unchanged) ...
        if self.distributer_id:
            if self.view.message("yes_no", "تأكيد", "هل تريد حذف الموزع وكل المنتجات والعمليات المرتبطة به؟"):
                is_true, error = self.model.delete_distributor(self.distributer_id)
                if is_true:
                    self.view.message("showinfo", "نجاح", "تم حذف الموزع بنجاح")
                    self.clear_inputs()
                    self.view.populate_treeview(self.model.get_distributors())
                else:
                    self.view.message("showinfo", "خطأ", f"حدث خطأ أثناء الحذف: {error}")
        else:
            return self.view.message("showinfo", "خطأ", "يرجى اختيار الموزع المراد حذفه")

