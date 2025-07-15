import customtkinter as ctk
from tkinter import StringVar, ttk, messagebox

class AdditionalCostsView(ctk.CTkFrame):

    def __init__(self, frame):
        super().__init__(frame)
        self.pack(side='top', padx=10, pady=10, fill='both',expand=True)


        self.adds_type = StringVar()
        self.price = StringVar()
        self.safe = StringVar(value='اختار الخزنة')


        self.create_upper_frame()
        self.create_bottom_frame()



    def create_upper_frame(self):
        ## get the code and the money only
        upper_frame = ctk.CTkFrame(self, corner_radius=5,border_width=5,border_color='yellow',height=450)
        upper_frame.pack(side='top', fill='x')
        
        
        inputs_frame = ctk.CTkFrame(upper_frame, corner_radius=5)
        inputs_frame.pack(side='top',pady=20,)
        ##############################################
        
        upper_input_frame = ctk.CTkFrame(inputs_frame, border_width=2, fg_color='#333333',width=560, height=400)
        upper_input_frame.pack(side='top', padx=10,pady=10,)
        
        
        
        
        ################################################
        lbls_frame = ctk.CTkFrame(upper_input_frame, fg_color='#333333',width=560, height=400)
        lbls_frame.pack(side='left', padx=10,pady=10,)
        
        lbls_names = ['نوع التكاليف', 'سعر التكاليف', 'الموزع','نوع الخزنة']
        
        for lbl in lbls_names:
            lbl = ctk.CTkLabel(lbls_frame, text=lbl, font=("Arial", 17, "bold"), text_color='white',width=200, height=40)
            lbl.pack(side='top', padx=10, pady=10)
        ################################################
        entries_frame = ctk.CTkFrame(upper_input_frame, fg_color='#333333',width=560, height=400)
        entries_frame.pack(side='right', padx=10,pady=10,)
        
        
        ctk.CTkEntry(entries_frame, textvariable=self.adds_type, font=("Arial", 18, "bold"),width=200, height=40, ).pack(side='top', padx=10, pady=10)
        ctk.CTkEntry(entries_frame, textvariable=self.price,font=("Arial", 18, "bold"),width=200, height=40, validate="key", validatecommand = (self.register(self.validate_Entry), '%P', 'float')).pack(side='top', padx=10, pady=10)
        
        
        self.safe_combo= ctk.CTkComboBox(entries_frame ,variable=self.safe)
        self.safe_combo.pack(side='top', padx=10, pady=10)
        ################################################
        self.save_btn = ctk.CTkButton(inputs_frame, text='اضافة', font=("Arial", 18, "bold"), text_color='white', fg_color="#007BFF", hover_color="#3484F0",width=200, height=40)
        self.save_btn.pack(side='bottom', padx=10, pady=10)


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
        self.tree_columns = ('adds_types', 'date', 'amount_of_money', 'resource_name', 'safe_name')
        self.tree_headers = ['نوع التكاليف', 'تاريخ', 'المبلغ', 'الموزع', 'نوع الخزنة']

        self.tree = ttk.Treeview(bottom_frame, columns=self.tree_columns, show='headings', selectmode="extended")
        
        # Define headers and bind the sort function to each
        for i, col in enumerate(self.tree_columns):
            self.tree.heading(col, text=self.tree_headers[i], anchor='center',command=lambda c=col: self.sort_column(c, False))
        
        
        # Define column widths (adjust as needed)
        self.tree.column('adds_types', width=100, anchor='center')
        self.tree.column('date', width=150, anchor='center')
        self.tree.column('amount_of_money', width=120, anchor='center')
        self.tree.column('resource_name', width=100, anchor='center')
        self.tree.column('safe_name', width=100, anchor='center')
        

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
            visual_row = row_data
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

