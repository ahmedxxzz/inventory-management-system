import customtkinter as ctk
from tkinter import StringVar, ttk , messagebox

class CustomerAccountView(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root)
        self.pack(fill='both', expand=True)
        
        self.cus_frames = []
        
        self.search_var = StringVar()
        self.cus_name = StringVar()
        self.amount_money = StringVar()
        self.product_quantity = StringVar()
        
        
        
        self.create_upper_frame()
        self.create_bottom_frame()


    def create_upper_frame(self):
        upper_frame = ctk.CTkFrame(self, corner_radius=5,border_width=5,border_color='yellow')
        upper_frame.pack(side='top',  padx=10, fill='x')
        
        #########################################
        search_frame = ctk.CTkFrame(upper_frame)
        search_frame.pack(side='top', pady=10, padx=50, fill='x',expand=True)
        
        search_lbl = ctk.CTkLabel(search_frame, text='بحث', font=("Arial", 16, "bold"), text_color='white',width=200, height=40)
        search_lbl.pack(side='right', padx=10, pady=10)

        self.search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var, font=("Arial", 16, "bold"), height= 40, justify='right')
        self.search_entry.pack(side='right',  padx=(50,), pady=10, fill='x', expand=True)

        #########################################

        adding_cus_frame = ctk.CTkFrame(upper_frame,)
        adding_cus_frame.pack(side='top', pady=10, padx=10, fill='x')
        
        self.adding_btn = ctk.CTkButton(adding_cus_frame, text='اضافة مصنع جديد', font=("Arial", 16, "bold"), text_color='white',width=200, height=40, fg_color='green',)
        self.adding_btn.pack(side='right', padx=10, pady=10)
        
        
        lbls = ['اسم المكتب', 'المبلغ المستحق', 'كمية القطع']
        ents = [self.cus_name, self.amount_money, self.product_quantity]
        for i in range(0, len(lbls)):
            lbl = ctk.CTkLabel(adding_cus_frame, text=lbls[i], font=("Arial", 16, "bold"), text_color='white',width=200, height=40)
            lbl.pack(side='right', pady=10)
            
            ent = ctk.CTkEntry(adding_cus_frame, textvariable=ents[i], font=("Arial", 16, "bold"), height= 40, justify='right')
            ent.pack(side='right',  padx=10, pady=10, fill='x', expand=True)
            if i != 0:
                ent.configure(validate = 'key', validatecommand=(ent.register(self.validate_Entry), '%P', 'float' if ents[i] ==self.amount_money else 'integer'))



    def create_bottom_frame(self):
        bottom_frame = ctk.CTkFrame(self, corner_radius=5,border_width=5)
        bottom_frame.pack(side='bottom', fill='both', expand=True)
        #########################################
        header_frame = ctk.CTkFrame(bottom_frame, width=200, corner_radius=5,height=30)
        header_frame.pack(side='top',  fill='x')
        for i in range(0, 10):
            header_frame.grid_columnconfigure(i, weight=1)
        header_frame.grid_rowconfigure(0, weight=0)
        
        lbls = ['اسم المكتب', 'المبلغ المستحق', 'الكمية         ']
        for i in range(0, len(lbls)):
            lbl = ctk.CTkLabel(header_frame, text=lbls[i], font=("Arial", 14, "bold"), text_color='white',width=120, height=40, )
            lbl.grid(row=0, column=i*2,  pady=10)
        #########################################
        self.bottom_frame = ctk.CTkScrollableFrame(bottom_frame,  )
        self.bottom_frame.pack(side='bottom',  padx=10, fill='both', expand=True)
        
        #########################################



    def add_customer_frame(self, cus_name, amount_money, product_quantity, zeros_func, report_class):
        cus_frame = ctk.CTkFrame(self.bottom_frame, border_width=1,  height=40, )
        cus_frame.pack(side='top', fill='x')
        for i in range(0, 10):
            cus_frame.grid_columnconfigure(i, weight=2 if i in [0, 2, 4] else 1)

        cus_frame.grid_rowconfigure(0, weight=0)

        #########################################

        report_button = ctk.CTkButton(cus_frame, text='كشف حساب', font=("Arial", 14, "bold"), text_color='white',width=100, height=40, fg_color='green', command=lambda cus_name = cus_name: report_class(cus_name))
        report_button.grid(row=0, column=9, pady=10)

        
        zeros_button = ctk.CTkButton(cus_frame, text='تصفير الحساب', font=("Arial", 14, "bold"), text_color='white',width=100, height=40, fg_color='red', command=lambda cus_name = cus_name: zeros_func(cus_name))
        zeros_button.grid(row=0, column=8, pady=10, sticky="e")


        lbls = [cus_name, amount_money, product_quantity]
        for i in range(0, len(lbls)):    
            lbl = ctk.CTkLabel(cus_frame, text=lbls[i], font=("Arial", 14, "bold"), text_color='white',width=120, height=40, )
            lbl.grid(row=0, column=i*2, pady=10,)

        
        self.cus_frames.append(cus_frame)


    def delete_customer_frames(self):
        for frame in self.cus_frames:
            frame.destroy()
        self.cus_frames = []


    def validate_Entry(self, value, op_type):
        """Validate amount entry to allow only numbers and decimals."""
        if op_type == "integer":
            if value == "":
                return True
            try:
                int(value)
                return True
            except ValueError:
                return False
        elif op_type == "float":
            if value == "":
                return True
            try:
                float(value)
                return True
            except ValueError:
                return False
        elif op_type == "":
            return True


    def message(self, mstype, info_text, text):
        if mstype == "yes_no":
            return messagebox.askyesno(info_text, text)
        elif mstype == "showinfo":
            messagebox.showinfo(info_text, text)
