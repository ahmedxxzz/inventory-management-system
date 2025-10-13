from tkinter import messagebox, END
from datetime import date, datetime
from view.Factory.factory_return_view import FactoryReturnView
from model.Factory.factory_return_model import FactoryReturnModel

class FactoryReturnController:
    def __init__(self, root, db_conn):
        self.root = root
        self.model = FactoryReturnModel(db_conn)
        self.view = FactoryReturnView(self.root)
        self.factories_data, self.products_data, self.return_items = {}, {}, []
        self._load_initial_data()
        self._bind_events()

    def _load_initial_data(self):
        factories = self.model.get_all_factories()
        self.factories_data = {name: fac_id for fac_id, name, _ in factories}
        self.view.factory_combobox.configure(values=list(self.factories_data.keys()))
        self.clear_form()

    def _bind_events(self):
        self.view.factory_combobox.configure(command=self._on_factory_select)
        self.view.product_combobox.configure(command=self._on_product_select)
        self.view.add_item_button.configure(command=self._add_item_to_list)
        self.view.remove_item_button.configure(command=self._remove_selected_item)
        self.view.save_button.configure(command=self._save_return)
        self.view.clear_button.configure(command=self.clear_form)

    # <<<--- REQUIREMENT #2: LOCK/UNLOCK WIDGETS --- START --->
    def _lock_header_widgets(self):
        """Disables the main details widgets so they can't be changed mid-bill."""
        self.view.factory_combobox.configure(state='disabled')
        self.view.day_menu.configure(state='disabled')
        self.view.month_menu.configure(state='disabled')
        self.view.year_menu.configure(state='disabled')

    def _unlock_header_widgets(self):
        """Enables the main details widgets for a new bill."""
        self.view.factory_combobox.configure(state='readonly')
        self.view.day_menu.configure(state='normal')
        self.view.month_menu.configure(state='normal')
        self.view.year_menu.configure(state='normal')
    # <<<--- REQUIREMENT #2: LOCK/UNLOCK WIDGETS --- END --->

    def _on_factory_select(self, name):
        self.return_items, self.products_data = [], {}
        self._update_treeview()
        self._clear_item_inputs()
        factory_id = self.factories_data.get(name)
        if factory_id:
            products = self.model.get_products_by_factory(factory_id)
            self.products_data = {p_name: p_id for p_id, p_name in products}
            self.view.product_combobox.configure(values=list(self.products_data.keys()))

    def _on_product_select(self, name):
        factory_id = self.factories_data.get(self.view.factory_combobox.get())
        product_id = self.products_data.get(name)
        if factory_id and product_id:
            price = self.model.get_last_purchase_price(factory_id, product_id)
            self.view.price_entry.delete(0, END)
            self.view.price_entry.insert(0, f"{price:.2f}")

    def _add_item_to_list(self):
        p_name = self.view.product_combobox.get()
        q_str = self.view.quantity_entry.get()
        p_str = self.view.price_entry.get()

        if not p_name: return messagebox.showerror("خطأ", "الرجاء اختيار صنف.")
        try:
            quantity, price = int(q_str), float(p_str)
            if quantity <= 0 or price < 0: raise ValueError
        except ValueError: return messagebox.showerror("خطأ", "الكمية والسعر يجب أن يكونا أرقامًا موجبة.")

        p_id = self.products_data[p_name]
        if any(item['product_id'] == p_id for item in self.return_items):
            return messagebox.showwarning("تنبيه", "هذا الصنف موجود بالفعل في قائمة المرتجع.")
        
        # <<<--- REQUIREMENT #2: LOCK WIDGETS ON FIRST ITEM ADD --- START --->
        if not self.return_items:
            self._lock_header_widgets()
        # <<<--- REQUIREMENT #2: LOCK WIDGETS ON FIRST ITEM ADD --- END --->

        self.return_items.append({
            'product_id': p_id, 'product_name': p_name, 'quantity': quantity,
            'price_at_return': price, 'total': quantity * price
        })
        self._update_treeview()
        self._clear_item_inputs()

    def _update_treeview(self):
        self.view.tree.delete(*self.view.tree.get_children())
        total_value = sum(item['total'] for item in self.return_items)
        for item in self.return_items:
            self.view.tree.insert("", END, values=(
                f"{item['total']:.2f}", f"{item['price_at_return']:.2f}",
                item['quantity'], item['product_name']
            ))
        self.view.total_value_label.configure(text=f"إجمالي قيمة المرتجع: {total_value:.2f} ج.م")

    def _remove_selected_item(self):
        selected_item = self.view.tree.focus()
        if not selected_item: return messagebox.showerror("خطأ", "الرجاء تحديد صنف لحذفه.")
        
        p_name_to_remove = self.view.tree.item(selected_item)['values'][3]
        self.return_items = [item for item in self.return_items if item['product_name'] != p_name_to_remove]
        self._update_treeview()
        # Note: We don't unlock here, only on full cancel.

    def _save_return(self):
        if not self.view.factory_combobox.get() or not self.return_items:
            return messagebox.showerror("خطأ", "الرجاء اختيار مصنع وإضافة أصناف للمرتجع.")
        
        try:
            r_date = datetime(int(self.view.year_menu.get()), int(self.view.month_menu.get()), int(self.view.day_menu.get())).strftime('%Y-%m-%d')
        except ValueError: return messagebox.showerror("خطأ", "التاريخ المحدد غير صحيح.")
        
        total_amount = sum(item['total'] for item in self.return_items)
        factory_id = self.factories_data[self.view.factory_combobox.get()]
        
        success, result = self.model.add_return_transaction(
            factory_id, r_date, self.view.reason_entry.get(), self.return_items, total_amount
        )
        if success:
            messagebox.showinfo("نجاح", "تم تسجيل المرتجع بنجاح.")
            if messagebox.askyesno("طباعة", "هل تريد طباعة إيصال المرتجع؟"):
                report_data = {
                    'return_id': result['return_id'],
                    'factory_name': self.view.factory_combobox.get(),
                    'date': r_date,
                    'items': self.return_items,
                    'balance_before': result['balance_before'],
                    'balance_after': result['balance_after']
                }
                from controller.Factory.factory_return_report_controller import FactoryReturnReportController
                report_generator = FactoryReturnReportController(report_data)
                report_generator.generate_pdf()
            self.clear_form()
        else:
            messagebox.showerror("فشل الحفظ", result)

    def _clear_item_inputs(self):
        self.view.product_combobox.set("")
        self.view.quantity_entry.delete(0, END)
        self.view.price_entry.delete(0, END)

    def clear_form(self):
        # <<<--- REQUIREMENT #2: UNLOCK WIDGETS ON CLEAR --- START --->
        self._unlock_header_widgets()
        # <<<--- REQUIREMENT #2: UNLOCK WIDGETS ON CLEAR --- END --->
        
        self.view.factory_combobox.set("")
        self.view.product_combobox.configure(values=[])
        self.view.reason_entry.delete(0, END)
        
        today = date.today()
        self.view.day_menu.set(str(today.day))
        self.view.month_menu.set(str(today.month))
        self.view.year_menu.set(str(today.year))
        
        self.return_items = []
        self._update_treeview()
        self._clear_item_inputs()