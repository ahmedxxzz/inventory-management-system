import customtkinter as ctk
from tkinter import ttk, messagebox, END
from datetime import date

class CustomerReturnView(ctk.CTkFrame):
    def __init__(self, root, distributor_name):
        super().__init__(root)
        self.pack(fill='both', padx=10, pady=10, expand=True)
        self.configure(fg_color="transparent")

        self.main_font = ctk.CTkFont(family="Arial", size=14)
        self.bold_font = ctk.CTkFont(family="Arial", size=14, weight="bold")
        self.title_font = ctk.CTkFont(family="Arial", size=20, weight="bold")

        title_text = f"تسجيل مرتجع من مكتب (موزع: {distributor_name})"
        title_label = ctk.CTkLabel(self, text=title_text, font=self.title_font)
        title_label.pack(pady=10)

        # --- Top Frame (Customer, Date, Reason) ---
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill='x', padx=20, pady=5)

        # Customer Row
        customer_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        customer_frame.pack( padx=10, pady=5)
        ctk.CTkLabel(customer_frame, text=":العميل (المكتب)", font=self.main_font).pack(side="right", padx=(0, 20))
        self.customer_combobox = ctk.CTkComboBox(customer_frame, values=[], state="readonly", justify='right', font=self.main_font, width=150)
        self.customer_combobox.pack(side="right", fill='x', padx = (20, 0))
        
        # Date Row
        ctk.CTkLabel(customer_frame, text=":التاريخ", font=self.main_font).pack(side="right", padx=(0, 20))
        date_inner_frame = ctk.CTkFrame(customer_frame, fg_color="transparent")
        date_inner_frame.pack(side="right")
        year_list = [str(y) for y in range(date.today().year - 5, date.today().year + 1)]
        self.year_menu = ctk.CTkOptionMenu(date_inner_frame, values=year_list, font=self.main_font)
        self.month_menu = ctk.CTkOptionMenu(date_inner_frame, values=[str(m) for m in range(1, 13)], font=self.main_font)
        self.day_menu = ctk.CTkOptionMenu(date_inner_frame, values=[str(d) for d in range(1, 32)], font=self.main_font)
        self.day_menu.pack(side="right", padx=2)
        self.month_menu.pack(side="right", padx=2)
        self.year_menu.pack(side="right", padx=2)

        # Reason Row
        ctk.CTkLabel(customer_frame, text=":سبب الاسترجاع", font=self.main_font).pack(side="right", padx=(0, 20))
        self.reason_entry = ctk.CTkEntry(customer_frame, placeholder_text="اكتب سبب الاسترجاع (اختياري)...", justify='right', font=self.main_font, width=250)
        self.reason_entry.pack(side="right", fill='x')
        
        # --- Add Item Frame ---
        add_item_frame = ctk.CTkFrame(self)
        add_item_frame.pack( padx=20, pady=10)
        
        self.add_item_button = ctk.CTkButton(add_item_frame, text="إضافة صنف", font=self.bold_font, width=110)
        self.add_item_button.pack(side="left", padx=(10, 5), pady=10)
        
        ctk.CTkLabel(add_item_frame, text=":الصنف", font=self.main_font).pack(side="right", padx=(5, 10), pady=10)
        self.product_entry = ctk.CTkEntry(add_item_frame, placeholder_text="اكتب اسم الصنف...", justify='right', font=self.main_font, width=150)
        self.product_entry.pack(side="right", padx=5, pady=10, fill='x')
        
        ctk.CTkLabel(add_item_frame, text=":الكمية", font=self.main_font).pack(side="right", padx=5, pady=10)
        self.quantity_entry = ctk.CTkEntry(add_item_frame, width=80, justify='center', font=self.main_font)
        self.quantity_entry.pack(side="right", padx=5, pady=10)

        ctk.CTkLabel(add_item_frame, text=":السعر", font=self.main_font).pack(side="right", padx=5, pady=10)
        self.price_entry = ctk.CTkEntry(add_item_frame, width=80, justify='center', font=self.main_font)
        self.price_entry.pack(side="right", padx=5, pady=10)
        
        # --- Treeview Frame ---
        table_frame = ctk.CTkFrame(self)
        table_frame.pack(fill='both', expand=True, padx=20, pady=5)
        
        # <<< MODIFICATION: Added "index" column and reordered >>>
        self.tree = ttk.Treeview(table_frame, columns=("total", "price", "quantity", "product", "index"), show="headings")
        
        # <<< MODIFICATION: Added heading for "index" and adjusted anchors >>>
        self.tree.heading("index", text="م", anchor='center')
        self.tree.heading("product", text="الصنف", anchor='e')
        self.tree.heading("quantity", text="الكمية", anchor='center')
        self.tree.heading("price", text="سعر القطعة", anchor='center')
        self.tree.heading("total", text="الإجمالي", anchor='center')
        
        # <<< MODIFICATION: Added column properties for "index" >>>
        self.tree.column("index", anchor='center', width=40, stretch=False)
        self.tree.column("product", anchor='e', width=250)
        self.tree.column("quantity", anchor='center', width=100, stretch=False)
        self.tree.column("price", anchor='center', width=100, stretch=False)
        self.tree.column("total", anchor='center', width=100, stretch=False)
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="left", fill="y")
        self.tree.pack(side="right", fill="both", expand=True)
        
        # --- Bottom Frame (Remove button and Total) ---
        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.pack(fill='x', padx=20, pady=10)
        self.remove_item_button = ctk.CTkButton(bottom_frame, text="حذف الصنف المحدد", fg_color="red", font=self.bold_font)
        self.remove_item_button.pack(side="right", padx=10)
        self.total_value_label = ctk.CTkLabel(bottom_frame, text="إجمالي قيمة المرتجع: 0.00", font=self.bold_font)
        self.total_value_label.pack(side="left", padx=10)

        # --- Action Buttons Frame ---
        action_buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_buttons_frame.pack(pady=10)
        self.save_button = ctk.CTkButton(action_buttons_frame, text="حفظ المرتجع", width=150, font=self.bold_font)
        self.save_button.pack(side="right", padx=10)
        self.clear_button = ctk.CTkButton(action_buttons_frame, text="إلغاء", fg_color="gray", font=self.bold_font)
        self.clear_button.pack(side="left", padx=10)

    # Messagebox wrappers for strict MVC
    def show_error(self, title, message): messagebox.showerror(title, message, parent=self)
    def show_warning(self, title, message): messagebox.showwarning(title, message, parent=self)
    def show_info(self, title, message): messagebox.showinfo(title, message, parent=self)
    def ask_yes_no(self, title, message): return messagebox.askyesno(title, message, parent=self)