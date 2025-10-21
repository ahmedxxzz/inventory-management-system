import customtkinter as ctk
from tkinter import ttk
from datetime import date

class FactoryReturnView(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root)
        self.pack(fill='both', padx=10, pady=10, expand=True)
        self.configure(fg_color="transparent")

        self.main_font = ctk.CTkFont(family="Arial", size=14)
        self.bold_font = ctk.CTkFont(family="Arial", size=14, weight="bold")
        self.title_font = ctk.CTkFont(family="Arial", size=20, weight="bold")

        title_label = ctk.CTkLabel(self, text="تسجيل مرتجع إلى مصنع", font=self.title_font)
        title_label.pack(pady=10)

        # --- Top Frame (Factory, Date, Reason) using Pack ---
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill='x', padx=20, pady=5)

        # Factory Row
        factory_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        factory_frame.pack( padx=10, pady=5)
        ctk.CTkLabel(factory_frame, text=":المصنع", font=self.main_font).pack(side="right", padx=(0, 20))
        self.factory_combobox = ctk.CTkComboBox(factory_frame, values=[], state="readonly", justify='right', font=self.main_font, width=150)
        self.factory_combobox.pack(side="right", fill='x')

        # Date Row
        ctk.CTkLabel(factory_frame, text=":التاريخ", font=self.main_font).pack(side="right", padx=(0, 20))
        date_inner_frame = ctk.CTkFrame(factory_frame, fg_color="transparent")
        date_inner_frame.pack(side="right")
        year_list = [str(y) for y in range(date.today().year - 5, date.today().year + 1)]
        self.year_menu = ctk.CTkOptionMenu(date_inner_frame, values=year_list, font=self.main_font)
        self.month_menu = ctk.CTkOptionMenu(date_inner_frame, values=[str(m) for m in range(1, 13)], font=self.main_font)
        self.day_menu = ctk.CTkOptionMenu(date_inner_frame, values=[str(d) for d in range(1, 32)], font=self.main_font)
        self.day_menu.pack(side="right", padx=2)
        self.month_menu.pack(side="right", padx=2)
        self.year_menu.pack(side="right", padx=2)

        # Reason Row
        ctk.CTkLabel(factory_frame, text=":سبب الاسترجاع", font=self.main_font).pack(side="right", padx=(0, 20))
        self.reason_entry = ctk.CTkEntry(factory_frame, placeholder_text="اكتب سبب الاسترجاع (اختياري)...", justify='right', font=self.main_font)
        self.reason_entry.pack(side="right", fill='x')
        
        # --- Add Item Frame using Pack ---
        add_item_frame = ctk.CTkFrame(self)
        add_item_frame.pack( padx=20, pady=10)
        
        self.add_item_button = ctk.CTkButton(add_item_frame, text="إضافة صنف", font=self.bold_font, width=110)
        self.add_item_button.pack(side="left", padx=(10, 5), pady=10)
        
        # <<< MODIFICATION: Changed from ComboBox to Entry >>>
        ctk.CTkLabel(add_item_frame, text=":الصنف", font=self.main_font).pack(side="right", padx=(5, 10), pady=10)
        self.product_entry = ctk.CTkEntry(add_item_frame, placeholder_text="اكتب اسم الصنف...", justify='right', font=self.main_font, width=150)
        self.product_entry.pack(side="right", padx=5, pady=10, fill='x')
        
        ctk.CTkLabel(add_item_frame, text=":الكمية", font=self.main_font).pack(side="right", padx=5, pady=10)
        self.quantity_entry = ctk.CTkEntry(add_item_frame, width=80, justify='center', font=self.main_font)
        self.quantity_entry.pack(side="right", padx=5, pady=10)

        ctk.CTkLabel(add_item_frame, text=":السعر", font=self.main_font).pack(side="right", padx=5, pady=10)
        self.price_entry = ctk.CTkEntry(add_item_frame, width=80, justify='center', font=self.main_font)
        self.price_entry.pack(side="right", padx=5, pady=10)

        # --- Items Table (TreeView) ---
        table_frame = ctk.CTkFrame(self)
        table_frame.pack(fill='both', expand=True, padx=20, pady=5)

        self.tree = ttk.Treeview(table_frame, columns=("total", "price", "quantity", "product", 'index'), show="headings")
        self.tree.heading("index", text="#", anchor='center')
        self.tree.heading("product", text="الصنف", anchor='center')
        self.tree.heading("quantity", text="الكمية", anchor='center')
        self.tree.heading("price", text="سعر القطعة", anchor='center')
        self.tree.heading("total", text="الإجمالي", anchor='center')
        
        self.tree.column("index", anchor='center', width=20)
        self.tree.column("product", anchor='center', width=250)
        self.tree.column("quantity", anchor='center', width=100)
        self.tree.column("price", anchor='center', width=100)
        self.tree.column("total", anchor='center', width=100)
        
        self.tree.pack(side="right", fill="both", expand=True)
        
        # --- Bottom Frame (Delete Button & Total) ---
        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.pack(fill='x', padx=20, pady=10)
        self.remove_item_button = ctk.CTkButton(bottom_frame, text="حذف الصنف المحدد", fg_color="red", font=self.bold_font)
        self.remove_item_button.pack(side="right", padx=10)
        self.total_value_label = ctk.CTkLabel(bottom_frame, text="إجمالي قيمة المرتجع: 0.00", font=self.bold_font)
        self.total_value_label.pack(side="left", padx=10)

        # --- Action Buttons (Save & Clear) ---
        action_buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_buttons_frame.pack(pady=10)
        self.save_button = ctk.CTkButton(action_buttons_frame, text="حفظ المرتجع", width=150, font=self.bold_font)
        self.save_button.pack(side="right", padx=10)
        self.clear_button = ctk.CTkButton(action_buttons_frame, text="إلغاء", fg_color="gray", font=self.bold_font)
        self.clear_button.pack(side="left", padx=10)