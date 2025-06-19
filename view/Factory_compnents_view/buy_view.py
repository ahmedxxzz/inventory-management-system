import customtkinter as ctk
from tkinter import StringVar, ttk , messagebox


class BuyView(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root)
        self.pack(fill='both', expand=True)
        self.Entries = []
        self.recommendation_buttons = []
        self.recommendations = []
        
        self.temp_operations = []
        self.temp_operations_buttons = []
        
        
        self.fac_name = StringVar()
        self.product_code = StringVar()
        self.price = StringVar()
        self.quantity = StringVar()
        self.discount = StringVar()
        self.supplier = StringVar()
        self.supplier.set('snow white')
        
        

        
        self.create_upper_frame()
        self.create_bottom_frame()


    def create_upper_frame(self):
        upper_frame = ctk.CTkFrame(self, corner_radius=5,border_width=5,border_color='yellow')
        upper_frame.pack(side='top', padx=10, fill='x')

        
        entry_frame = ctk.CTkFrame(upper_frame, border_width=2)
        entry_frame.pack(side='left', padx=10,pady=10,)
        
         
        inputs_lbls_frame = ctk.CTkFrame(entry_frame)
        inputs_lbls_frame.pack(side='left', fill='y')
        lbls_names = ['اسم المصنع', 'كود القطعة', 'سعر القطعة', 'عدد القطع', 'الخصم', 'الموزع']
        
        for lbl in lbls_names:
            lbl = ctk.CTkLabel(inputs_lbls_frame, text=lbl, font=("Arial", 14, "bold"), text_color='white',width=200, height=40)
            lbl.pack(side='top', padx=10, pady=10)
        
        
        inputs_entries_frame = ctk.CTkFrame(entry_frame)
        inputs_entries_frame.pack(side='right', fill='y')
        
        
        entry_variables = [self.fac_name, self.product_code, self.price, self.quantity, self.discount]
        for var in entry_variables:
            fac_entry = ctk.CTkEntry(inputs_entries_frame, textvariable=var, font=("Arial", 18, "bold"),width=200, height=40, justify='right' if var ==self.fac_name else 'left', )
            fac_entry.pack(side='top', padx=10, pady=10)
            self.Entries.append(fac_entry)
            
            if var != self.fac_name and var != self.product_code :
                fac_entry.configure(validate="key", validatecommand = (fac_entry.register(self.validate_Entry), '%P', 'float' if var !=self.quantity else 'integer'))
        
        ctk.CTkOptionMenu(inputs_entries_frame,variable=self.supplier ,values=['snow white', 'golden rose'], font=("Arial", 18, "bold"),width=200, height=40, state='readonly').pack(side='top', padx=10, pady=10)
        
        self.save_buys_button = ctk.CTkButton(inputs_lbls_frame, text='حفظ الفاتورة', font=("Arial", 18, "bold"),width=200, height=40,)
        self.save_buys_button.pack(side='top', padx=10, pady=10)
        
        self.cache_buy_button = ctk.CTkButton(inputs_entries_frame, text='اضافة الى الفاتورة', font=("Arial", 18, "bold"),width=200, height=40,)
        self.cache_buy_button.pack(side='top', padx=10, pady=10)
        
        ###### Recommendation frame
        self.recommended_frame = ctk.CTkScrollableFrame(upper_frame, width=170,height=300 ,corner_radius=5, border_width=0, fg_color='transparent',scrollbar_button_color='#333333', scrollbar_button_hover_color='#333333', scrollbar_fg_color='#333333')
        self.recommended_frame.pack(side='left', padx=10,pady=30)
        
        ##### Temp Operations Frame
        self.temp_operations_frame = ctk.CTkScrollableFrame(upper_frame, width=170,height=400 ,corner_radius=5, border_width=0, fg_color='transparent',scrollbar_button_color='#333333', scrollbar_button_hover_color='#333333', scrollbar_fg_color='#333333')
        self.temp_operations_frame.pack(side='right', padx=10,pady=30)


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
        self.tree_columns = ('factory_name', 'date', 'piece_type', 'price', 'quantity', 'discount', 'total_price')
        self.tree_headers = ['اسم المصنع', 'التاريخ', 'نوع القطعة', 'السعر', 'الكمية', 'الخصم', 'السعر الكلي']

        self.tree = ttk.Treeview(bottom_frame, columns=self.tree_columns, show='headings', selectmode="extended")
        
        # Define headers and bind the sort function to each
        for i, col in enumerate(self.tree_columns):
            self.tree.heading(col, text=self.tree_headers[i], anchor='center',command=lambda c=col: self.sort_column(c, False))
        
        
        # Define column widths (adjust as needed)
        self.tree.column('factory_name', width=60, anchor='center')
        self.tree.column('date', width=170, anchor='center')
        self.tree.column('piece_type', width=150, anchor='w')
        self.tree.column('price', width=100, anchor='center')
        self.tree.column('quantity', width=80, anchor='center')
        self.tree.column('discount', width=80, anchor='center')
        self.tree.column('total_price', width=100, anchor='center')

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
            

    def message(self,info_text, text):
        messagebox.showinfo(info_text, text)
    

    def check_inputs_before_caching(self):
        for  ent in [self.fac_name, self.product_code, self.price, self.quantity, self.discount, self.supplier]:
            if ent !=self.discount:
                if ent.get() == '':
                    messagebox.showerror("خطأ", "لا يمكن ترك الحقول فارغة")
                    return
        if self.discount.get() != '':
            if float(self.price.get())<= float(self.discount.get()):
                messagebox.showerror("خطأ", "لا يمكن ان يكون الخصم اكبر من السعر")
                return
        
        if float(self.price.get())<= 0:
            messagebox.showerror("خطأ", "لا يمكن ان يكون السعر اقل من او يساوى صفر")
            return
        
        if int(self.quantity.get())< 1:
            messagebox.showerror("خطأ", "لا يمكن ان يكون الكمية اقل من 1")
            return
        return True


    def add_temp_operation_button(self):
        button = ctk.CTkButton(self.temp_operations_frame, text=self.product_code.get())
        button.pack(side='top', padx=10, pady=10)
        self.temp_operations_buttons.append(button)
        return button


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


    def recommendation_focusIn(self, var):
            for btn_text in self.recommendations:
                button = ctk.CTkButton(self.recommended_frame, text=btn_text,width=200, height=40, command=lambda btn_text=btn_text: var.set(btn_text))
                button.pack(side='top', padx=10, pady=10)
                self.recommendation_buttons.append(button)

  
    def recommendation_KeyRelease(self, var, matching_items):
        for btn_text in matching_items:
                    button = ctk.CTkButton(self.recommended_frame, text=btn_text,width=200, height=40, command=lambda btn_text=btn_text: var.set(btn_text))
                    button.pack(side='top', padx=10, pady=10)
                    self.recommendation_buttons.append(button)


