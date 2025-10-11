import customtkinter as ctk
from tkinter import ttk

class InventoryDetailsView(ctk.CTkFrame):
    def __init__(self, frame):
        """create a frame for every navigation button inside the inventory main frame 

        Args:
            frame (ctk.CTkFrame): the inventory main frame but contains a frame for the navigation buttons
        """
        super().__init__(frame)
        self.pack(side='top', padx=10,  fill='both',expand=True)
        
        self.search_var = ctk.StringVar()
        self.total_row = None
        self.total_labels = {}
        self.HEADER_BG = "#1f282e" 
        self.HEADER_FG = "white"
        
        self.create_upper_frame()
        self.create_the_table()
        
    def create_upper_frame(self):
        upper_frame = ctk.CTkFrame(self, corner_radius=5,border_width=5,border_color='yellow')
        upper_frame.pack(side='top', fill='x')

        search_lbl = ctk.CTkLabel(upper_frame, text='بحث', font=("Arial", 16, "bold"), text_color='white',width=200, height=40)
        search_lbl.pack(side='right', padx=10, pady=10)

        self.search_entry = ctk.CTkEntry(upper_frame, textvariable=self.search_var, font=("Arial", 16, "bold"), height= 40, justify='right')
        self.search_entry.pack(side='left',  padx=(50,), pady=10, fill='x', expand=True)

    def create_the_table(self):
        """Creates the frame containing the Treeview for displaying data."""
        bottom_frame = ctk.CTkFrame(self, corner_radius=5)
        bottom_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Make the grid layout responsive
        bottom_frame.grid_rowconfigure(0, weight=1) 
        bottom_frame.grid_rowconfigure(2, weight=0)
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
        self.tree_columns = ('product_code', 'quantity',  'cus_price' )
        self.tree_headers = ['كود القطعة',  'الكمية',  'سعر البيع للمكتب']

        self.tree = ttk.Treeview(bottom_frame, columns=self.tree_columns, show='headings', selectmode="extended")
        
        # Define headers and bind the sort function to each
        for i, col in enumerate(self.tree_columns):
            self.tree.heading(col, text=self.tree_headers[i], anchor='center',command=lambda c=col: self.sort_column(c, False))
        
        
        # Define column widths (adjust as needed)
        self.tree.column('product_code',  anchor='center')
        self.tree.column('quantity',  anchor='center')
        self.tree.column('cus_price', anchor='center')
        

        # --- Add Scrollbars ---
        v_scrollbar = ttk.Scrollbar(bottom_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(bottom_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Place widgets in the grid
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        self.create_total_footer(bottom_frame)


    def populate_treeview(self, data):
        """Clears the tree and inserts new data."""
        # Clear existing items in the tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        total_quantity = 0
        total_cus_price_value = 0 

        # Insert new data rows (in reverse for correct visual order)
        for row_data in data:
            if len(row_data) >= 3:
                try:
                    # جمع الكميات والقيم المالية
                    quantity = int(row_data[1])
                    price = float(row_data[2])
                    
                    total_quantity += quantity
                    total_cus_price_value += price * quantity 
                    
                except (ValueError, TypeError):
                    pass 
            
            self.tree.insert("", "end", values=row_data)

        # 💡 تغيير: تحديث صف الإجمالي الثابت
        self.update_total_footer(total_quantity, total_cus_price_value)



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


    def create_total_footer(self, parent_frame):
        """Creates a sticky frame at the bottom styled like a header."""
        
        # الإطار الرئيسي يوضع في الصف 2 من bottom_frame (Footer الثابت)
        footer_container = ctk.CTkFrame(parent_frame, fg_color=self.HEADER_BG, height=35)
        footer_container.grid(row=2, column=0, sticky='ew', pady=(0, 5), columnspan=2)
        footer_container.grid_columnconfigure(0, weight=1)

        self.total_row = ctk.CTkFrame(footer_container, fg_color=self.HEADER_BG)
        self.total_row.pack(fill='x', expand=True)
        
        self.total_labels = {}
        for col in self.tree_columns:
            index = self.tree_columns.index(col)
            self.total_row.grid_columnconfigure(index, weight=1)

            # Labels هنا تأخذ مظهر Header
            label = ctk.CTkLabel(self.total_row, text="", font=('Arial', 12, 'bold'), 
                                 anchor='center', fg_color=self.HEADER_BG, text_color=self.HEADER_FG, height=35)
            label.grid(row=0, column=index, sticky='nsew', padx=(1, 1))
            self.total_labels[col] = label


    def _sync_footer_widths(self, event=None):
        """Syncs the footer column widths with the Treeview column widths."""
        if not self.total_labels or not self.winfo_ismapped():
            return
            
        try:
            for i, col in enumerate(self.tree_columns):
                # جلب عرض العمود ومحاذاته من Treeview
                width = self.tree.column(col, 'width')
                anchor = self.tree.column(col, 'anchor')

                # تطبيق العرض والمحاذاة على Label في Footer
                self.total_row.grid_columnconfigure(i, minsize=width)
                self.total_labels[col].configure(width=width, anchor=anchor)
                
        except Exception:
            pass


    def update_total_footer(self, total_quantity, total_cus_price_value):
        """Updates the text of the total footer labels."""
        if not self.total_labels:
            return

        # وضع كلمة "الإجمالي" في العمود الأول
        self.total_labels['product_code'].configure(text='الإجمالي', font=('Arial', 14, 'bold'), text_color='yellow')
        
        # تحديث عمود 'quantity'
        self.total_labels['quantity'].configure(text=f'{total_quantity:,}')
        
        # تحديث عمود 'cus_price' (لعرض إجمالي القيمة المالية)
        self.total_labels['cus_price'].configure(text=f'{total_cus_price_value:,.2f}')

