import customtkinter as ctk
from tkinter import StringVar, ttk 

class Buy_frame(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root)
        self.pack(fill='both', expand=True)
        
        self.recommendation_buttons = []
        self.recommendations = []
        
        self.fac_name = StringVar()
        self.product_code = StringVar()
        self.price = StringVar()
        self.quantity = StringVar()
        self.discount = StringVar()
        self.supplier = StringVar()
        
        self.tree_data = [
                        #[الترتيب, الترايخ, نوع القطعة, الكمية, سعر القطعة, الخصم على القطعة , السعر الكلى ]
                        
                        [1, '2025-04-21 20:54:29', '1003,1002', 50, 500, 1, 24750.0],
                        [2, '2025-04-21 21:54:29', '1001,1004', 210, 500, 1, 103950.0],
                        [3, '2025-04-21 22:54:29', '1005,1008,1000', 20, 500, 1, 9900.0],
                        [4, '2025-04-21 19:54:29', '1003', 200, 500, 1, 99000.0],
                        [5, '2025-04-21 20:52:29', '1003', 40, 500, 1, 19800.0],
                        [6, '2025-04-21 20:54:29', '1003,1002', 50, 500, 1, 24750.0],
                        [7, '2025-04-21 21:54:29', '1001,1004', 210, 500, 1, 103950.0],
                        [8, '2025-04-21 22:54:29', '1005,1008,1000', 20, 500, 1, 9900.0],
                        [9, '2025-04-21 19:54:29', '1003', 200, 500, 1, 99000.0],
                        [10, '2025-04-21 20:52:29', '1003', 40, 500, 1, 19800.0],
                        [11, '2025-04-21 20:54:29', '1003,1002', 50, 500, 1, 24750.0],
                        [12, '2025-04-21 21:54:29', '1001,1004', 210, 500, 1, 103950.0],
                        [13, '2025-04-21 22:54:29', '1005,1008,1000', 20, 500, 1, 9900.0],
                        [14, '2025-04-21 19:54:29', '1003', 200, 500, 1, 99000.0],
                        [15, '2025-04-21 20:52:29', '1003', 40, 500, 1, 19800.0]
                        
                        ]
        
        self.create_upper_frame()
        self.create_bottom_frame()
        
        
    def create_upper_frame(self):
        upper_frame = ctk.CTkFrame(self, corner_radius=5,border_width=5,border_color='yellow')
        upper_frame.pack(side='top', padx=10, fill='x')
        
        
        ###### Inputs frame
        inputs_frame = ctk.CTkFrame(upper_frame, border_width=2)
        inputs_frame.pack(side='left', padx=10,pady=10)
        
        
        entry_frame = ctk.CTkFrame(inputs_frame, border_width=2)
        entry_frame.pack(side='top', padx=10,pady=10, fill='both')
        
         
        inputs_lbls_frame = ctk.CTkFrame(entry_frame)
        inputs_lbls_frame.pack(side='left', fill='y')
        lbls_names = ['اسم المصنع', 'كود القطعة', 'سعر القطعة', 'عدد القطع', 'الخصم', 'الموزع']
        
        for lbl in lbls_names:
            lbl = ctk.CTkLabel(inputs_lbls_frame, text=lbl, font=("Arial", 14, "bold"), text_color='white',width=200, height=40)
            lbl.pack(side='top', padx=10, pady=10)
        
        
        inputs_entries_frame = ctk.CTkFrame(entry_frame)
        inputs_entries_frame.pack(side='right', fill='y')
        
        
        entry_variables = [self.fac_name,self.product_code,self.price,self.quantity,self.discount]
        for var in entry_variables:
            fac_entry = ctk.CTkEntry(inputs_entries_frame, textvariable=var, font=("Arial", 18, "bold"),width=200, height=40, justify='right' if var ==self.fac_name else 'left')
            fac_entry.pack(side='top', padx=10, pady=10)
            if var == self.fac_name or var == self.product_code:
                fac_entry.bind('<FocusIn>', lambda event,var = var: self.recommendation_focusIn(var))
                fac_entry.bind('<KeyRelease>', lambda event,var = var: self.recommendation_KeyRelease(var))
                fac_entry.bind('<FocusOut>', lambda event,var = var: self.recommendation_focusOut(var))
            
        
        ctk.CTkOptionMenu(inputs_entries_frame,variable=self.supplier ,values=['snow white', 'golden rose'], font=("Arial", 18, "bold"),width=200, height=40).pack(side='top', padx=10, pady=10)
        
        
        '''
        connect the button to the function with data base
        '''
        
        ctk.CTkButton(inputs_lbls_frame, text='حفظ الفاتورة', font=("Arial", 18, "bold"),width=200, height=40, command=self.buy).pack(side='top', padx=10, pady=10)
        ctk.CTkButton(inputs_entries_frame, text='اضافة الى الفاتورة', font=("Arial", 18, "bold"),width=200, height=40,command=self.cache_buy).pack(side='top', padx=10, pady=10)
        
        
        ###### Recommendation frame
        self.recommended_frame = ctk.CTkScrollableFrame(upper_frame, width=170,height=300 ,corner_radius=5, border_width=0, fg_color='transparent',scrollbar_button_color='#2b2b2b', scrollbar_button_hover_color='#2b2b2b', scrollbar_fg_color='#2b2b2b')

        self.recommended_frame.pack(side='left', padx=10,pady=30)
    
    


    def clear_recommendation_buttons(self):
        for btn in self.recommendation_buttons:
            btn.destroy()
        
        self.recommendation_buttons = []
        self.recommended_frame._scrollbar.set(0.0, 0.0)
        self.recommended_frame._parent_canvas.yview_moveto(0.0)


    def recommendation_KeyRelease(self, var):
        var_text = var.get().strip() 
        
        if  var_text !='':
            self.clear_recommendation_buttons()
            if  self.recommendations :
                self.recommended_frame.configure(border_width=5, fg_color= 'gray20', border_color='#21130d', scrollbar_button_color='#696969', scrollbar_button_hover_color='red', scrollbar_fg_color='#333333')
            
            matching_items =[]
            for item in self.recommendations:
                if var_text in str(item):
                    matching_items.append(str(item))
            
            if matching_items :
                for btn_text in matching_items:
                    button = ctk.CTkButton(self.recommended_frame, text=btn_text,width=200, height=40, command=lambda btn_text=btn_text: var.set(btn_text))
                    button.pack(side='top', padx=10, pady=10)
                    self.recommendation_buttons.append(button)
        else:
            self.recommendation_focusIn(var)
        
            
    def recommendation_focusIn(self, var):
        
        self.clear_recommendation_buttons()
        
        if var == self.fac_name:
            ''' 
            ## call a function from data base to get the factories names
            '''
            self.recommendations = ["جلوبال تك للتصنيع", "حلول الروبوتات الدقيقة", "المنتجات البيئية الدائمة الخضرة", "صناعات الابتكار التقني", "أعمال الأتمتة العليا", "مصنع التصنيع الديناميكي", "مركز اللوجستيات الموحد", "أعمال الصلب النجمية", "ابتكارات المستقبل المزدهرة", "مجمع الهندسة النخبة", "مطاحن جراند سنترال", "منشأة الإنتاج الرئيسية", "أنظمة ستريملاين إنك", "بضائع الجودة الكمية", "سلسلة التوريد التآزرية", "مشاريع فانجارد المحدودة", "الصناعات الثقيلة هارموني", "مواد الجيل القادم المركبة", "مصنع البلاستيك بيكنكل", "الطاقة المتجددة المشرقة", "حلول الحالة الصلبة", "شركة تيتانيوم للتقنيات", "مؤسسة المرافق العالمية", "أعمال رؤية الرأس", "المستودعات العالمية", "زينيث بلا نفايات", "خطوط التجميع ألفا", "أعمال بيتا للتكنولوجيا الحيوية", "مجموعة غاما للمعدات", "أجهزة دلتا الرقمية"]

        
        
        elif var == self.product_code:
            ''' 
            ## call a function from data base to get the codes names
            '''
            self.recommendations = [i for i in range(1001, 1051)]
        
        if var.get() =='':
            if self.recommendations :
                self.recommended_frame.configure(border_width=5, fg_color= 'gray20', border_color='#21130d', scrollbar_button_color='#696969', scrollbar_button_hover_color='red', scrollbar_fg_color='#333333')
                
                for btn_text in self.recommendations:
                    button = ctk.CTkButton(self.recommended_frame, text=btn_text,width=200, height=40, command=lambda btn_text=btn_text: var.set(btn_text))
                    button.pack(side='top', padx=10, pady=10)
                    self.recommendation_buttons.append(button)
        
        else: 
            self.recommendation_KeyRelease(var)


    def recommendation_focusOut(self, var):
        self.clear_recommendation_buttons()
        self.recommendations = []
        self.recommended_frame.configure(border_width=0, fg_color='transparent',scrollbar_button_color='#2b2b2b', scrollbar_button_hover_color='#2b2b2b', scrollbar_fg_color='#2b2b2b' )
        



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
        self.tree_columns = ('total_price', 'discount', 'piece_price', 'quantity', 'piece_type', 'date', 'order')
        self.tree_headers = ['السعر الكلي', 'الخصم', 'سعر القطعة', 'الكمية', 'نوع القطعة', 'التاريخ', 'الترتيب']

        self.tree = ttk.Treeview(bottom_frame, columns=self.tree_columns, show='headings', selectmode="extended")
        
        # Define headers and bind the sort function to each
        for i, col in enumerate(self.tree_columns):
            self.tree.heading(col, text=self.tree_headers[i], anchor='center',command=lambda c=col: self.sort_column(c, False))
            
        # Define column widths (adjust as needed)
        self.tree.column('order', width=60, anchor='center')
        self.tree.column('date', width=170, anchor='center')
        self.tree.column('piece_type', width=150, anchor='w')
        self.tree.column('quantity', width=80, anchor='center')
        self.tree.column('piece_price', width=100, anchor='center')
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
        
        # --- Populate the Treeview with initial data ---
        self.populate_treeview(self.tree_data)

    def populate_treeview(self, data):
        """Clears the tree and inserts new data."""
        # Clear existing items in the tree
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Insert new data rows (in reverse for correct visual order)
        for row_data in data:
            # Reorder the data to match the visual column order (right-to-left)
            # Original: [0, 'date', 'type', qty, price, disc, total]
            # Target:   [total, disc, price, qty, 'type', 'date', 0]
            visual_row = row_data[::-1]
            self.tree.insert("", "end", values=visual_row)

    def sort_column(self, col, reverse):
        """Sorts a treeview column when the header is clicked."""
        # Get data from the column to be sorted
        try:
            data = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        except Exception:
            # Handle cases where column might not exist
            return
            
        # --- Smart sorting: try converting to number, otherwise sort as text ---
        # The key tries to convert the value to a float for numeric sorting.
        # If it fails (e.g., for text or dates), it uses the original string value.
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

    @staticmethod
    def get_sort_key(value):
        """Helper function to convert values for sorting."""
        try:
            # Try to convert to a float for numeric sorting
            return float(str(value).replace(',', ''))
        except (ValueError, TypeError):
            # If conversion fails, return the lowercase string for case-insensitive text sorting
            return str(value).lower()
            

    def cache_buy(self):
        print('here we cached the buy operation')

    def buy(self):
        print('here we saved the buy operations')