import customtkinter as ctk
from tkinter import ttk, messagebox, END
from datetime import date

class CustomerSalesView(ctk.CTkFrame):
    def __init__(self, root, distributor_name):
        super().__init__(root)
        self.pack(fill='both', padx=10, pady=10, expand=True)
        self.configure(fg_color="transparent")

        self.main_font = ctk.CTkFont(family="Arial", size=14)
        self.bold_font = ctk.CTkFont(family="Arial", size=14, weight="bold")
        self.title_font = ctk.CTkFont(family="Arial", size=20, weight="bold")
        
        title_text = f"فاتورة بيع جديدة (موزع: {distributor_name})"
        title_label = ctk.CTkLabel(self, text=title_text, font=self.title_font)
        title_label.pack(pady=10)

        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill='x', padx=20, pady=5)
        top_frame.grid_columnconfigure(0, weight=1); top_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(top_frame, text="المكتب:", font=self.main_font).grid(row=0, column=1, padx=10, pady=10, sticky="e")
        self.customer_combobox = ctk.CTkComboBox(top_frame, values=[], state="readonly", justify='right', font=self.main_font)
        self.customer_combobox.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        right_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        right_frame.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.paid_switch = ctk.CTkSwitch(right_frame, text="مدفوعة (نقدي)", font=self.main_font, onvalue=1, offvalue=0)
        self.paid_switch.pack(side="right", padx=10)
        date_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        date_frame.pack(side="right", padx=20)
        year_list = [str(y) for y in range(date.today().year - 5, date.today().year + 2)]
        self.year_menu = ctk.CTkOptionMenu(date_frame, values=year_list, font=self.main_font)
        self.month_menu = ctk.CTkOptionMenu(date_frame, values=[f"{m:02d}" for m in range(1, 13)], font=self.main_font)
        self.day_menu = ctk.CTkOptionMenu(date_frame, values=[f"{d:02d}" for d in range(1, 32)], font=self.main_font)
        self.year_menu.pack(side="right", padx=2); self.month_menu.pack(side="right", padx=2); self.day_menu.pack(side="right", padx=2)
        ctk.CTkLabel(top_frame, text=":التاريخ والحالة", font=self.main_font).grid(row=1, column=1, padx=10, pady=10, sticky="e")
        
        add_item_frame = ctk.CTkFrame(self)
        add_item_frame.pack(fill='x', padx=20, pady=10)
        add_item_frame.grid_columnconfigure(5, weight=1)
        ctk.CTkLabel(add_item_frame, text=":الصنف", font=self.main_font).grid(row=0, column=6, padx=(5,0), pady=10)
        self.product_combobox = ctk.CTkComboBox(add_item_frame, state="readonly", justify='right', font=self.main_font)
        self.product_combobox.grid(row=0, column=5, padx=5, pady=10, sticky="ew")
        ctk.CTkLabel(add_item_frame, text=":السعر", font=self.main_font).grid(row=0, column=4, padx=5, pady=10)
        self.price_entry = ctk.CTkEntry(add_item_frame, width=100, justify='center', font=self.main_font)
        self.price_entry.grid(row=0, column=3, padx=5, pady=10)
        ctk.CTkLabel(add_item_frame, text=":الكمية", font=self.main_font).grid(row=0, column=2, padx=5, pady=10)
        self.quantity_entry = ctk.CTkEntry(add_item_frame, width=100, justify='center', font=self.main_font)
        self.quantity_entry.grid(row=0, column=1, padx=5, pady=10)
        self.add_item_button = ctk.CTkButton(add_item_frame, text="إضافة صنف", font=self.bold_font, width=110)
        self.add_item_button.grid(row=0, column=0, padx=(10,5), pady=10)

        # --- REQUIREMENT 1: Discount frame moved ABOVE the table ---
        discount_outer_frame = ctk.CTkFrame(self)
        discount_outer_frame.pack(fill='x', padx=20, pady=(5,0))
        
        discount_frame = ctk.CTkFrame(discount_outer_frame)
        discount_frame.pack(side='right', padx=10, pady=5)
        
        self.discount_percentage_entry = ctk.CTkEntry(discount_frame, width=60, justify='center', font=self.main_font, placeholder_text="0")
        self.discount_percentage_entry.pack(side='right')
        ctk.CTkLabel(discount_frame, text="% خصم نسبة", font=self.main_font).pack(side='right', padx=(5, 15))
        
        self.discount_value_entry = ctk.CTkEntry(discount_frame, width=60, justify='center', font=self.main_font, placeholder_text="0.00")
        self.discount_value_entry.pack(side='right')
        ctk.CTkLabel(discount_frame, text="خصم قيمة (للقطعة)", font=self.main_font).pack(side='right', padx=5)

        table_frame = ctk.CTkFrame(self)
        table_frame.pack(fill='both', expand=True, padx=20, pady=5)
        
        # --- REQUIREMENT 3: Reordered columns to put '#' at the end ---
        self.tree = ttk.Treeview(table_frame, columns=("total", "price", "quantity", "product", "#"), show="headings")
        self.tree.heading("total", text="الإجمالي", anchor='center')
        self.tree.heading("price", text="السعر", anchor='center')
        self.tree.heading("quantity", text="الكمية", anchor='center')
        self.tree.heading("product", text="الصنف", anchor='center')
        self.tree.heading("#", text="#", anchor='center')
        
        self.tree.column("total", anchor='center', width=100)
        self.tree.column("price", anchor='center', width=80)
        self.tree.column("quantity", anchor='center', width=80)
        self.tree.column("product", anchor='e', width=250)
        self.tree.column("#", anchor='center', width=30, stretch=False)
        self.tree.pack(side="right", fill="both", expand=True)
        
        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.pack(fill='x', padx=20, pady=10)
        self.remove_item_button = ctk.CTkButton(bottom_frame, text="حذف الصنف المحدد", fg_color="red", font=self.bold_font)
        self.remove_item_button.pack(side="right", padx=10)
        # --- REQUIREMENT 3: Total label moved to the bottom frame ---
        self.total_value_label = ctk.CTkLabel(bottom_frame, text="الإجمالي: 0.00", font=self.bold_font, justify='left')
        self.total_value_label.pack(side="left", padx=10)

        action_buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_buttons_frame.pack(pady=10)
        self.save_button = ctk.CTkButton(action_buttons_frame, text="حفظ الفاتورة", width=150, font=self.bold_font)
        self.save_button.pack(side="right", padx=10)
        self.clear_button = ctk.CTkButton(action_buttons_frame, text="فاتورة جديدة", fg_color="gray", font=self.bold_font)
        self.clear_button.pack(side="left", padx=10)

    # --- NEW: Methods to control discount widgets ---
    def lock_discount_widgets(self):
        self.discount_value_entry.configure(state='disabled')
        self.discount_percentage_entry.configure(state='disabled')

    def unlock_discount_widgets(self):
        self.discount_value_entry.configure(state='normal')
        self.discount_percentage_entry.configure(state='normal')

    def show_error(self, title, message):
        messagebox.showerror(title, message, parent=self)

    def show_warning(self, title, message):
        messagebox.showwarning(title, message, parent=self)

    def show_info(self, title, message):
        messagebox.showinfo(title, message, parent=self)

    def ask_yes_no(self, title, message):
        return messagebox.askyesno(title, message, parent=self)