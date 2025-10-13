import customtkinter as ctk
from datetime import date, datetime

class FactoryPayView(ctk.CTkFrame):
    def __init__(self, root):
        """
        Create the factory pay main frame.
        Args:
            root (ctk.CTkFrame): The parent widget.
        """
        super().__init__(root)
        self.pack(fill='both', padx=10, pady=10, expand=True)
        self.configure(fg_color="transparent")
        
        # Main Title
        title_label = ctk.CTkLabel(self, text="تسجيل دفعة سداد لمصنع", font=("Arial", 14, "bold"),)
        title_label.pack(pady=20)
        
        # Form Frame
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill='x', padx=50, pady=10)
        # Configure column 0 (inputs) to expand, and column 1 (labels) to stay fixed
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=0)

        # --- Factory Selection ---
        # Label is in column 1, aligned to the right (east)
        ctk.CTkLabel(form_frame, text=":اختر المصنع", font=("Arial", 14, "bold")).grid(row=0, column=1, padx=10, pady=10, sticky="e")
        # Combobox is in column 0, expands horizontally
        self.factory_combobox = ctk.CTkComboBox(form_frame, values=[], state="readonly", justify='right')
        self.factory_combobox.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # --- POINT 1: Factory Balance Label is REMOVED ---
        
        # --- Amount Paid ---
        ctk.CTkLabel(form_frame, text=":المبلغ المدفوع", font=("Arial", 14, "bold"),).grid(row=1, column=1, padx=10, pady=10, sticky="e")
        self.amount_entry = ctk.CTkEntry(form_frame, placeholder_text="ادخل المبلغ المدفوع...", justify='right')
        self.amount_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # --- Wallet Selection ---
        ctk.CTkLabel(form_frame, text=":الدفع من خزنة", font=("Arial", 14, "bold"),).grid(row=2, column=1, padx=10, pady=10, sticky="e")
        self.wallet_combobox = ctk.CTkComboBox(form_frame, values=[], state="readonly", justify='right')
        self.wallet_combobox.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        # --- Wallet Balance Display ---
        self.wallet_balance_label = ctk.CTkLabel(form_frame, text="الرصيد المتاح: 0.00", font=("Arial", 14, "bold") ,text_color="gray")
        self.wallet_balance_label.grid(row=3, column=0, padx=10, sticky="e") # Aligned to the right of its cell

        # --- POINT 2: Date Selection with Option Menus ---
        ctk.CTkLabel(form_frame, text=":تاريخ الدفعة", font=("Arial", 14, "bold"),).grid(row=4, column=1, padx=10, pady=10, sticky="e")
        
        # Frame to hold the date menus together
        date_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        date_frame.grid(row=4, column=0, padx=10, pady=10, sticky="e") # Align frame to the right

        current_year = date.today().year
        year_list = [str(y) for y in range(current_year - 5, current_year + 1)]
        month_list = [str(m) for m in range(1, 13)]
        day_list = [str(d) for d in range(1, 32)]

        self.year_menu = ctk.CTkOptionMenu(date_frame, values=year_list)
        self.month_menu = ctk.CTkOptionMenu(date_frame, values=month_list)
        self.day_menu = ctk.CTkOptionMenu(date_frame, values=day_list)

        # Pack them right-to-left: Year, then Month, then Day
        self.year_menu.pack(side="right", padx=2)
        self.month_menu.pack(side="right", padx=2)
        self.day_menu.pack(side="right", padx=2)

        # --- Buttons Frame ---
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.pack(pady=20)
        
        self.save_button = ctk.CTkButton(buttons_frame, text="حفظ الدفعة", width=150, font=("Arial", 14, "bold"),)
        self.save_button.pack(side="right", padx=10)
        
        self.clear_button = ctk.CTkButton(buttons_frame, text="مسح الحقول", command=self.clear_form, fg_color="gray", font=("Arial", 14, "bold"))
        self.clear_button.pack(side="left", padx=10)

    def clear_form(self):
        """Clears all input fields in the form."""
        self.factory_combobox.set("")
        self.amount_entry.delete(0, 'end')
        self.wallet_combobox.set("")
        self.wallet_balance_label.configure(text="الرصيد المتاح: 0.00")
        
        # Set date menus to today's date
        today = date.today()
        self.day_menu.set(str(today.day))
        self.month_menu.set(str(today.month))
        self.year_menu.set(str(today.year))