from model.Factory.factory_buy_model import FactoryBuyModel
from view.Factory.factory_buy_view import FactoryBuyView
from controller.Factory.factory_buy_report_controller import BuyReportController 
from datetime import datetime
import uuid


class FactoryBuyController:
    def __init__(self, frame, db_conn):
        self.frame = frame
        self.db_conn = db_conn
        
        self.model = FactoryBuyModel(self.db_conn)
        self.view = FactoryBuyView(self.frame)
        self.view.pack(expand=True, fill="both")

        self.current_bill_items = []
        self.total_amount = 0.0
        self.selected_item_id = None
        
        self._bind_events()
        self._load_initial_data()

    def _load_initial_data(self):
        factories = self.model.get_all_factories()
        distributors = self.model.get_all_distributors()
        self.view.populate_combobox(self.view.factory_combobox, factories)
        self.view.populate_combobox(self.view.distributor_combobox, distributors)
        self.view.distributor_combobox.set("")

    def _bind_events(self):
        # Button commands
        self.view.add_item_button.configure(command=self._on_add_item)
        self.view.update_item_button.configure(command=self._on_update_item)
        self.view.delete_item_button.configure(command=self._on_delete_item)
        self.view.clear_selection_button.configure(command=self._on_clear_selection)
        self.view.save_bill_button.configure(command=self._on_save_bill)
        self.view.cancel_bill_button.configure(command=self._on_cancel_bill)
        
        # Widget events
        self.view.product_name_entry.bind("<FocusOut>", self._check_product_status)
        self.view.bill_items_table.bind("<<TreeviewSelect>>", self._on_table_row_select)

        # <<< --- NEW: Add Enter key bindings for navigation --- >>>
        self.view.product_name_entry.bind("<Return>", self._handle_product_enter)
        self.view.quantity_entry.bind("<Return>", lambda event: self.view.price_entry.focus())
        self.view.price_entry.bind("<Return>", lambda event: self.view.discount_entry.focus())
        self.view.discount_entry.bind("<Return>", lambda event: self._on_add_item())

    # <<< --- NEW: Helper function to handle Enter key on product entry --- >>>
    def _handle_product_enter(self, event=None):
        """Checks product status and moves focus to the quantity field."""
        self._check_product_status()
        self.view.quantity_entry.focus()
        return "break" # Prevents the default Enter key behavior

    def _on_cancel_bill(self):
        if not self.current_bill_items:
            self.view.clear_bill_form()
            return
        if self.view.ask_yes_no("تأكيد الإلغاء", "هل أنت متأكد من رغبتك في إلغاء الفاتورة الحالية؟ سيتم فقدان كل البيانات المدخلة."):
            self.current_bill_items = []
            self.total_amount = 0.0
            self.view.clear_bill_form()
    
    def _on_table_row_select(self, event=None):
        selected_id = self.view.get_selected_item_id()
        if not selected_id: return
        self.selected_item_id = selected_id
        item_data = next((item for item in self.current_bill_items if item['id'] == self.selected_item_id), None)
        if item_data:
            self.view.populate_item_inputs(item_data)
            self.view.show_edit_mode_buttons()

    def _on_clear_selection(self):
        self.selected_item_id = None
        self.view.bill_items_table.selection_remove(self.view.bill_items_table.selection())
        self.view.clear_item_inputs()
        self.view.show_add_mode_buttons()

    def _check_product_status(self, event=None):
        product_name = self.view.product_name_entry.get().strip()
        factory_name = self.view.factory_combobox.get()
        if not product_name or not factory_name: return
        product_details = self.model.get_product_details_for_purchase(product_name, factory_name)
        if product_details is None:
            self.view.distributor_combobox.configure(state="normal")
            self.view.set_distributor("")
            self.view.set_price(None)
            self.view.show_info("منتج جديد", f"المنتج '{product_name}' غير مسجل. يرجى اختيار الموزع التابع له.")
        else:
            self.view.set_distributor(product_details['distributor_name'])
            last_price = product_details.get('last_price')
            self.view.set_price(last_price)
                
    def _validate_item_inputs(self):
        item_data = self.view.get_item_data()
        if not all([item_data["product_name"], item_data["quantity"], item_data["price"]]):
            self.view.show_error("خطأ في الإدخال", "يرجى ملء حقول اسم المنتج، الكمية، والسعر.")
            return None
        try:
            quantity = int(item_data["quantity"])
            price = float(item_data["price"])
            discount = float(item_data["discount"])
            if quantity <= 0 or price <= 0 or discount < 0: raise ValueError()
        except ValueError:
            self.view.show_error("خطأ في الإدخال", "الكمية والسعر والخصم يجب أن تكون أرقامًا موجبة.")
            return None
        if self.model.is_new_product(item_data["product_name"]) and not item_data["distributor"]:
            self.view.show_error("بيانات ناقصة", "يجب اختيار موزع للمنتج الجديد.")
            return None
        item_data['quantity'] = quantity
        item_data['price'] = price
        item_data['discount'] = discount
        return item_data

    def _on_add_item(self):
        validated_data = self._validate_item_inputs()
        if not validated_data: return
        if not self.current_bill_items:
            self.view.set_header_fields_state("disabled")
        total_item_price = (validated_data['price'] - validated_data['discount']) * validated_data['quantity']
        item_to_add = {
            "id": str(uuid.uuid4()), "product_name": validated_data["product_name"],
            "quantity": validated_data['quantity'], "price": validated_data['price'],
            "discount": validated_data['discount'], "distributor_name": validated_data["distributor"],
            "total": total_item_price
        }
        self.current_bill_items.append(item_to_add)
        self.total_amount += total_item_price
        self.view.add_item_to_table(item_to_add)
        self.view.update_total_display(self.total_amount)
        self.view.clear_item_inputs()

    def _on_update_item(self):
        if not self.selected_item_id: return
        validated_data = self._validate_item_inputs()
        if not validated_data: return
        old_item = next((item for item in self.current_bill_items if item['id'] == self.selected_item_id), None)
        if old_item:
            self.total_amount -= old_item['total']
            self.current_bill_items.remove(old_item)
        total_item_price = (validated_data['price'] - validated_data['discount']) * validated_data['quantity']
        updated_item = {
            "id": self.selected_item_id, "product_name": validated_data["product_name"],
            "quantity": validated_data['quantity'], "price": validated_data['price'],
            "discount": validated_data['discount'], "distributor_name": validated_data["distributor"],
            "total": total_item_price
        }
        self.current_bill_items.append(updated_item)
        self.total_amount += updated_item['total']
        self.view.update_table_row(self.selected_item_id, updated_item)
        self.view.update_total_display(self.total_amount)
        self._on_clear_selection()

    def _on_delete_item(self):
        if not self.selected_item_id: return
        item_to_delete = next((item for item in self.current_bill_items if item['id'] == self.selected_item_id), None)
        if item_to_delete:
            self.total_amount -= item_to_delete['total']
            self.current_bill_items.remove(item_to_delete)
            self.view.delete_table_row(self.selected_item_id)
            self.view.update_total_display(self.total_amount)
            self._on_clear_selection()

    def _on_save_bill(self):
        if not self.current_bill_items:
            self.view.show_error("فاتورة فارغة", "يجب إضافة صنف واحد على الأقل قبل حفظ الفاتورة.")
            return
            
        header_data = self.view.get_bill_header_data()
        
        for item in self.current_bill_items:
            details = self.model.get_product_details_for_purchase(item['product_name'], header_data['factory_name'])
            last_price = details.get('last_price') if details else None
            current_price = item['price']
            if last_price is not None and abs(last_price - current_price) > 0.001:
                msg = (f"سعر منتج '{item['product_name']}' قد تغير.\n"
                       f"آخر سعر شراء كان: {last_price:.2f}\n"
                       f"السعر الجديد هو: {current_price:.2f}\n\n"
                       "هل تريد المتابعة بالسعر الجديد؟")
                if not self.view.ask_yes_no("تأكيد تغيير السعر", msg):
                    self.view.show_info("عملية ملغاة", "تم إلغاء حفظ الفاتورة.")
                    return
            
        full_bill_data = {
            "factory_name": header_data["factory_name"], "date": header_data["date"],
            "total_amount": self.total_amount, "is_paid": header_data["is_paid"],
            "items": self.current_bill_items
        }
        
        try:
            save_result = self.model.save_purchase_bill(full_bill_data)
            self.view.show_info("نجاح", "تم حفظ الفاتورة بنجاح!")
            
            if self.view.ask_yes_no("طباعة الفاتورة", "هل تريد طباعة الفاتورة الآن؟"):
                full_bill_data['purchases_bill_id'] = save_result['id']
                full_bill_data['balance_before'] = save_result['balance_before']
                full_bill_data['balance_after'] = save_result['balance_after']
                
                report_generator = BuyReportController(full_bill_data)
                report_generator.generate_pdf()

            self.current_bill_items = []
            self.total_amount = 0.0
            self.view.clear_bill_form()

        except Exception as e:
            self.view.show_error("خطأ في الحفظ", f"حدث خطأ أثناء حفظ الفاتورة:\n{e}")