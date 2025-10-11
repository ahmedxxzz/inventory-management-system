import customtkinter as ctk
from tkinter import  ttk 
class ShowDetailsPopupView(ctk.CTkToplevel):
    def __init__(self, root, operation_type):
        super().__init__(root)
        self.geometry("750x450")
        self.title("operation details Window")
        self.grab_set()
        
        self.create_bottom_frame(operation_type)



    def create_bottom_frame(self, operation_type):
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
        style.map('Treeview', background=[('selected', "#19bbf1")])

        # Configure the Treeview Heading colors
        style.configure("Treeview.Heading",background="#565b5e",foreground="white",relief="flat",font=('Arial', 12, 'bold'))
        style.map("Treeview.Heading",background=[('active', '#3484F0')])

        # --- Create Treeview Widget ---
        if operation_type == 'فاتورة شراء':
            self.tree_columns = ( 'product_code', 'price_per_piece', 'quantity', 'discount', 'total_price', 'paid')
            self.tree_headers = [ 'كود المنتج', 'سعر القطعة', 'الكمية', 'الخصم', 'السعر الكلي', 'مدفوعة']


        elif operation_type == 'دفعة':
            self.tree_columns = ( 'amount_money', 'cus_money_before')
            self.tree_headers = ['المبلغ', 'حساب المكتب قبل الدفع']
            
            
        elif operation_type == 'مرتجع':
            self.tree_columns = ( 'product_code', 'quantity', 'price_per_piece', 'total_price','reason')
            self.tree_headers = [ 'كود المنتج', 'الكمية', 'سعر القطعة', 'السعر الكلي' ,'سبب المرتجع']
            

        self.tree = ttk.Treeview(bottom_frame, columns=self.tree_columns, show='headings', selectmode="extended")
        
        # Define headers and bind the sort function to each
        for i, col in enumerate(self.tree_columns):
            self.tree.heading(col, text=self.tree_headers[i], anchor='center',command=lambda c=col: self.sort_column(c, False))
        
        
        if operation_type == 'فاتورة شراء':
            self.tree.column('product_code', width=100, anchor='center')
            self.tree.column('price_per_piece', width=100, anchor='center')
            self.tree.column('quantity', width=80, anchor='center')
            self.tree.column('discount', width=60, anchor='center')
            self.tree.column('total_price', width=120, anchor='center')
            self.tree.column('paid', width=60, anchor='center')

            
        elif operation_type == 'دفعة':
            self.tree.column('amount_money', width=100, anchor='center')
            self.tree.column('cus_money_before', width=100, anchor='center')

            
        elif operation_type == 'مرتجع':
            self.tree.column('product_code', width=100, anchor='center')
            self.tree.column('quantity', width=80, anchor='center')
            self.tree.column('price_per_piece', width=100, anchor='center')
            self.tree.column('total_price', width=120, anchor='center')
            self.tree.column('reason', width=100, anchor='center')


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
