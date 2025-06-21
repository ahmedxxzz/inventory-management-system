import customtkinter as ctk
from tkinter import StringVar, ttk , messagebox

class PayView(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root, )
        self.pack(fill='both', padx=10,expand=True)
        self.fac_name = StringVar()
        self.safe_type = StringVar()
        self.safe_type.set('cash')
        self.money_amount = StringVar()
        
        self.recommendation_frames = []
        self.recommendations = []
        
        
        
        self.create_upper_frame()
        self.create_bottom_frame()


    def create_upper_frame(self):
        upper_frame = ctk.CTkFrame(self, corner_radius=5,border_width=5,border_color='yellow',height=450)
        upper_frame.pack(side='top', fill='x')
        
        sub_upper_frame = ctk.CTkFrame(upper_frame, bg_color='#333333', fg_color='#333333',width=560, height=400)
        sub_upper_frame.pack(side='top',pady=10,)
        
        inputs_frame = ctk.CTkFrame(sub_upper_frame, fg_color='#333333')
        inputs_frame.pack(side='left', padx=10,pady=10,)
        
        upper_input_frame = ctk.CTkFrame(inputs_frame, border_width=2)
        upper_input_frame.pack(side='top', padx=10,pady=10,)
        
        inputs_lbls_frame = ctk.CTkFrame(upper_input_frame,  fg_color='#333333')
        inputs_lbls_frame.pack(side='left', fill='y')
        lbls_names = ['اسم المصنع', 'نوع الخزنة', 'مبلغ الدفع']

        for lbl in lbls_names:
            lbl = ctk.CTkLabel(inputs_lbls_frame, text=lbl, font=("Arial", 14, "bold"), text_color='white',width=200, height=40)
            lbl.pack(side='top', padx=10, pady=10)
        
        inputs_entries_frame = ctk.CTkFrame(upper_input_frame, fg_color='#333333')
        inputs_entries_frame.pack(side='right', fill='y')
        
        entry_variables = [self.fac_name, self.money_amount]
        for var in entry_variables:
            fac_entry = ctk.CTkEntry(inputs_entries_frame, textvariable=var, font=("Arial", 18, "bold"),width=200, height=40, justify='right' if var ==self.fac_name else 'left', )
            fac_entry.pack(side='top', padx=10, pady=10)
            if var == self.fac_name:
                self.fac_name_entry = fac_entry
                ctk.CTkOptionMenu(inputs_entries_frame,variable=self.safe_type ,values=['cash', 'vodafone cash'], font=("Arial", 18, "bold"),width=200, height=40, state='readonly').pack(side='top', padx=10, pady=10)
            
            if var == self.money_amount:
                fac_entry.configure(validate="key", validatecommand = (fac_entry.register(self.validate_Entry), '%P', 'float'))
        
        
        frame_pay_button = ctk.CTkFrame(inputs_frame, fg_color='#333333')
        frame_pay_button.pack(side='top', padx=10,pady=10,)
        
        self.button = ctk.CTkButton(frame_pay_button, text='دفع', font=("Arial", 16, "bold"), width=200, height=40)
        self.button.pack(side='top', pady=10)
        
        
        ######## recommendation frame 
        self.recommended_frame = ctk.CTkScrollableFrame(sub_upper_frame, width=200,height=250,border_width=5, border_color='#333333' ,corner_radius=5, fg_color='transparent',scrollbar_button_color='#333333', scrollbar_button_hover_color='#333333', scrollbar_fg_color='#333333')
        self.recommended_frame.pack(side='left', padx=10,pady=30)



    def create_bottom_frame(self):
        """Creates the frame containing the Treeview for displaying data."""
        bottom_frame = ctk.CTkFrame(self, corner_radius=5)
        bottom_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Make the grid layout responsive
        bottom_frame.grid_rowconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(0, weight=1)

        # --- Style the Treeview to match the CustomTkinter dark theme ---
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",background="#2b2b2b",foreground="white",rowheight=25,fieldbackground="#2b2b2b",bordercolor="#343638",borderwidth=0)
        style.map('Treeview', background=[('selected', '#2a2d2e')])

        # Configure the Treeview Heading colors
        style.configure("Treeview.Heading",background="#565b5e",foreground="white",relief="flat",font=('Arial', 12, 'bold'))
        style.map("Treeview.Heading",background=[('active', '#3484F0')])

        # --- Create Treeview Widget ---
        self.tree_columns = ('factory_name', 'date', 'money', 'money_before', 'money_after')
        self.tree_headers = ['الحساب بعد الدفع', 'الحساب قبل الدفع', 'الاموال المدفوعة', 'التاريخ', 'اسم المصنع']

        self.tree = ttk.Treeview(bottom_frame, columns=self.tree_columns, show='headings', selectmode="extended")
        
        # Define headers and bind the sort function to each
        for i, col in enumerate(self.tree_columns):
            self.tree.heading(col, text=self.tree_headers[i], anchor='center',command=lambda c=col: self.sort_column(c, False))
        
        
        # Define column widths (adjust as needed)
        self.tree.column('factory_name', width=80, anchor='center')
        self.tree.column('date', width=180, anchor='center')
        self.tree.column('money', width=120, anchor='w')
        self.tree.column('money_before', width=150, anchor='center')
        self.tree.column('money_after', width=150, anchor='center')

        # --- Add Scrollbars ---
        v_scrollbar = ttk.Scrollbar(bottom_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(bottom_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Place widgets in the grid
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')



    def populate_treeview(self, data):
        """Clears the tree and inserts new data."""
        # Clear existing items in the tree
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Insert new data rows (in reverse for correct visual order)
        for row_data in data:
            visual_row = row_data[::-1]
            self.tree.insert("", "end", values=visual_row)


    def sort_column(self, col, reverse):
        """Sorts a treeview column when the header is clicked."""
        try:
            data = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        except Exception:
            return
            
        data.sort(key=lambda t: self.get_sort_key(t[0]), reverse=reverse)
        
        # Rearrange items in the tree
        for index, (val, k) in enumerate(data):
            self.tree.move(k, '', index)
            
        # Update the header text to show sort direction (▲/▼)
        for c in self.tree_columns:
            # Get original header text
            header_text = self.tree.heading(c, 'text').replace(' ▲', '').replace(' ▼', '')
            if c == col:
                header_text += ' ▲' if reverse else ' ▼'
            self.tree.heading(c, text=header_text)

        # Reverse the sort direction for the next click on this column
        self.tree.heading(col, command=lambda: self.sort_column(col, not reverse))


    def get_sort_key(self,value):
        """Helper function to convert values for sorting."""
        try:
            return float(str(value).replace(',', ''))
        except (ValueError, TypeError):
            return str(value).lower()



    def recommendation_focusIn(self, var):
            for btn_text, amount_money in self.recommendations:
                frame = ctk.CTkFrame(self.recommended_frame, fg_color='transparent', border_width=0, width=200, height=40)
                frame.pack(side='top', padx=10, pady=10)
                button = ctk.CTkButton(frame,text=btn_text,width=100,  height=35,fg_color="#4CAF50", hover_color="#45a049",text_color="yellow",border_width=2,border_color="#388E3C", corner_radius=10,command=lambda btn_text=btn_text: var.set(btn_text))
                button.pack(side='left', padx=(0, 5))
                money_lbl = ctk.CTkLabel(frame,text=amount_money,width=80,height=35,font=("Arial", 14, "bold"),text_color='white',fg_color="#007BFF", corner_radius=5)
                money_lbl.pack(side='right', padx=(5, 0))
                self.recommendation_frames.append(frame)


    def recommendation_KeyRelease(self, var, matching_items):
        for fac, amount_money in matching_items:
            frame = ctk.CTkFrame(self.recommended_frame, fg_color='transparent', border_width=0, width=200, height=40)
            frame.pack(side='top', padx=10, pady=10)
            button = ctk.CTkButton(frame,text=fac,width=100,  height=35,fg_color="#4CAF50", hover_color="#45a049",text_color="yellow",border_width=2,border_color="#388E3C", corner_radius=10,command=lambda btn_text=fac: var.set(btn_text))
            button.pack(side='left', padx=(0, 5))
            money_lbl = ctk.CTkLabel(frame,text=amount_money,width=80,height=35,font=("Arial", 14, "bold"),text_color='white',fg_color="#007BFF", corner_radius=5)
            money_lbl.pack(side='right', padx=(5, 0))
            
            self.recommendation_frames.append(frame)


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

    def clear_inputs(self):
        self.fac_name.set('')
        self.money_amount.set('')
        self.safe_type.set('cash')
        