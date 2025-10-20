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
        self.products_data = {}
        self.bill_items = []

        self._load_initial_data()
        self._bind_events()

    def _load_initial_data(self):
        customers = self.model.get_customers_by_distributor(self.distributor_id)
        if customers:
            self.customers_data = {name: cust_id for cust_id, name in customers}
            self.view.customer_combobox.configure(values=list(self.customers_data.keys()))
        
        products = self.model.get_products_by_distributor(self.distributor_id)
        if products:
            self.products_data = {name: {'id': prod_id, 'price': price, 'stock': stock} for prod_id, name, price, stock in products}
            self.view.product_combobox.configure(values=list(self.products_data.keys()))
        
        self.clear_form()
        
    def _bind_events(self):
        self.view.product_combobox.configure(command=self._on_product_select)
        self.view.add_item_button.configure(command=self._add_item_to_list)
        self.view.remove_item_button.configure(command=self._remove_selected_item)
        self.view.save_button.configure(command=self._save_bill)
        self.view.clear_button.configure(command=self.clear_form)
        self.view.discount_value_entry.bind("<KeyRelease>", lambda e: self._update_treeview())
        self.view.discount_percentage_entry.bind("<KeyRelease>", lambda e: self._update_treeview())

    def _lock_header_widgets(self):
        self.view.customer_combobox.configure(state='disabled')
        self.view.day_menu.configure(state='disabled'); self.view.month_menu.configure(state='disabled'); self.view.year_menu.configure(state='disabled')
        self.view.paid_switch.configure(state='disabled')
        
    def _unlock_header_widgets(self):
        self.view.customer_combobox.configure(state='readonly')
        self.view.day_menu.configure(state='normal'); self.view.month_menu.configure(state='normal'); self.view.year_menu.configure(state='normal')
        self.view.paid_switch.configure(state='normal')

    def _on_product_select(self, product_name):
        product_info = self.products_data.get(product_name)
        self.view.price_entry.delete(0, END)
        if product_info and product_info['price'] > 0: 
            self.view.price_entry.insert(0, f"{product_info['price']:.2f}")
        else: 
            self.view.price_entry.configure(placeholder_text="أدخل سعر البيع")

    def _add_item_to_list(self):
        if not self.view.customer_combobox.get():
            return self.view.show_error("خطأ", "الرجاء اختيار العميل (المكتب) أولاً.")

        # --- REQUIREMENT 1 & 2: Discount confirmation on first item ---
        is_first_item = not self.bill_items
        if is_first_item:
            discount_value = self.view.discount_value_entry.get()
            discount_percentage = self.view.discount_percentage_entry.get()
            if not discount_value and not discount_percentage:
                if not self.view.ask_yes_no("تأكيد", "لم تقم بإدخال أي خصم. هل تريد المتابعة بدون خصم؟"):
                    return # Stop if user says "No"
            self.view.lock_discount_widgets() # Lock discounts after the decision

        p_name = self.view.product_combobox.get()
        product_info = self.products_data.get(p_name)
        if not product_info:
            return self.view.show_error("خطأ", "الرجاء اختيار صنف صحيح.")
        
        try:
            quantity = int(self.view.quantity_entry.get())
            price = float(self.view.price_entry.get())
            if quantity <= 0 or price <= 0: raise ValueError
            if quantity > product_info['stock']:
                return self.view.show_warning("تنبيه", f"الكمية المطلوبة ({quantity}) أكبر من المتاح بالمخزن ({product_info['stock']}).")
        except (ValueError, TypeError):
            return self.view.show_error("خطأ", "الكمية والسعر يجب أن تكون أرقامًا صحيحة وموجبة.")

        p_id = product_info['id']
        if any(item['product_id'] == p_id for item in self.bill_items):
            return self.view.show_warning("تنبيه", "هذا الصنف موجود بالفعل في الفاتورة.")
        
        if is_first_item: self._lock_header_widgets()
        
        item_data = {
            'iid': str(uuid.uuid4()), 'product_id': p_id, 'product_name': p_name, 
            'quantity': quantity, 'price': price, 'initial_price': product_info['price']
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

        # --- REQUIREMENT 2: Validate that only one discount type is used ---
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
        
        items_for_db = []
        items_for_report = []
        gross_total = 0
        total_discount_amount = 0

        for item in self.bill_items:
            # Step 1: Calculate the effective total discount per single piece
            price_after_value_discount = item['price'] - discount_value
            percentage_discount_amount = price_after_value_discount * (discount_percentage / 100)
            
            # This is the final, actual discount amount for one piece
            total_discount_per_piece = discount_value + percentage_discount_amount
            
            # Step 2: Prepare the item dictionary for the database
            # This now saves the CORRECT calculated discount per piece
            items_for_db.append({
                'product_id': item['product_id'],
                'quantity': item['quantity'],
                'price': item['price'],
                'discount': total_discount_per_piece, # This is the crucial change
                'initial_price': item['initial_price']
            })
            
            # Step 3: Prepare the item dictionary for the report
            report_item = item.copy()
            report_item['discount'] = total_discount_per_piece
            items_for_report.append(report_item)

            # Step 4: Calculate overall totals for the bill
            gross_total += item['price'] * item['quantity']
            total_discount_amount += total_discount_per_piece * item['quantity']

        net_total = gross_total - total_discount_amount
        data_to_save = {
            'customer_id': self.customers_data[customer_name], 'distributor_id': self.distributor_id, 
            'date': bill_date, 'is_paid': self.view.paid_switch.get(), 
            'items_list': items_for_db, 'total_amount': net_total
        }
        
        success, result = self.model.add_sales_transaction(data_to_save)
        if success:
            self.view.show_info("نجاح", "تم حفظ الفاتورة بنجاح.")
            if self.view.ask_yes_no("طباعة", "هل تريد طباعة الفاتورة؟"):
                report_data = {
                    'sales_bill_id': result['sales_bill_id'], 'customer_name': customer_name,
                    'distributor_name': self.distributor_name, 'date': bill_date,
                    'items': items_for_report, # Pass the list with calculated discounts
                    'is_paid': data_to_save['is_paid'], 'balance_before': result['balance_before'],
                    'balance_after': result['balance_after'],
                    'logo_path': self.model.get_distributor_logo_by_name(self.distributor_name)
                }
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

        gross_total = 0
        total_discount_amount = 0
        
        for i, item in enumerate(self.bill_items, 1):
            price_after_value_discount = item['price'] - discount_value
            percentage_discount_for_item = price_after_value_discount * (discount_percentage / 100)
            final_price_per_item = price_after_value_discount - percentage_discount_for_item
            
            item_total = final_price_per_item * item['quantity']
            
            gross_total += item['price'] * item['quantity']
            total_discount_amount += (item['price'] - final_price_per_item) * item['quantity']
            
            # --- REQUIREMENT 3: Reordered values to match the view ---
            self.view.tree.insert(
                "", END, iid=item['iid'],
                values=(f"{item_total:.2f}", f"{item['price']:.2f}", item['quantity'], item['product_name'], i)
            )

        net_total = gross_total - total_discount_amount
        
        total_text = (
            f"الإجمالي قبل الخصم: {gross_total:.2f} | "
            f"مجموع الخصم: {total_discount_amount:.2f} | "
            f"صافي الفاتورة: {net_total:.2f} ج.م"
        )
        self.view.total_value_label.configure(text=total_text)

    def _clear_item_inputs(self):
        self.view.product_combobox.set("")
        self.view.quantity_entry.delete(0, END)
        self.view.price_entry.delete(0, END)
        
    def clear_form(self):
        self._unlock_header_widgets()
        self.view.unlock_discount_widgets() # Also unlock discount fields
        self.view.customer_combobox.set("")
        self.view.paid_switch.deselect()
        today = date.today()
        self.view.day_menu.set(f"{today.day:02d}")
        self.view.month_menu.set(f"{today.month:02d}")
        self.view.year_menu.set(str(today.year))
        
        self.view.discount_value_entry.delete(0, END)
        self.view.discount_percentage_entry.delete(0, END)

        self.bill_items = []
        self._update_treeview()
        self._clear_item_inputs()