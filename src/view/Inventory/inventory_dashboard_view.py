import customtkinter as ctk
from tkinter import ttk

class InventoryDashboardView(ctk.CTkFrame):
    def __init__(self, frame):
        """create the inventory dashboard frame

        Args:
            frame (ctk.CTkFrame): the inventory main frame but contains a frame for the navigation buttons
        """
        self.frame = frame
        super().__init__(self.frame)
        self.pack(fill='both', expand=True)
        self.opt1_value = ctk.StringVar(value='شهريا')
        self.opt2_value = ctk.StringVar(value='شهريا')
        self.distributor = ctk.StringVar(value='الجميع')
        self.create_scrollableframe()
        self.most_sold_products()
        self.profit()

    def create_scrollableframe(self):
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(side='top', fill='both', expand=True, padx=30, pady=30)
        self.distributor_opt = ctk.CTkOptionMenu(self.scrollable_frame,  variable=self.distributor)
        self.distributor_opt.pack(side='top', padx=10, pady=20)


    def most_sold_products(self):
        frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=5,border_width=5)
        frame.pack(side='top', fill='x')

        options_frame = ctk.CTkFrame(frame, corner_radius=5,border_width=5,border_color='yellow')
        options_frame.pack(side='top', fill='x')

        self.opt1 = ctk.CTkOptionMenu(options_frame, values=["سنويا", "شهريا", "اسبوعيا"], variable=self.opt1_value)
        self.opt1.pack(side='right', padx=10, pady=10)
        

        
        
        ############ create the table ###########
        """Creates the frame containing the Treeview for displaying data."""
        bottom_frame = ctk.CTkFrame(frame, corner_radius=5)
        bottom_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Make the grid layout responsive
        bottom_frame.grid_rowconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(0, weight=1)

        # --- Style the Treeview to match the CustomTkinter dark theme ---
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",background="#2b2b2b",foreground="white",rowheight=25,fieldbackground="#2b2b2b",bordercolor="#343638",borderwidth=0)
        style.map('Treeview', background=[('selected', "#00bfff")])

        # Configure the Treeview Heading colors
        style.configure("Treeview.Heading",background="#565b5e",foreground="white",relief="flat",font=('Arial', 12, 'bold'))
        style.map("Treeview.Heading",background=[('active', '#3484F0')])

        # --- Create Treeview Widget ---
        self.tree1_columns = ('product_code', 'quantity')
        self.tree1_headers = ['كود القطعة', 'الكمية المباعة']

        self.tree1 = ttk.Treeview(bottom_frame, columns=self.tree1_columns, show='headings', selectmode="extended")

        # Define headers and bind the sort function to each
        for i, col in enumerate(self.tree1_columns):
            self.tree1.heading(col, text=self.tree1_headers[i], anchor='center',command=lambda c=col: self.sort_column(self.tree1, self.tree1_columns, c, False))


        # Define column widths (adjust as needed)
        self.tree1.column('product_code', width=120, anchor='center')
        self.tree1.column('quantity', width=120, anchor='center')

        # --- Add Scrollbars ---
        v_scrollbar = ttk.Scrollbar(bottom_frame, orient="vertical", command=self.tree1.yview)
        h_scrollbar = ttk.Scrollbar(bottom_frame, orient="horizontal", command=self.tree1.xview)
        self.tree1.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Place widgets in the grid
        self.tree1.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')






    def profit(self):
        frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=5,border_width=5)
        frame.pack(side='top', fill='x', pady= 50)

        options_frame = ctk.CTkFrame(frame, corner_radius=5,border_width=5,border_color='yellow')
        options_frame.pack(side='top', fill='x')

        self.opt2 = ctk.CTkOptionMenu(options_frame, values=["سنويا", "شهريا", "اسبوعيا"], variable=self.opt2_value)
        self.opt2.pack(side='right', padx=10, pady=10)
        
        
        
        ############ create the table ###########
        """Creates the frame containing the Treeview for displaying data."""
        bottom_frame = ctk.CTkFrame(frame, corner_radius=5)
        bottom_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Make the grid layout responsive
        bottom_frame.grid_rowconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(0, weight=1)

        # --- Style the Treeview to match the CustomTkinter dark theme ---
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",background="#2b2b2b",foreground="white",rowheight=25,fieldbackground="#2b2b2b",bordercolor="#343638",borderwidth=0)
        style.map('Treeview', background=[('selected', "#00bfff")])

        # Configure the Treeview Heading colors
        style.configure("Treeview.Heading",background="#565b5e",foreground="white",relief="flat",font=('Arial', 12, 'bold'))
        style.map("Treeview.Heading",background=[('active', '#3484F0')])

        # --- Create Treeview Widget ---
        self.tree2_columns = ('opt_type', 'amount_of_money')
        self.tree2_headers = ['نوع العملية', 'المبلغ']

        self.tree2 = ttk.Treeview(bottom_frame, columns=self.tree2_columns, show='headings', selectmode="extended")

        # Define headers and bind the sort function to each
        for i, col in enumerate(self.tree2_columns):
            self.tree2.heading(col, text=self.tree2_headers[i], anchor='center',command=lambda c=col: self.sort_column(self.tree2, self.tree2_columns, c, False))


        # Define column widths (adjust as needed)
        self.tree2.column('opt_type', width=120, anchor='center')
        self.tree2.column('amount_of_money', width=120, anchor='center')

        # --- Add Scrollbars ---
        v_scrollbar = ttk.Scrollbar(bottom_frame, orient="vertical", command=self.tree2.yview)
        h_scrollbar = ttk.Scrollbar(bottom_frame, orient="horizontal", command=self.tree2.xview)
        self.tree2.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Place widgets in the grid
        self.tree2.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')







    def populate_treeview(self, tree, data):
        """Clears the tree and inserts new data."""
        # Clear existing items in the tree
        for item in tree.get_children():
            tree.delete(item)
            
        # Insert new data rows (in reverse for correct visual order)
        for row_data in data:
            visual_row = row_data
            tree.insert("", "end", values=visual_row)


    def sort_column(self, tree, tree_columns, col, reverse):
        """Sorts a treeview column when the header is clicked."""
        try:
            data = [(tree.set(k, col), k) for k in tree.get_children('')]
        except Exception:
            return
            
        data.sort(key=lambda t: self.get_sort_key(t[0]), reverse=reverse)
        
        # Rearrange items in the tree
        for index, (val, k) in enumerate(data):
            tree.move(k, '', index)
            
        # Update the header text to show sort direction (▲/▼)
        for c in tree_columns:
            # Get original header text
            header_text = tree.heading(c, 'text').replace(' ▲', '').replace(' ▼', '')
            if c == col:
                header_text += ' ▲' if reverse else ' ▼'
            tree.heading(c, text=header_text)

        # Reverse the sort direction for the next click on this column
        tree.heading(col, command=lambda: self.sort_column(tree, tree_columns, col, not reverse))


    def get_sort_key(self,value):
        """Helper function to convert values for sorting."""
        try:
            return float(str(value).replace(',', ''))
        except (ValueError, TypeError):
            return str(value).lower()



