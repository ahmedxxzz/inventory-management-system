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
        self.products_data = {}
        self.bill_items = []

        self._load_initial_data()
        self._bind_events()

    # ... (_load_initial_data, _bind_events, locking/unlocking methods remain the same) ...
    def _load_initial_data(self):
        customers = self.model.get_customers_by_distributor(self.distributor_id)
        self.customers_data = {name: cust_id for cust_id, name in customers}
        self.view.customer_combobox.configure(values=list(self.customers_data.keys()))
        products = self.model.get_products_by_distributor(self.distributor_id)
        self.products_data = {name: {'id': prod_id, 'price': price, 'stock': stock} for prod_id, name, price, stock in products}
        self.view.product_combobox.configure(values=list(self.products_data.keys()))
        self.clear_form()
    def _bind_events(self):
        self.view.product_combobox.configure(command=self._on_product_select)
        self.view.add_item_button.configure(command=self._add_item_to_list)
        self.view.remove_item_button.configure(command=self._remove_selected_item)
        self.view.save_button.configure(command=self._save_bill)
        self.view.clear_button.configure(command=self.clear_form)
    def _lock_header_widgets(self):
        self.view.customer_combobox.configure(state='disabled'); self.view.day_menu.configure(state='disabled'); self.view.month_menu.configure(state='disabled'); self.view.year_menu.configure(state='disabled'); self.view.paid_switch.configure(state='disabled')
    def _unlock_header_widgets(self):
        self.view.customer_combobox.configure(state='readonly'); self.view.day_menu.configure(state='normal'); self.view.month_menu.configure(state='normal'); self.view.year_menu.configure(state='normal'); self.view.paid_switch.configure(state='normal')
    def _on_product_select(self, product_name):
        product_info = self.products_data.get(product_name)
        self.view.price_entry.delete(0, END)
        if product_info and product_info['price'] > 0: self.view.price_entry.insert(0, f"{product_info['price']:.2f}")
        else: self.view.price_entry.configure(placeholder_text="أدخل سعر البيع")
    # ...

    def _add_item_to_list(self):
        p_name = self.view.product_combobox.get()
        product_info = self.products_data.get(p_name)
        # <<< MODIFICATION: Use self.view.show_error
        if not product_info:
            return self.view.show_error("خطأ", "الرجاء اختيار صنف.")
        
        q_str, p_str, d_str = self.view.quantity_entry.get(), self.view.price_entry.get(), self.view.discount_entry.get() or "0"
        
        try:
            quantity, price, discount = int(q_str), float(p_str), float(d_str)
            if quantity <= 0 or price <= 0 or discount < 0: raise ValueError
            if price <= discount:
                return self.view.show_error("خطأ", "الخصم لا يمكن أن يكون أكبر من أو يساوي السعر.")
            if quantity > product_info['stock']:
                return self.view.show_warning("تنبيه", f"الكمية المطلوبة ({quantity}) أكبر من المتاح بالمخزن ({product_info['stock']}).")
        except ValueError:
            return self.view.show_error("خطأ", "الكمية والسعر والخصم يجب أن تكون أرقامًا صحيحة.")

        p_id = product_info['id']
        if any(item['product_id'] == p_id for item in self.bill_items):
            return self.view.show_warning("تنبيه", "هذا الصنف موجود بالفعل في الفاتورة.")
        
        if not self.bill_items: self._lock_header_widgets()

        self.bill_items.append({'product_id': p_id, 'product_name': p_name, 'quantity': quantity, 'price': price, 'discount': discount, 'total': (price - discount) * quantity, 'initial_price': product_info['price']})
        self._update_treeview()
        self._clear_item_inputs()

    def _remove_selected_item(self):
        sel = self.view.tree.focus()
        # <<< MODIFICATION: Use self.view.show_error
        if not sel:
            return self.view.show_error("خطأ", "الرجاء تحديد صنف لحذفه.")
        p_name = self.view.tree.item(sel)['values'][4]
        self.bill_items = [i for i in self.bill_items if i['product_name'] != p_name]
        self._update_treeview()
        if not self.bill_items: self._unlock_header_widgets()

    def _save_bill(self):
        customer_name = self.view.customer_combobox.get()
        if not customer_name or not self.bill_items:
            # <<< MODIFICATION: Use self.view.show_error
            return self.view.show_error("خطأ", "الرجاء اختيار عميل وإضافة أصناف للفاتورة.")

        try:
            bill_date = datetime(int(self.view.year_menu.get()), int(self.view.month_menu.get()), int(self.view.day_menu.get())).strftime('%Y-%m-%d')
        except ValueError:
            return self.view.show_error("خطأ", "التاريخ المحدد غير صحيح.")
        
        data_to_save = {'customer_id': self.customers_data[customer_name], 'distributor_id': self.distributor_id, 'date': bill_date, 'is_paid': self.view.paid_switch.get(), 'items_list': self.bill_items, 'total_amount': sum(item['total'] for item in self.bill_items)}
        
        success, result = self.model.add_sales_transaction(data_to_save)
        if success:
            # <<< MODIFICATION: Use self.view.show_info
            self.view.show_info("نجاح", "تم حفظ الفاتورة بنجاح.")
            # <<< MODIFICATION: Use self.view.ask_yes_no for the print dialog
            if self.view.ask_yes_no("طباعة", "هل تريد طباعة الفاتورة؟"):
                # You would call the report generator here
                print("Printing bill with data:", result)
            self.clear_form()
        else:
            self.view.show_error("فشل الحفظ", result)

    # ... (_update_treeview, _clear_item_inputs, clear_form methods remain the same) ...
    def _update_treeview(self):
        self.view.tree.delete(*self.view.tree.get_children())
        total = sum(item['total'] for item in self.bill_items)
        for item in self.bill_items: self.view.tree.insert("", END, values=(f"{item['total']:.2f}", f"{item['discount']:.2f}", f"{item['price']:.2f}", item['quantity'], item['product_name']))
        self.view.total_value_label.configure(text=f"إجمالي الفاتورة: {total:.2f} ج.م")
    def _clear_item_inputs(self):
        self.view.product_combobox.set(""); self.view.quantity_entry.delete(0, END); self.view.price_entry.delete(0, END); self.view.discount_entry.delete(0, END)
    def clear_form(self):
        self._unlock_header_widgets(); self.view.customer_combobox.set(""); self.view.paid_switch.deselect()
        today = date.today()
        self.view.day_menu.set(str(today.day)); self.view.month_menu.set(str(today.month)); self.view.year_menu.set(str(today.year))
        self.bill_items = []; self._update_treeview(); self._clear_item_inputs()