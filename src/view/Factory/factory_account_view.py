import customtkinter as ctk
from tkinter import StringVar, messagebox, ttk

class FactoryAccountView(ctk.CTkFrame):
    def __init__(self, root):
        """create the factory account frame and its commponents inside the factory main frame 

        Args:
            root (ctk.CTkFrame): the factory main frame that contains the navigation buttons  
        """
        self.root = root
        super().__init__(self.root)
        self.pack(fill='both', expand=True, side='top')
        
        self.fac_frames = []
        
        self.search_var = StringVar()
        self.fac_name = StringVar()
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

        adding_fac_frame = ctk.CTkFrame(upper_frame,)
        adding_fac_frame.pack(side='top', pady=10, padx=10, fill='x')
        
        self.adding_btn = ctk.CTkButton(adding_fac_frame, text='اضافة مصنع جديد', font=("Arial", 16, "bold"), text_color='white',width=200, height=40, fg_color='green',)
        self.adding_btn.pack(side='right', padx=10, pady=10)
        
        
        lbls = ['اسم المصنع', 'المبلغ المستحق', 'كمية القطع']
        ents = [self.fac_name, self.amount_money, self.product_quantity]
        for i in range(0, len(lbls)):
            lbl = ctk.CTkLabel(adding_fac_frame, text=lbls[i], font=("Arial", 16, "bold"), text_color='white',width=200, height=40)
            lbl.pack(side='right', pady=10)
            
            ent = ctk.CTkEntry(adding_fac_frame, textvariable=ents[i], font=("Arial", 16, "bold"), height= 40, justify='right')
            ent.pack(side='right',  padx=10, pady=10, fill='x', expand=True)
            if i != 0:
                ent.configure(validate = 'key', validatecommand=(ent.register(self.validate_Entry), '%P', 'float' if ents[i] ==self.amount_money else 'integer'))


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
        style.map('Treeview', background=[('selected', '#8B0000')], foreground=[('selected', 'white')])

        # Configure the Treeview Heading colors
        style.configure("Treeview.Heading",background="#565b5e",foreground="white",relief="flat",font=('Arial', 12, 'bold'))
        style.map("Treeview.Heading",background=[('active', '#3484F0')])

        # --- Create Treeview Widget ---
        self.tree_columns = ('factory_name', 'factory_money', 'factory_quantity')
        self.tree_headers = ['اسم المصنع', 'المبلغ المستحق', 'كمية القطع']

        self.tree = ttk.Treeview(bottom_frame, columns=self.tree_columns, show='headings', selectmode="extended")
        
        # Define headers and bind the sort function to each
        for i, col in enumerate(self.tree_columns):
            self.tree.heading(col, text=self.tree_headers[i], anchor='center',command=lambda c=col: self.sort_column(c, False))
        
        
        # Define column widths (adjust as needed)
        self.tree.column('factory_name',  anchor='center')
        self.tree.column('factory_money',  anchor='center')
        self.tree.column('factory_quantity',  anchor='center')
        

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


    def bind_table(self,  function = None):
        self.tree.bind('<<TreeviewSelect>>', lambda e, func =function: self.on_row_select(e, func))


    def on_row_select(self, event, func):
            """
            Handles the event when a row is selected in the Treeview.
            pass the selected row data to the passed function
            """
            # 1. الحصول على Item ID للصف المحدد
            selected_item_id = self.tree.focus()
            
            
            if selected_item_id:
                row_values = self.tree.item(selected_item_id, 'values') # return (factory_name value, factory_money value ,...)
                func(row_values)


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

