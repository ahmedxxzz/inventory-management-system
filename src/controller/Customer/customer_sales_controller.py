import uuid
from datetime import date, datetime
from view.Customer.customer_sales_view import CustomerSalesView, END
from model.Customer.customer_sales_model import CustomerSalesModel

class CustomerSalesController:
    def __init__(self, root, db_conn, distributor_name):
        self.root = root
        self.model = CustomerSalesModel(db_conn)
        self.distributor_name = distributor_name
        self.distributor_id = self.model.get_distributor_id_by_name(distributor_name)
        
        self.view = CustomerSalesView(self.root, self.distributor_name)
        
        self.customers_data = {}
        self.bill_items = []
        self.selected_product_info = None

        self._load_initial_data()
        self._bind_events()

    def _load_initial_data(self):
        customers = self.model.get_customers_by_distributor(self.distributor_id)
        if customers:
            self.customers_data = {name: cust_id for cust_id, name in customers}
            self.view.customer_combobox.configure(values=list(self.customers_data.keys()))
        self.clear_form()
        
    def _bind_events(self):
        # Existing bindings
        self.view.product_entry.bind("<FocusOut>", self._on_product_focus_out)
        self.view.add_item_button.configure(command=self._add_item_to_list)
        self.view.remove_item_button.configure(command=self._remove_selected_item)
        self.view.save_button.configure(command=self._save_bill)
        self.view.clear_button.configure(command=self.clear_form)
        self.view.discount_value_entry.bind("<KeyRelease>", lambda e: self._update_treeview())
        self.view.discount_percentage_entry.bind("<KeyRelease>", lambda e: self._update_treeview())
        
        # --- NEW: Enter key navigation bindings ---
        self.view.product_entry.bind("<Return>", self._navigate_to_quantity)
        self.view.quantity_entry.bind("<Return>", self._navigate_to_price)
        self.view.price_entry.bind("<Return>", self._add_item_on_enter)

    # --- NEW: Navigation handler methods ---
    def _navigate_to_quantity(self, event):
        """Trigger validation and move to quantity if product is valid."""
        self._on_product_focus_out()
        if self.selected_product_info:
            self.view.quantity_entry.focus_set()
        return "break" # Prevents the default 'ding' sound

    def _navigate_to_price(self, event):
        """Move focus to the price entry."""
        self.view.price_entry.focus_set()
        return "break"

    def _add_item_on_enter(self, event):
        """Trigger the add item action when Enter is pressed in the price field."""
        self._add_item_to_list()
        return "break"
    
    def _on_product_focus_out(self, event=None):
        self.selected_product_info = None
        self.view.price_entry.delete(0, END)
        product_name = self.view.product_entry.get().strip()
        if not product_name: return
        status, data = self.model.get_product_details_by_name(product_name, self.distributor_id)
        if status == "NOT_FOUND":
            self.view.show_error("خطأ", f"الصنف '{product_name}' غير موجود في المخزن.")
            return
        if status == "WRONG_DISTRIBUTOR":
            self.view.show_error("خطأ", f"الصنف '{product_name}' لا يتبع الموزع '{self.distributor_name}'.")
            return
        if status == "OK":
            self.selected_product_info = data
            if data['price'] > 0:
                self.view.price_entry.insert(0, f"{data['price']:.2f}")
            else:
                self.view.price_entry.configure(placeholder_text="أدخل سعر البيع")
            return

    def _lock_header_widgets(self):
        self.view.customer_combobox.configure(state='disabled')
        self.view.day_menu.configure(state='disabled'); self.view.month_menu.configure(state='disabled'); self.view.year_menu.configure(state='disabled')
        self.view.paid_switch.configure(state='disabled')
        
    def _unlock_header_widgets(self):
        self.view.customer_combobox.configure(state='readonly')
        self.view.day_menu.configure(state='normal'); self.view.month_menu.configure(state='normal'); self.view.year_menu.configure(state='normal')
        self.view.paid_switch.configure(state='normal')

    def _add_item_to_list(self):
        if not self.view.customer_combobox.get():
            return self.view.show_error("خطأ", "الرجاء اختيار العميل (المكتب) أولاً.")

        is_first_item = not self.bill_items
        if is_first_item:
            discount_value = self.view.discount_value_entry.get()
            discount_percentage = self.view.discount_percentage_entry.get()
            if not discount_value and not discount_percentage:
                if not self.view.ask_yes_no("تأكيد", "لم تقم بإدخال أي خصم. هل تريد المتابعة بدون خصم؟"):
                    return
            self.view.lock_discount_widgets()
        
        if not self.selected_product_info:
            # Re-validate in case user directly clicks 'Add' button without leaving the field
            self._on_product_focus_out()
            if not self.selected_product_info:
                return self.view.show_error("خطأ", "الرجاء إدخال اسم صنف صحيح والتحقق منه.")
        
        try:
            quantity = int(self.view.quantity_entry.get())
            price = float(self.view.price_entry.get())
            if quantity <= 0 or price <= 0: raise ValueError
            if quantity > self.selected_product_info['stock']:
                return self.view.show_warning("تنبيه", f"الكمية المطلوبة ({quantity}) أكبر من المتاح بالمخزن ({self.selected_product_info['stock']}).")
        except (ValueError, TypeError):
            return self.view.show_error("خطأ", "الكمية والسعر يجب أن تكون أرقامًا صحيحة وموجبة.")

        p_id = self.selected_product_info['id']
        if any(item['product_id'] == p_id for item in self.bill_items):
            return self.view.show_warning("تنبيه", "هذا الصنف موجود بالفعل في الفاتورة.")
        
        if is_first_item: self._lock_header_widgets()
        
        item_data = {
            'iid': str(uuid.uuid4()), 'product_id': p_id, 'product_name': self.selected_product_info['name'], 
            'quantity': quantity, 'price': price, 'initial_price': self.selected_product_info['price']
        }
        self.bill_items.append(item_data)
        self._update_treeview()
        self._clear_item_inputs()

    def _remove_selected_item(self):
        selected_iid = self.view.tree.focus()
        if not selected_iid:
            return self.view.show_error("خطأ", "الرجاء تحديد صنف من الجدول لحذفه.")
        self.bill_items = [item for item in self.bill_items if item['iid'] != selected_iid]
        self._update_treeview()
        if not self.bill_items:
            self._unlock_header_widgets()
            self.view.unlock_discount_widgets()

    def _save_bill(self):
        customer_name = self.view.customer_combobox.get()
        if not customer_name or not self.bill_items:
            return self.view.show_error("خطأ", "الرجاء اختيار عميل وإضافة أصناف للفاتورة.")

        try:
            discount_value = float(self.view.discount_value_entry.get() or 0)
            discount_percentage = float(self.view.discount_percentage_entry.get() or 0)
            if discount_value > 0 and discount_percentage > 0:
                return self.view.show_error("خطأ في الخصم", "لا يمكن استخدام نوعي الخصم (قيمة ونسبة) معًا.\nالرجاء إدخال قيمة في حقل واحد فقط.")
        except ValueError:
            return self.view.show_error("خطأ", "قيم الخصم يجب أن تكون أرقامًا.")

        try:
            bill_date = datetime(int(self.view.year_menu.get()), int(self.view.month_menu.get()), int(self.view.day_menu.get())).strftime('%Y-%m-%d')
        except ValueError:
            return self.view.show_error("خطأ", "التاريخ المحدد غير صحيح.")
        
        items_for_db = []; items_for_report = []; gross_total = 0; total_discount_amount = 0
        for item in self.bill_items:
            price_after_value_discount = item['price'] - discount_value
            percentage_discount_amount = price_after_value_discount * (discount_percentage / 100)
            total_discount_per_piece = discount_value + percentage_discount_amount
            gross_total += item['price'] * item['quantity']
            total_discount_amount += total_discount_per_piece * item['quantity']
            items_for_db.append({'product_id': item['product_id'], 'quantity': item['quantity'], 'price': item['price'], 'discount': total_discount_per_piece, 'initial_price': item['initial_price']})
            report_item = item.copy(); report_item['discount'] = total_discount_per_piece; items_for_report.append(report_item)
        net_total = gross_total - total_discount_amount
        data_to_save = {'customer_id': self.customers_data[customer_name], 'distributor_id': self.distributor_id, 'date': bill_date, 'is_paid': self.view.paid_switch.get(), 'items_list': items_for_db, 'total_amount': net_total}
        
        success, result = self.model.add_sales_transaction(data_to_save)
        if success:
            self.view.show_info("نجاح", "تم حفظ الفاتورة بنجاح.")
            if self.view.ask_yes_no("طباعة", "هل تريد طباعة الفاتورة؟"):
                report_data = {'sales_bill_id': result['sales_bill_id'], 'customer_name': customer_name, 'distributor_name': self.distributor_name, 'date': bill_date, 'items': items_for_report, 'is_paid': data_to_save['is_paid'], 'balance_before': result['balance_before'], 'balance_after': result['balance_after'], 'logo_path': self.model.get_distributor_logo_by_name(self.distributor_name)}
                from controller.Customer.sales_report_controller import SalesReportController
                report_generator = SalesReportController(report_data)
                report_generator.generate_pdf()
            self.clear_form()
        else:
            self.view.show_error("فشل الحفظ", result)

    def _update_treeview(self):
        self.view.tree.delete(*self.view.tree.get_children())
        try:
            discount_value = float(self.view.discount_value_entry.get() or 0)
            discount_percentage = float(self.view.discount_percentage_entry.get() or 0)
        except ValueError:
            discount_value, discount_percentage = 0.0, 0.0
        gross_total = 0; total_discount_amount = 0
        for i, item in enumerate(self.bill_items, 1):
            price_after_value_discount = item['price'] - discount_value
            percentage_discount_for_item = price_after_value_discount * (discount_percentage / 100)
            final_price_per_item = price_after_value_discount - percentage_discount_for_item
            item_total = final_price_per_item * item['quantity']
            gross_total += item['price'] * item['quantity']
            total_discount_amount += (item['price'] - final_price_per_item) * item['quantity']
            self.view.tree.insert("", END, iid=item['iid'], values=(f"{item_total:.2f}", f"{item['price']:.2f}", item['quantity'], item['product_name'], i))
        net_total = gross_total - total_discount_amount
        total_text = (f"الإجمالي قبل الخصم: {gross_total:.2f} | " f"مجموع الخصم: {total_discount_amount:.2f} | " f"صافي الفاتورة: {net_total:.2f} ج.م")
        self.view.total_value_label.configure(text=total_text)

    def _clear_item_inputs(self):
        self.view.product_entry.delete(0, END)
        self.view.quantity_entry.delete(0, END)
        self.view.price_entry.delete(0, END)
        self.selected_product_info = None
        # --- NEW: Set focus back to the product entry for fast input ---
        self.view.product_entry.focus_set()
        
    def clear_form(self):
        self._unlock_header_widgets(); self.view.unlock_discount_widgets()
        self.view.customer_combobox.set(""); self.view.paid_switch.deselect()
        today = date.today()
        self.view.day_menu.set(f"{today.day:02d}"); self.view.month_menu.set(f"{today.month:02d}"); self.view.year_menu.set(str(today.year))
        self.view.discount_value_entry.delete(0, END); self.view.discount_percentage_entry.delete(0, END)
        self.bill_items = []; self._update_treeview(); self._clear_item_inputs()