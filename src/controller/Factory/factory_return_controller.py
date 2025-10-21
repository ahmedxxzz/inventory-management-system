from tkinter import messagebox, END
from datetime import date, datetime
from view.Factory.factory_return_view import FactoryReturnView
from model.Factory.factory_return_model import FactoryReturnModel

class FactoryReturnController:
    def __init__(self, root, db_conn):
        self.root = root
        self.model = FactoryReturnModel(db_conn)
        self.view = FactoryReturnView(self.root)
        self.factories_data = {}
        self.return_items = []
        self._load_initial_data()
        self._bind_events()

    def _load_initial_data(self):
        factories = self.model.get_all_factories()
        self.factories_data = {name: fac_id for fac_id, name, _ in factories}
        self.view.factory_combobox.configure(values=list(self.factories_data.keys()))
        self.clear_form()

    def _bind_events(self):
        self.view.factory_combobox.configure(command=self._on_factory_select)
        # <<< MODIFICATION: Bind Entry widgets to Enter key >>>
        self.view.product_entry.bind("<Return>", self._handle_product_enter)
        self.view.quantity_entry.bind("<Return>", lambda event: self.view.price_entry.focus())
        self.view.price_entry.bind("<Return>", lambda event: self._add_item_to_list())
        
        # Button commands remain the same
        self.view.add_item_button.configure(command=self._add_item_to_list)
        self.view.remove_item_button.configure(command=self._remove_selected_item)
        self.view.save_button.configure(command=self._save_return)
        self.view.clear_button.configure(command=self.clear_form)

    def _lock_header_widgets(self):
        self.view.factory_combobox.configure(state='disabled')
        self.view.day_menu.configure(state='disabled'); self.view.month_menu.configure(state='disabled'); self.view.year_menu.configure(state='disabled')

    def _unlock_header_widgets(self):
        self.view.factory_combobox.configure(state='readonly')
        self.view.day_menu.configure(state='normal'); self.view.month_menu.configure(state='normal'); self.view.year_menu.configure(state='normal')

    def _on_factory_select(self, name):
        # When factory changes, clear everything
        self.return_items = []
        self._update_treeview()
        self._clear_item_inputs()

    # <<< NEW: Function to handle Enter key on product entry >>>
    def _handle_product_enter(self, event=None):
        factory_name = self.view.factory_combobox.get()
        product_name = self.view.product_entry.get().strip()
        if not factory_name or not product_name: return

        factory_id = self.factories_data.get(factory_name)
        product_id = self.model.get_purchased_product_by_name(product_name, factory_id)
        
        if product_id:
            price = self.model.get_last_purchase_price(factory_id, product_id)
            self.view.price_entry.delete(0, END)
            self.view.price_entry.insert(0, f"{price:.2f}")
            self.view.quantity_entry.focus()
        else:
            messagebox.showerror("خطأ", f"الصنف '{product_name}' غير موجود أو لم يتم شراؤه من هذا المصنع من قبل.")

    def _add_item_to_list(self):
        factory_name = self.view.factory_combobox.get()
        p_name = self.view.product_entry.get().strip()
        q_str, p_str = self.view.quantity_entry.get(), self.view.price_entry.get()

        if not factory_name: return messagebox.showerror("خطأ", "الرجاء اختيار مصنع أولاً.")
        if not p_name: return messagebox.showerror("خطأ", "الرجاء إدخال اسم الصنف.")

        # --- VALIDATION ---
        factory_id = self.factories_data.get(factory_name)
        product_id = self.model.get_purchased_product_by_name(p_name, factory_id)
        if not product_id:
            return messagebox.showerror("خطأ", f"الصنف '{p_name}' غير موجود أو لم يتم شراؤه من هذا المصنع من قبل.")
        
        try:
            quantity, price = int(q_str), float(p_str)
            if quantity <= 0 or price < 0: raise ValueError
        except (ValueError, TypeError): return messagebox.showerror("خطأ", "الكمية والسعر يجب أن يكونا أرقامًا موجبة.")

        if any(item['product_id'] == product_id for item in self.return_items):
            return messagebox.showwarning("تنبيه", "هذا الصنف موجود بالفعل في قائمة المرتجع.")
        
        if not self.return_items: self._lock_header_widgets()

        self.return_items.append({
            'product_id': product_id, 'product_name': p_name, 'quantity': quantity,
            'price_at_return': price, 'total': quantity * price
        })
        self._update_treeview()
        self._clear_item_inputs()
        self.view.product_entry.focus()

    def _update_treeview(self):
        self.view.tree.delete(*self.view.tree.get_children())
        total_value = sum(item['total'] for item in self.return_items)
        index = 1
        for item in self.return_items:
            self.view.tree.insert("", END, values=(
                f"{item['total']:.2f}", f"{item['price_at_return']:.2f}",
                item['quantity'], item['product_name'], f"{index}"
            ))
            index += 1
        self.view.total_value_label.configure(text=f"إجمالي قيمة المرتجع: {total_value:.2f} ج.م")

    def _remove_selected_item(self):
        selected_item_id = self.view.tree.focus()
        if not selected_item_id: return messagebox.showerror("خطأ", "الرجاء تحديد صنف لحذفه.")
        
        # This logic is more robust than relying on name alone if names could duplicate
        selected_index = self.view.tree.index(selected_item_id)
        self.return_items.pop(selected_index)
        
        self._update_treeview()
        
        if not self.return_items:
            self._unlock_header_widgets()

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
        # <<< MODIFICATION: Clear product Entry instead of ComboBox >>>
        self.view.product_entry.delete(0, END)
        self.view.quantity_entry.delete(0, END)
        self.view.price_entry.delete(0, END)

    def clear_form(self):
        self._unlock_header_widgets()
        
        self.view.factory_combobox.set("")
        self.view.reason_entry.delete(0, END)
        
        today = date.today()
        self.view.day_menu.set(str(today.day))
        self.view.month_menu.set(str(today.month))
        self.view.year_menu.set(str(today.year))
        
        self.return_items = []
        self._update_treeview()
        self._clear_item_inputs()
        self.view.product_entry.focus()