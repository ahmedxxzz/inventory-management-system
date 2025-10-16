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
        self.products_data = {}
        self.return_items = []

        self._load_initial_data()
        self._bind_events()

    def _load_initial_data(self):
        customers = self.model.get_customers_by_distributor(self.distributor_id)
        self.customers_data = {name: cust_id for cust_id, name in customers}
        self.view.customer_combobox.configure(values=list(self.customers_data.keys()))
        
        self.clear_form()

    def _bind_events(self):
        # <<< MODIFICATION: Bind the customer combobox to a new function
        self.view.customer_combobox.configure(command=self._on_customer_select)
        self.view.product_combobox.configure(command=self._on_product_select)
        self.view.add_item_button.configure(command=self._add_item_to_list)
        self.view.remove_item_button.configure(command=self._remove_selected_item)
        self.view.save_button.configure(command=self._save_return)
        self.view.clear_button.configure(command=self.clear_form)

    # <<< --- NEW FUNCTION TO HANDLE CUSTOMER SELECTION --- START --->
    def _on_customer_select(self, selected_customer_name):
        """
        Triggered when a customer is selected. Fetches the products they have purchased.
        """
        # Clear any existing items if the customer is changed
        self.return_items = []
        self._update_treeview()
        self._clear_item_inputs()
        
        customer_id = self.customers_data.get(selected_customer_name)
        if not customer_id:
            # If selection is cleared, empty the product list
            self.products_data = {}
            self.view.product_combobox.configure(values=[])
            return

        # Fetch products specifically for this customer and distributor
        products = self.model.get_products_purchased_by_customer(customer_id, self.distributor_id)
        self.products_data = {name: {'id': prod_id, 'price': price} for prod_id, name, price in products}
        self.view.product_combobox.configure(values=list(self.products_data.keys()))
    # <<< --- NEW FUNCTION TO HANDLE CUSTOMER SELECTION --- END --->

    def _on_product_select(self, product_name):
        # This function remains the same, it works with the now-filtered product list
        product_info = self.products_data.get(product_name)
        self.view.price_entry.delete(0, END)
        if product_info and product_info['price'] is not None:
            self.view.price_entry.insert(0, f"{product_info['price']:.2f}")

    def _lock_header_widgets(self):
        self.view.customer_combobox.configure(state='disabled')
        self.view.day_menu.configure(state='disabled'); self.view.month_menu.configure(state='disabled'); self.view.year_menu.configure(state='disabled')

    def _unlock_header_widgets(self):
        self.view.customer_combobox.configure(state='readonly')
        self.view.day_menu.configure(state='normal'); self.view.month_menu.configure(state='normal'); self.view.year_menu.configure(state='normal')

    def _add_item_to_list(self):
        # This function remains the same
        p_name = self.view.product_combobox.get()
        if not p_name: return self.view.show_error("خطأ", "الرجاء اختيار صنف.")
        
        q_str, p_str = self.view.quantity_entry.get(), self.view.price_entry.get()
        try:
            quantity, price = int(q_str), float(p_str)
            if quantity <= 0 or price < 0: raise ValueError
        except ValueError: return self.view.show_error("خطأ", "الكمية والسعر يجب أن يكونا أرقامًا موجبة.")
        
        p_id = self.products_data[p_name]['id']
        if any(item['product_id'] == p_id for item in self.return_items):
            return self.view.show_warning("تنبيه", "هذا الصنف موجود بالفعل في قائمة المرتجع.")
        
        if not self.return_items: self._lock_header_widgets()

        self.return_items.append({'product_id': p_id, 'product_name': p_name, 'quantity': quantity, 'price_at_return': price, 'total': quantity * price})
        self._update_treeview()
        self._clear_item_inputs()

    def _update_treeview(self):
        # This function remains the same
        self.view.tree.delete(*self.view.tree.get_children())
        total = sum(item['total'] for item in self.return_items)
        for item in self.return_items:
            self.view.tree.insert("", END, values=(f"{item['total']:.2f}", f"{item['price_at_return']:.2f}", item['quantity'], item['product_name']))
        self.view.total_value_label.configure(text=f"إجمالي قيمة المرتجع: {total:.2f} ج.م")

    def _remove_selected_item(self):
        # This function remains the same
        sel = self.view.tree.focus()
        if not sel: return self.view.show_error("خطأ", "الرجاء تحديد صنف لحذفه.")
        p_name = self.view.tree.item(sel)['values'][3]
        self.return_items = [i for i in self.return_items if i['product_name'] != p_name]
        self._update_treeview()
        if not self.return_items: self._unlock_header_widgets()

    def _save_return(self):
        # This function remains the same
        customer_name = self.view.customer_combobox.get()
        if not customer_name or not self.return_items:
            return self.view.show_error("خطأ", "الرجاء اختيار عميل وإضافة أصناف للمرتجع.")

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
                # 2. Generate the report
                try:
                    from controller.Customer.customer_return_report_controller import CustomerReturnReportController
                    report_generator = CustomerReturnReportController(report_data)
                    report_generator.generate_pdf()
                except Exception as e:
                    self.view.show_error("خطأ في الطباعة", f"فشل إنشاء التقرير:\n{e}")
            self.clear_form()
        else:
            self.view.show_error("فشل الحفظ", result)

    def _clear_item_inputs(self):
        # This function remains the same
        self.view.product_combobox.set(""); self.view.quantity_entry.delete(0, END); self.view.price_entry.delete(0, END)

    def clear_form(self):
        # <<< MODIFICATION: Ensure product list is cleared on full form clear
        self._unlock_header_widgets()
        self.view.customer_combobox.set("")
        self.view.product_combobox.configure(values=[]) # Clear product dropdown
        self.view.reason_entry.delete(0, END)
        today = date.today()
        self.view.day_menu.set(str(today.day)); self.view.month_menu.set(str(today.month)); self.view.year_menu.set(str(today.year))
        self.return_items = []
        self._update_treeview()
        self._clear_item_inputs()
