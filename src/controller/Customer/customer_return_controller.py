from datetime import date, datetime
from view.Customer.customer_return_view import CustomerReturnView, END
from model.Customer.customer_return_model import CustomerReturnModel

class CustomerReturnController:
    def __init__(self, root, db_conn, distributor_name):
        self.root = root
        self.model = CustomerReturnModel(db_conn)
        self.distributor_name = distributor_name
        self.distributor_id = self.model.get_distributor_id_by_name(distributor_name)

        self.view = CustomerReturnView(self.root, self.distributor_name)

        self.customers_data = {}
        self.return_items = []

        self._load_initial_data()
        self._bind_events()

    def _load_initial_data(self):
        customers = self.model.get_customers_by_distributor(self.distributor_id)
        self.customers_data = {name: cust_id for cust_id, name in customers}
        self.view.customer_combobox.configure(values=list(self.customers_data.keys()))
        self.clear_form()
        self.view.product_entry.focus()

    def _bind_events(self):
        self.view.add_item_button.configure(command=self._add_item_to_list)
        self.view.remove_item_button.configure(command=self._remove_selected_item)
        self.view.save_button.configure(command=self._save_return)
        self.view.clear_button.configure(command=self.clear_form)
        
        self.view.product_entry.bind("<Return>", self._handle_product_entry_enter)
        self.view.quantity_entry.bind("<Return>", lambda event: self.view.price_entry.focus())
        self.view.price_entry.bind("<Return>", lambda event: self._add_item_to_list())

    def _handle_product_entry_enter(self, event=None):
        customer_name = self.view.customer_combobox.get()
        if not customer_name:
            self.view.show_error("خطأ", "الرجاء اختيار العميل أولاً.")
            return

        product_name = self.view.product_entry.get().strip()
        if not product_name:
            self.view.show_error("خطأ", "الرجاء إدخال اسم الصنف.")
            return

        product_info = self.model.get_product_by_name_and_distributor(product_name, self.distributor_id)
        if not product_info:
            self.view.show_error("خطأ", f"الصنف '{product_name}' غير موجود أو لا يتبع هذا الموزع.")
            return
            
        product_id, _, selling_price = product_info
        customer_id = self.customers_data[customer_name]

        last_price = self.model.get_last_purchase_price(customer_id, product_id, self.distributor_id)
        
        self.view.price_entry.delete(0, END)
        price_to_set = last_price if last_price is not None else selling_price
        self.view.price_entry.insert(0, f"{price_to_set:.2f}")

        self.view.quantity_entry.focus()

    def _lock_header_widgets(self):
        self.view.customer_combobox.configure(state='disabled')
        self.view.day_menu.configure(state='disabled'); self.view.month_menu.configure(state='disabled'); self.view.year_menu.configure(state='disabled')

    def _unlock_header_widgets(self):
        self.view.customer_combobox.configure(state='readonly')
        self.view.day_menu.configure(state='normal'); self.view.month_menu.configure(state='normal'); self.view.year_menu.configure(state='normal')

    def _add_item_to_list(self):
        customer_name = self.view.customer_combobox.get()
        if not customer_name: return self.view.show_error("خطأ", "الرجاء اختيار العميل أولاً.")

        product_name = self.view.product_entry.get().strip()
        if not product_name: return self.view.show_error("خطأ", "الرجاء إدخال اسم الصنف.")

        product_info = self.model.get_product_by_name_and_distributor(product_name, self.distributor_id)
        if not product_info: return self.view.show_error("خطأ", f"الصنف '{product_name}' غير موجود أو لا يتبع هذا الموزع.")
        
        product_id, _, _ = product_info

        q_str, p_str = self.view.quantity_entry.get(), self.view.price_entry.get()
        try:
            quantity, price = int(q_str), float(p_str)
            if quantity <= 0 or price < 0: raise ValueError
        except (ValueError, TypeError): return self.view.show_error("خطأ", "الكمية والسعر يجب أن يكونا أرقامًا موجبة وصحيحة.")

        if any(item['product_id'] == product_id for item in self.return_items):
            return self.view.show_warning("تنبيه", "هذا الصنف موجود بالفعل في قائمة المرتجع الحالية.")

        customer_id = self.customers_data[customer_name]
        has_purchased = self.model.check_if_customer_purchased_product(customer_id, product_id, self.distributor_id)
        
        if not has_purchased:
            proceed = self.view.ask_yes_no("تأكيد إضافة", f"هذا المكتب لم يشترِ الصنف '{product_name}' من قبل. هل أنت متأكد من تسجيل مرتجع له؟")
            if not proceed: return

        if not self.return_items: self._lock_header_widgets()

        self.return_items.append({'product_id': product_id, 'product_name': product_name, 'quantity': quantity, 'price_at_return': price, 'total': quantity * price})
        self._update_treeview()
        self._clear_item_inputs()
        self.view.product_entry.focus()

    def _update_treeview(self):
        self.view.tree.delete(*self.view.tree.get_children())
        total = sum(item['total'] for item in self.return_items)
        for index, item in enumerate(self.return_items, start=1):
            self.view.tree.insert("", END, values=(f"{item['total']:.2f}", f"{item['price_at_return']:.2f}", item['quantity'], item['product_name'], index))
        self.view.total_value_label.configure(text=f"إجمالي قيمة المرتجع: {total:.2f} ج.م")

    # <<< --- FIXED and IMPROVED item removal function --- START --->
    def _remove_selected_item(self):
        selected_item_id = self.view.tree.focus()
        if not selected_item_id:
            return self.view.show_error("خطأ", "الرجاء تحديد صنف لحذفه.")
        
        try:
            item_values = self.view.tree.item(selected_item_id)['values']
            # The custom index 'م' is the last column (index 4)
            # VIEW COLUMNS: ("total", "price", "quantity", "product", "index")
            item_index_to_delete = int(item_values[4])

            # self.return_items is a 0-based list, so we pop the item at 'index - 1'
            if 1 <= item_index_to_delete <= len(self.return_items):
                self.return_items.pop(item_index_to_delete - 1)
            else:
                # This is a safeguard in case of a mismatch between the view and the data list
                raise IndexError("فهرس العنصر المحدد في الجدول خارج نطاق قائمة الأصناف.")

            self._update_treeview()
            
            if not self.return_items:
                self._unlock_header_widgets()
        
        except (IndexError, ValueError) as e:
            # This catches errors if the row is empty, if the index isn't a number, or if the index is out of bounds.
            print(f"Error during item removal: {e}")
            self.view.show_error("خطأ", "حدث خطأ غير متوقع أثناء محاولة حذف الصنف.")
    # <<< --- FIXED and IMPROVED item removal function --- END --->


    def _save_return(self):
        customer_name = self.view.customer_combobox.get()
        if not customer_name or not self.return_items: return self.view.show_error("خطأ", "الرجاء اختيار عميل وإضافة أصناف للمرتجع.")

        try:
            return_date = datetime(int(self.view.year_menu.get()), int(self.view.month_menu.get()), int(self.view.day_menu.get())).strftime('%Y-%m-%d')
        except ValueError: return self.view.show_error("خطأ", "التاريخ المحدد غير صحيح.")

        data_to_save = {
            'customer_id': self.customers_data[customer_name],
            'distributor_id': self.distributor_id,
            'date': return_date,
            'reason': self.view.reason_entry.get(),
            'items_list': self.return_items,
            'total_amount': sum(item['total'] for item in self.return_items)
        }

        success, result = self.model.add_return_transaction(data_to_save)
        if success:
            self.view.show_info("نجاح", "تم حفظ المرتجع بنجاح.")
            if self.view.ask_yes_no("طباعة", "هل تريد طباعة إيصال المرتجع؟"):
                report_data = {
                    'return_id': result['return_id'],
                    'customer_name': customer_name,
                    'distributor_name': self.distributor_name,
                    'date': return_date,
                    'items': self.return_items,
                    'balance_before': result['balance_before'],
                    'balance_after': result['balance_after'],
                    'logo_path': self.model.get_distributor_logo_by_name(self.distributor_name),
                }
                try:
                    # Assuming the report controller exists at this path
                    from controller.Customer.customer_return_report_controller import CustomerReturnReportController
                    report_generator = CustomerReturnReportController(report_data)
                    report_generator.generate_pdf()
                except Exception as e:
                    self.view.show_error("خطأ في الطباعة", f"فشل إنشاء التقرير:\n{e}")
            self.clear_form()
        else:
            self.view.show_error("فشل الحفظ", result)

    def _clear_item_inputs(self):
        self.view.product_entry.delete(0, END)
        self.view.quantity_entry.delete(0, END)
        self.view.price_entry.delete(0, END)

    def clear_form(self):
        self._unlock_header_widgets()
        self.view.customer_combobox.set("")
        self.view.reason_entry.delete(0, END)
        today = date.today()
        self.view.day_menu.set(str(today.day)); self.view.month_menu.set(str(today.month)); self.view.year_menu.set(str(today.year))
        self.return_items = []
        self._update_treeview()
        self._clear_item_inputs()
        self.view.product_entry.focus()