import customtkinter as ctk
from tkinter import ttk, messagebox
import arabic_reshaper
from bidi.algorithm import get_display
from datetime import datetime

class FactoryBuyView(ctk.CTkFrame):
    def __init__(self, master):
        """
        Create a frame for the factory buying process.
        """
        super().__init__(master)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # --- Left Frame (Input Fields) ---
        self.left_frame = ctk.CTkFrame(self, corner_radius=10)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.left_frame.grid_columnconfigure(1, weight=1)

        # Bill Header
        ctk.CTkLabel(self.left_frame, text=self._rtl_text("بيانات الفاتورة"), font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 20))
        
        ctk.CTkLabel(self.left_frame, text=self._rtl_text("اختر المصنع:")).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.factory_combobox = ctk.CTkComboBox(self.left_frame, values=[], justify='right')
        self.factory_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # --- NEW: Date Option Menus ---
        ctk.CTkLabel(self.left_frame, text=self._rtl_text("تاريخ الفاتورة:")).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.date_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        self.date_frame.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.date_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Populate date options
        current_year = datetime.now().year
        years = [str(y) for y in range(current_year, current_year - 6, -1)]
        months = [f"{m:02d}" for m in range(1, 13)]
        days = [f"{d:02d}" for d in range(1, 32)]

        self.year_optionmenu = ctk.CTkOptionMenu(self.date_frame, values=years)
        self.month_optionmenu = ctk.CTkOptionMenu(self.date_frame, values=months)
        self.day_optionmenu = ctk.CTkOptionMenu(self.date_frame, values=days)
        
        self.year_optionmenu.grid(row=0, column=2, padx=(2,0), sticky="ew")
        self.month_optionmenu.grid(row=0, column=1, padx=2, sticky="ew")
        self.day_optionmenu.grid(row=0, column=0, padx=(0,2), sticky="ew")
        
        self.set_default_date() # Set to today's date initially

        # Separator
        ttk.Separator(self.left_frame, orient='horizontal').grid(row=3, column=0, columnspan=2, sticky='ew', pady=20, padx=10)

        # Item Details
        ctk.CTkLabel(self.left_frame, text=self._rtl_text("إضافة أصناف الفاتورة"), font=ctk.CTkFont(size=14, weight="bold")).grid(row=4, column=0, columnspan=2, padx=10, pady=(0, 10))

        ctk.CTkLabel(self.left_frame, text=self._rtl_text("اسم المنتج:")).grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.product_name_entry = ctk.CTkEntry(self.left_frame, justify='right')
        self.product_name_entry.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(self.left_frame, text=self._rtl_text("الكمية:")).grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.quantity_entry = ctk.CTkEntry(self.left_frame, justify='right')
        self.quantity_entry.grid(row=6, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(self.left_frame, text=self._rtl_text("سعر القطعة:")).grid(row=7, column=0, padx=10, pady=5, sticky="w")
        self.price_entry = ctk.CTkEntry(self.left_frame, justify='right')
        self.price_entry.grid(row=7, column=1, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(self.left_frame, text=self._rtl_text("خصم للقطعة:")).grid(row=8, column=0, padx=10, pady=5, sticky="w")
        self.discount_entry = ctk.CTkEntry(self.left_frame, placeholder_text="0.00", justify='right')
        self.discount_entry.grid(row=8, column=1, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(self.left_frame, text=self._rtl_text("اختر الموزع (للصنف الجديد):")).grid(row=9, column=0, padx=10, pady=5, sticky="w")
        self.distributor_combobox = ctk.CTkComboBox(self.left_frame, values=[], state="disabled", justify='right')
        self.distributor_combobox.grid(row=9, column=1, padx=10, pady=5, sticky="ew")

        # Action Buttons Frame
        self.action_buttons_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        self.action_buttons_frame.grid(row=10, column=0, columnspan=2, pady=15)
        
        self.add_item_button = ctk.CTkButton(self.action_buttons_frame, text=self._rtl_text("إضافة الصنف"))
        self.add_item_button.pack(side="right", padx=5)

        self.update_item_button = ctk.CTkButton(self.action_buttons_frame, text=self._rtl_text("تعديل الصنف"), fg_color="#e67e22", hover_color="#d35400")
        self.delete_item_button = ctk.CTkButton(self.action_buttons_frame, text=self._rtl_text("حذف الصنف"), fg_color="#c0392b", hover_color="#e74c3c")
        self.clear_selection_button = ctk.CTkButton(self.action_buttons_frame, text=self._rtl_text("إلغاء التحديد"), fg_color="gray")

        # Separator
        ttk.Separator(self.left_frame, orient='horizontal').grid(row=11, column=0, columnspan=2, sticky='ew', pady=20, padx=10)
        
        # Payment Status
        ctk.CTkLabel(self.left_frame, text=self._rtl_text("حالة الدفع:")).grid(row=12, column=0, padx=10, pady=5, sticky="w")
        self.payment_status_var = ctk.StringVar(value="آجل")
        self.paid_radio = ctk.CTkRadioButton(self.left_frame, text=self._rtl_text("نقدي (مدفوعة)"), variable=self.payment_status_var, value="نقدي")
        self.unpaid_radio = ctk.CTkRadioButton(self.left_frame, text=self._rtl_text("آجل (غير مدفوعة)"), variable=self.payment_status_var, value="آجل")
        self.paid_radio.grid(row=13, column=1, padx=10, pady=5, sticky="w")
        self.unpaid_radio.grid(row=12, column=1, padx=10, pady=5, sticky="w")

        # --- Right Frame (Bill Preview) ---
        self.right_frame = ctk.CTkFrame(self, corner_radius=10)
        self.right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.right_frame.grid_rowconfigure(1, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.right_frame, text=self._rtl_text("تفاصيل الفاتورة الحالية"), font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, padx=10, pady=10)

        # Treeview for bill items
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2a2d2e", foreground="white", fieldbackground="#343638", borderwidth=0, rowheight=25)
        style.map('Treeview', background=[('selected', '#24527d')])
        style.configure("Treeview.Heading", font=('Calibri', 10,'bold'))
        
        tree_columns = ("total", "discount", "price", "quantity", "product_name")
        self.bill_items_table = ttk.Treeview(self.right_frame, columns=tree_columns, show="headings", selectmode="browse")
        
        self.bill_items_table.heading("product_name", text=self._rtl_text("اسم المنتج"))
        self.bill_items_table.heading("quantity", text=self._rtl_text("الكمية"))
        self.bill_items_table.heading("price", text=self._rtl_text("السعر"))
        self.bill_items_table.heading("discount", text=self._rtl_text("الخصم"))
        self.bill_items_table.heading("total", text=self._rtl_text("الإجمالي"))

        self.bill_items_table.column("product_name", width=150, anchor="e")
        for col in tree_columns[1:]:
            self.bill_items_table.column(col, width=80, anchor="center")

        self.bill_items_table.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Total Amount Display
        self.total_frame = ctk.CTkFrame(self.right_frame)
        self.total_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.total_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(self.total_frame, text=self._rtl_text("إجمالي الفاتورة:"), font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, padx=10, pady=5)
        self.total_amount_label = ctk.CTkLabel(self.total_frame, text="0.00", font=ctk.CTkFont(size=18, weight="bold"), text_color="#22a6b3")
        self.total_amount_label.grid(row=0, column=1, padx=10, pady=5, sticky="e")
        
        # --- Bottom Buttons ---
        self.bottom_buttons_frame = ctk.CTkFrame(self.right_frame)
        self.bottom_buttons_frame.grid(row=3, column=0, padx=10, pady=(10, 20), sticky="ew")
        
        self.save_bill_button = ctk.CTkButton(self.bottom_buttons_frame, text=self._rtl_text("حفظ الفاتورة"), height=40, font=ctk.CTkFont(size=15))
        self.save_bill_button.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self.cancel_bill_button = ctk.CTkButton(self.bottom_buttons_frame, text=self._rtl_text("إلغاء الفاتورة"), height=40, font=ctk.CTkFont(size=15), fg_color="#c0392b", hover_color="#e74c3c")
        self.cancel_bill_button.pack(side="left", fill="x", expand=True, padx=(5, 0))

        self.show_add_mode_buttons()

    # --- Helper function for RTL text ---
    def _rtl_text(self, text):
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)
        return bidi_text
        
    # --- Methods for Controller to use ---
    def set_default_date(self):
        """Sets the date option menus to the current date."""
        now = datetime.now()
        self.year_optionmenu.set(str(now.year))
        self.month_optionmenu.set(f"{now.month:02d}")
        self.day_optionmenu.set(f"{now.day:02d}")
        
    def get_selected_date_str(self):
        """Gets the selected date and returns it as a 'YYYY-MM-DD' string."""
        year = self.year_optionmenu.get()
        month = self.month_optionmenu.get()
        day = self.day_optionmenu.get()
        return f"{year}-{month}-{day}"

    def set_header_fields_state(self, state):
        self.factory_combobox.configure(state=state)
        self.year_optionmenu.configure(state=state)
        self.month_optionmenu.configure(state=state)
        self.day_optionmenu.configure(state=state)
        self.paid_radio.configure(state=state)
        self.unpaid_radio.configure(state=state)

    def show_add_mode_buttons(self):
        self.add_item_button.pack(side="right", padx=5)
        self.update_item_button.pack_forget()
        self.delete_item_button.pack_forget()
        self.clear_selection_button.pack_forget()

    def show_edit_mode_buttons(self):
        self.add_item_button.pack_forget()
        self.update_item_button.pack(side="right", padx=5)
        self.delete_item_button.pack(side="right", padx=5)
        self.clear_selection_button.pack(side="left", padx=5)
        
    def populate_item_inputs(self, item_data):
        self.product_name_entry.delete(0, 'end')
        self.product_name_entry.insert(0, item_data['product_name'])
        self.quantity_entry.delete(0, 'end')
        self.quantity_entry.insert(0, str(item_data['quantity']))
        self.price_entry.delete(0, 'end')
        self.price_entry.insert(0, f"{item_data['price']:.2f}")
        self.discount_entry.delete(0, 'end')
        self.discount_entry.insert(0, f"{item_data['discount']:.2f}")
        
    def set_distributor(self, distributor_name):
        if distributor_name:
            self.distributor_combobox.set(distributor_name)
            self.distributor_combobox.configure(state="disabled")
        else:
            self.distributor_combobox.set("")

    def set_price(self, price):
        self.price_entry.delete(0, 'end')
        if price is not None:
            self.price_entry.insert(0, f"{price:.2f}")
        
    def get_selected_item_id(self):
        selection = self.bill_items_table.selection()
        return selection[0] if selection else None

    def update_table_row(self, item_id, item_data):
        values = (
            f"{item_data['total']:.2f}", f"{item_data['discount']:.2f}",
            f"{item_data['price']:.2f}", item_data['quantity'],
            self._rtl_text(item_data['product_name'])
        )
        self.bill_items_table.item(item_id, values=values)

    def delete_table_row(self, item_id):
        self.bill_items_table.delete(item_id)

    def populate_combobox(self, combobox, data):
        combobox.configure(values=data)
        if data:
            combobox.set(data[0])

    def get_item_data(self):
        return {
            "product_name": self.product_name_entry.get().strip(),
            "quantity": self.quantity_entry.get().strip(),
            "price": self.price_entry.get().strip(),
            "discount": self.discount_entry.get().strip() or "0.00",
            "distributor": self.distributor_combobox.get()
        }
        
    def get_bill_header_data(self):
        return {
            "factory_name": self.factory_combobox.get(),
            "date": self.get_selected_date_str(), # Use the new method
            "is_paid": 1 if self.payment_status_var.get() == "نقدي" else 0
        }

    def add_item_to_table(self, item_data):
        values = (
            f"{item_data['total']:.2f}", f"{item_data['discount']:.2f}",
            f"{item_data['price']:.2f}", item_data['quantity'],
            self._rtl_text(item_data['product_name'])
        )
        self.bill_items_table.insert("", "end", values=values, iid=item_data['id'])
        
    def update_total_display(self, new_total):
        self.total_amount_label.configure(text=f"{new_total:.2f}")

    def clear_item_inputs(self, clear_product_name=True):
        if clear_product_name:
            self.product_name_entry.delete(0, 'end')
        self.quantity_entry.delete(0, 'end')
        self.price_entry.delete(0, 'end')
        self.discount_entry.delete(0, 'end')
        self.distributor_combobox.set("")
        self.distributor_combobox.configure(state="disabled")
        if clear_product_name:
            self.product_name_entry.focus()
        
    def clear_bill_form(self):
        self.clear_item_inputs()
        for item in self.bill_items_table.get_children():
            self.bill_items_table.delete(item)
        self.update_total_display(0.0)
        self.set_header_fields_state("normal")
        self.set_default_date() # Reset date to today

    def show_error(self, title, message):
        messagebox.showerror(title, message)

    def show_info(self, title, message):
        messagebox.showinfo(title, message)

    def ask_yes_no(self, title, message):
        return messagebox.askyesno(title, message)