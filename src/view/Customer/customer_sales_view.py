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

        # --- START: CONVERTED FROM GRID TO PACK (Top Frame Section) ---
        # Frame for the first row (Customer)
        customer_row_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        customer_row_frame.pack( padx=10, pady=(10, 5))
        
        ctk.CTkLabel(customer_row_frame, text=": المكتب", font=self.main_font).pack(side='right', padx=(10,0))
        self.customer_combobox = ctk.CTkComboBox(customer_row_frame, values=[], state="readonly", justify='right', font=self.main_font, width=250)
        self.customer_combobox.pack(side='right', padx=(30,0))

        # Frame for the second row (Date and Status)

        ctk.CTkLabel(customer_row_frame, text=":التاريخ والحالة", font=self.main_font).pack(side='right', padx=(10,0))
        
        right_sub_frame = ctk.CTkFrame(customer_row_frame, fg_color="transparent")
        right_sub_frame.pack(side='right', padx=(10,0))
        
        self.paid_switch = ctk.CTkSwitch(right_sub_frame, text="مدفوعة (نقدي)", font=self.main_font, onvalue=1, offvalue=0)
        self.paid_switch.pack(side="right", padx=10)
        
        date_frame = ctk.CTkFrame(right_sub_frame, fg_color="transparent")
        date_frame.pack(side="right", padx=20)
        
        year_list = [str(y) for y in range(date.today().year - 5, date.today().year + 2)]
        self.year_menu = ctk.CTkOptionMenu(date_frame, values=year_list, font=self.main_font)
        self.month_menu = ctk.CTkOptionMenu(date_frame, values=[f"{m:02d}" for m in range(1, 13)], font=self.main_font)
        self.day_menu = ctk.CTkOptionMenu(date_frame, values=[f"{d:02d}" for d in range(1, 32)], font=self.main_font)
        self.year_menu.pack(side="right", padx=2)
        self.month_menu.pack(side="right", padx=2)
        self.day_menu.pack(side="right", padx=2)

        discount_outer_frame = ctk.CTkFrame(self)
        discount_outer_frame.pack( padx=20, pady=(5,0))
        discount_frame = ctk.CTkFrame(discount_outer_frame)
        discount_frame.pack( padx=10, pady=5)
        ctk.CTkLabel(discount_frame, text="% خصم نسبة", font=self.main_font).pack(side='right', padx=(5, 15))
        self.discount_percentage_entry = ctk.CTkEntry(discount_frame, width=60, justify='center', font=self.main_font, placeholder_text="0")
        self.discount_percentage_entry.pack(side='right')
        ctk.CTkLabel(discount_frame, text="خصم قيمة (للقطعة)", font=self.main_font).pack(side='right', padx=5)
        self.discount_value_entry = ctk.CTkEntry(discount_frame, width=60, justify='center', font=self.main_font, placeholder_text="0.00")
        self.discount_value_entry.pack(side='right')



        add_item_frame = ctk.CTkFrame(self)
        add_item_frame.pack( padx=20, pady=10)

        # --- START: CONVERTED FROM GRID TO PACK (Add Item Section) ---
        # We will pack from left to right for the button, and then right to left for the entry fields
        self.add_item_button = ctk.CTkButton(add_item_frame, text="إضافة صنف", font=self.bold_font, width=110)
        self.add_item_button.pack(side='left', padx=(10, 5), pady=10)
        
        ctk.CTkLabel(add_item_frame, text=":الصنف", font=self.main_font).pack(side='right', padx=(5,0), pady=10)
        self.product_entry = ctk.CTkEntry(add_item_frame, justify='right', font=self.main_font, width=100)
        self.product_entry.pack(side='right', padx=5, pady=10, fill='x', )
        
        ctk.CTkLabel(add_item_frame, text=":السعر", font=self.main_font).pack(side='right', padx=5, pady=10)
        self.price_entry = ctk.CTkEntry(add_item_frame, width=100, justify='center', font=self.main_font)
        self.price_entry.pack(side='right', padx=5, pady=10)
        
        ctk.CTkLabel(add_item_frame, text=":الكمية", font=self.main_font).pack(side='right', padx=5, pady=10)
        self.quantity_entry = ctk.CTkEntry(add_item_frame, width=100, justify='center', font=self.main_font)
        self.quantity_entry.pack(side='right', padx=5, pady=10)
        # --- END: CONVERTED FROM GRID TO PACK (Add Item Section) ---



        table_frame = ctk.CTkFrame(self)
        table_frame.pack(fill='both', expand=True, padx=20, pady=5)
        self.tree = ttk.Treeview(table_frame, columns=("total", "price", "quantity", "product", "#"), show="headings")
        self.tree.heading("total", text="الإجمالي", anchor='center'); self.tree.heading("price", text="السعر", anchor='center'); self.tree.heading("quantity", text="الكمية", anchor='center'); self.tree.heading("product", text="الصنف", anchor='center'); self.tree.heading("#", text="#", anchor='center')
        self.tree.column("total", anchor='center', width=100); self.tree.column("price", anchor='center', width=80); self.tree.column("quantity", anchor='center', width=80); self.tree.column("product", anchor='e', width=250); self.tree.column("#", anchor='center', width=30, stretch=False)
        self.tree.pack(side="right", fill="both", expand=True)
        
        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.pack(fill='x', padx=20, pady=10)
        self.remove_item_button = ctk.CTkButton(bottom_frame, text="حذف الصنف المحدد", fg_color="red", font=self.bold_font)
        self.remove_item_button.pack(side="right", padx=10)
        self.total_value_label = ctk.CTkLabel(bottom_frame, text="الإجمالي: 0.00", font=self.bold_font, justify='left')
        self.total_value_label.pack(side="left", padx=10)

        action_buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_buttons_frame.pack(pady=10)
        self.save_button = ctk.CTkButton(action_buttons_frame, text="حفظ الفاتورة", width=150, font=self.bold_font)
        self.save_button.pack(side="right", padx=10)
        self.clear_button = ctk.CTkButton(action_buttons_frame, text="فاتورة جديدة", fg_color="gray", font=self.bold_font)
        self.clear_button.pack(side="left", padx=10)

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