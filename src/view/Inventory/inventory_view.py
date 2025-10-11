import customtkinter as ctk
from tkinter import messagebox

class InventoryView(ctk.CTkFrame):
    def __init__(self, root, get_distributors_func):
        """create the inventory main frame and adding navigation buttons

        Args:
            root (ctk.CTk): this is the root window of the application but contains the side bar frame
            get_distributors_func (function): to get the list of distributors names from model
        """
        super().__init__(root,)
        self.pack(fill='both', expand=True)
        self.buttons = []
        self.Frames = []
        self.distributors = get_distributors_func # to get the list of distributors names from model 
        self.create_options_buttons()


    def create_options_buttons(self):
        options_frame = ctk.CTkFrame(self, width=200, corner_radius=5,height=30)
        options_frame.pack(side='top', padx=10)
        options = ['كل الموزعين'] + self.distributors() + ['الرئيسية']
        for option in options:
            button = ctk.CTkButton(options_frame, text=option,  font=("Arial", 16, "bold"), width=200, height=40)
            button.pack(side= 'left',padx=10)
            self.buttons.append(button)


    def create_password_popup(self):
        popup = ctk.CTkToplevel(self.master, )
        popup.grab_set()
        popup.geometry(f'+900+450')
        
        self.password = None
        
        ctk.CTkLabel(popup, text='ادخل كلمة المرور', font=("Arial", 14)).pack(pady=10, padx=20)
        entry = ctk.CTkEntry(popup, show='*')
        entry.pack(pady=10, padx=20)
        
        button_frame = ctk.CTkFrame(popup, fg_color="transparent")
        button_frame.pack(pady=10)
        
        ok_btn = ctk.CTkButton(button_frame, text="موافق", command=lambda ent= entry, popup=popup: self.pop_on_ok(popup=popup, entry=ent) )
        ok_btn.pack(side="left", padx=10)
        cnl_btn =ctk.CTkButton(button_frame, text="إلغاء", command=popup.destroy)
        cnl_btn.pack(side="left", padx=10)
        
        popup.bind('<Return>', lambda event: ok_btn.invoke())
        popup.bind("<Escape>", lambda event: cnl_btn.invoke())
        popup.after(4, entry.focus_set)
        
        # block the code untill the popup is destroyed # i used it to change the password before return it .
        self.master.wait_window(popup)
        return self.password
        
    def pop_on_ok(self, popup, entry):
        self.password =entry.get()
        popup.destroy()
        

    def message(self, mstype, info_text, text):
        if mstype == "yes_no":
            return messagebox.askyesno(info_text, text)
        elif mstype == "showinfo":
            messagebox.showinfo(info_text, text)

