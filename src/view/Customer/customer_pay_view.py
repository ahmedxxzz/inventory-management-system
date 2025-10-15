import customtkinter as ctk
from tkinter import messagebox, END
from datetime import date

class CustomerPayView(ctk.CTkFrame):
    def __init__(self, root, distributor_name):
        super().__init__(root)
        self.pack(fill='both', padx=10, pady=10, expand=True)
        self.configure(fg_color="transparent")

        self.main_font = ctk.CTkFont(family="Arial", size=14)
        self.bold_font = ctk.CTkFont(family="Arial", size=14, weight="bold")
        self.title_font = ctk.CTkFont(family="Arial", size=20, weight="bold")
        
        title_text = f"تسجيل دفعة تحصيل من مكتب (موزع: {distributor_name})"
        title_label = ctk.CTkLabel(self, text=title_text, font=self.title_font)
        title_label.pack(pady=20)
        
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill='x', padx=50, pady=10)
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=0)

        ctk.CTkLabel(form_frame, text=":اختر المكتب", font=self.main_font).grid(row=0, column=1, padx=(10, 20), pady=10, sticky="e")
        self.customer_combobox = ctk.CTkComboBox(form_frame, values=[], state="readonly", justify='right', font=self.main_font)
        self.customer_combobox.grid(row=0, column=0, padx=(20, 10), pady=10, sticky="ew")

        # Label to show customer's current balance
        self.customer_balance_label = ctk.CTkLabel(form_frame, text="الرصيد الحالي: 0.00", font=ctk.CTkFont(size=12), text_color="gray")
        self.customer_balance_label.grid(row=1, column=0, padx=(20, 10), sticky="e")
        
        ctk.CTkLabel(form_frame, text=":المبلغ المحصَّل", font=self.main_font).grid(row=2, column=1, padx=(10, 20), pady=10, sticky="e")
        self.amount_entry = ctk.CTkEntry(form_frame, placeholder_text="ادخل المبلغ المستلم...", justify='right', font=self.main_font)
        self.amount_entry.grid(row=2, column=0, padx=(20, 10), pady=10, sticky="ew")

        ctk.CTkLabel(form_frame, text=":الإيداع في خزنة", font=self.main_font).grid(row=3, column=1, padx=(10, 20), pady=10, sticky="e")
        self.wallet_combobox = ctk.CTkComboBox(form_frame, values=[], state="readonly", justify='right', font=self.main_font)
        self.wallet_combobox.grid(row=3, column=0, padx=(20, 10), pady=10, sticky="ew")

        ctk.CTkLabel(form_frame, text=":تاريخ التحصيل", font=self.main_font).grid(row=4, column=1, padx=(10, 20), pady=10, sticky="e")
        date_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        date_frame.grid(row=4, column=0, padx=(20, 10), pady=10, sticky="e")
        year_list = [str(y) for y in range(date.today().year - 5, date.today().year + 1)]
        self.year_menu = ctk.CTkOptionMenu(date_frame, values=year_list, font=self.main_font)
        self.month_menu = ctk.CTkOptionMenu(date_frame, values=[str(m) for m in range(1, 13)], font=self.main_font)
        self.day_menu = ctk.CTkOptionMenu(date_frame, values=[str(d) for d in range(1, 32)], font=self.main_font)
        self.year_menu.pack(side="right", padx=2); self.month_menu.pack(side="right", padx=2); self.day_menu.pack(side="right", padx=2)

        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.pack(pady=20)
        self.save_button = ctk.CTkButton(buttons_frame, text="حفظ الدفعة", width=150, font=self.bold_font)
        self.save_button.pack(side="right", padx=10)
        self.clear_button = ctk.CTkButton(buttons_frame, text="مسح الحقول", fg_color="gray", font=self.bold_font)
        self.clear_button.pack(side="left", padx=10)

    # Messagebox wrappers
    def show_error(self, title, message): messagebox.showerror(title, message, parent=self)
    def show_info(self, title, message): messagebox.showinfo(title, message, parent=self)
    def ask_yes_no(self, title, message): return messagebox.askyesno(title, message, parent=self)

