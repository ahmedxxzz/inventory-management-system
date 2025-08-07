import customtkinter as ctk
from tkinter import StringVar, ttk , messagebox
from datetime import datetime

class PayView(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root, )
        self.pack(fill='both', padx=10,expand=True)
        self.cus_name = StringVar()
        self.safe_type = StringVar()
        self.safe_type.set('اختار نوع الخزنة')
        self.money_amount = StringVar()
        self.day_var = StringVar()
        self.month_var = StringVar()
        self.year_var = StringVar()
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
        
        # --- CONVERTED TO GRID ---
        # Configure the grid layout for the upper_input_frame
        upper_input_frame.grid_columnconfigure(0, weight=1) # Column for labels
        upper_input_frame.grid_columnconfigure(1, weight=2) # Column for entries

        # --- Row 0: Customer Name ---
        lbl_cus_name = ctk.CTkLabel(upper_input_frame, text='اسم المكتب', font=("Arial", 14, "bold"), text_color='white',width=200, height=40)
        lbl_cus_name.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.cus_name_entry = ctk.CTkEntry(upper_input_frame, textvariable=self.cus_name, font=("Arial", 18, "bold"),width=200, height=40, justify='right')
        self.cus_name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # --- Row 1: Safe Type ---
        lbl_safe_type = ctk.CTkLabel(upper_input_frame, text='نوع الخزنة', font=("Arial", 14, "bold"), text_color='white',width=200, height=40)
        lbl_safe_type.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.option_menu = ctk.CTkOptionMenu(upper_input_frame, variable=self.safe_type, font=("Arial", 18, "bold"),width=200, height=40, state='readonly')
        self.option_menu.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # --- Row 2: Payment Amount ---
        lbl_money_amount = ctk.CTkLabel(upper_input_frame, text='مبلغ الدفع', font=("Arial", 14, "bold"), text_color='white',width=200, height=40)
        lbl_money_amount.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        
        money_amount_entry = ctk.CTkEntry(upper_input_frame, textvariable=self.money_amount, font=("Arial", 18, "bold"),width=200, height=40, justify='left')
        money_amount_entry.configure(validate="key", validatecommand = (money_amount_entry.register(self.validate_Entry), '%P', 'float'))
        money_amount_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        
        # --- NEW ROW FOR DATE SELECTION (under مبلغ الدفع) ---
        # 1. Add the Date Label in the next row (row=3)
        date_label = ctk.CTkLabel(upper_input_frame, text="التاريخ", font=("Arial", 14, "bold"), text_color='white', width=200, height=40)
        date_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        
        # 2. Create a frame to hold the 3 option menus in a single grid cell
        date_options_frame = ctk.CTkFrame(upper_input_frame, fg_color="transparent")
        date_options_frame.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        # 3. Create the Year, Month, and Day Option Menus
        current_date = datetime.now()
        years = [str(y) for y in range(current_date.year, current_date.year - 10, -1)]
        months = [f"{m:02d}" for m in range(1, 13)]
        days = [f"{d:02d}" for d in range(1, 32)]
        
        # Using local variables as requested (not changing self)
        self.year_var.set(str(current_date.year))
        self.month_var.set(f"{current_date.month:02d}")
        self.day_var.set(f"{current_date.day:02d}")

        # Pack menus inside their container frame (right-to-left for Arabic UI)
        day_menu = ctk.CTkOptionMenu(date_options_frame, values=days, variable=self.day_var, width=60, height=40, font=("Arial", 14))
        day_menu.pack(side='right', padx=(2,0), fill='x', expand=True)

        month_menu = ctk.CTkOptionMenu(date_options_frame, values=months, variable=self.month_var, width=60, height=40, font=("Arial", 14))
        month_menu.pack(side='right', padx=2, fill='x', expand=True)
        
        year_menu = ctk.CTkOptionMenu(date_options_frame, values=years, variable=self.year_var, width=80, height=40, font=("Arial", 14))
        year_menu.pack(side='right', padx=(0,2), fill='x', expand=True)
        # --- END OF NEW ROW ---

        
        frame_pay_button = ctk.CTkFrame(inputs_frame, fg_color='#333333')
        frame_pay_button.pack(side='top', padx=10,pady=10,)
        
        self.button = ctk.CTkButton(frame_pay_button, text='دفع', font=("Arial", 16, "bold"), width=200, height=40)
        self.button.pack(side='top', pady=10)
        
        
        ######## recommendation frame 
        self.recommended_frame = ctk.CTkScrollableFrame(sub_upper_frame, width=200,height=250,border_width=5, border_color='#333333' ,corner_radius=5, fg_color='transparent',scrollbar_button_color='#333333', scrollbar_button_hover_color='#333333', scrollbar_fg_color='#333333')
        self.recommended_frame.pack(side='left', padx=10,pady=30)
        # ==============================================================================
        # >>>>>>>> MODIFIED FUNCTION ENDS HERE <<<<<<<<
        # ==============================================================================


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
        self.tree_columns = ('customer_name', 'date', 'money', 'money_before', 'money_after')
        self.tree_headers = ['اسم المكتب', 'التاريخ', 'المبلغ', 'الحساب قبل الدفع', 'الحساب بعد الدفع']

        self.tree = ttk.Treeview(bottom_frame, columns=self.tree_columns, show='headings', selectmode="extended")
        
        # Define headers and bind the sort function to each
        for i, col in enumerate(self.tree_columns):
            self.tree.heading(col, text=self.tree_headers[i], anchor='center',command=lambda c=col: self.sort_column(c, False))


        # Define column widths (adjust as needed)
        self.tree.column('customer_name', width=80, anchor='center')
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



    def recommendation_focusIn(self, var):
            for btn_text, amount_money in self.recommendations:
                frame = ctk.CTkFrame(self.recommended_frame, fg_color='transparent', border_width=0, width=200, height=40)
                frame.pack(side='top', padx=10, pady=10)
                button = ctk.CTkButton(frame,text=btn_text,width=100,  height=35,fg_color="#4CAF50", hover_color="#45a049", text_color="yellow", border_width=2, border_color="#388E3C", corner_radius=10, font=("Arial", 14), command=lambda btn_text=btn_text: var.set(btn_text))
                button.pack(side='left', padx=(0, 5))
                money_lbl = ctk.CTkLabel(frame,text=amount_money,width=80,height=35,font=("Arial", 14, "bold"),text_color='white',fg_color="#007BFF", corner_radius=5)
                money_lbl.pack(side='right', padx=(5, 0))
                self.recommendation_frames.append(frame)


    def recommendation_KeyRelease(self, var, matching_items):
        for cus, amount_money in matching_items:
            frame = ctk.CTkFrame(self.recommended_frame, fg_color='transparent', border_width=0, width=200, height=40)
            frame.pack(side='top', padx=10, pady=10)
            button = ctk.CTkButton(frame,text=cus,width=100,  height=35,fg_color="#4CAF50", hover_color="#45a049",text_color="yellow",border_width=2,border_color="#388E3C", corner_radius=10,font=("Arial", 14), command=lambda btn_text=cus: var.set(btn_text))
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
        self.cus_name.set('')
        self.money_amount.set('')
        self.safe_type.set('اختار نوع الخزنة')
        