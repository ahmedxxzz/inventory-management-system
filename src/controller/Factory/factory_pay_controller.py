# controller/Factory/factory_pay_controller.py

from view.Factory.factory_pay_view import FactoryPayView
from model.Factory.factory_pay_model import FactoryPayModel
from tkinter import messagebox
from datetime import date, datetime

class FactoryPayController:
    # ... (init, _load_initial_data, _bind_events, _on_wallet_select remain unchanged) ...
    def __init__(self, root, db_conn):
        self.root = root
        self.model = FactoryPayModel(db_conn)
        self.view = FactoryPayView(self.root)
        self.factories_data = {}
        self.wallets_data = {}
        self._load_initial_data()
        self._bind_events()

    def _load_initial_data(self):
        factories = self.model.get_all_factories()
        factory_names = []
        if factories:
            for fac_id, name, balance in factories:
                self.factories_data[name] = {'id': fac_id, 'balance': balance}
                factory_names.append(name)
        self.view.factory_combobox.configure(values=factory_names)
        
        wallets = self.model.get_all_wallets()
        wallet_names = []
        if wallets:
            for wal_id, name, balance in wallets:
                self.wallets_data[name] = {'id': wal_id, 'balance': balance}
                wallet_names.append(name)
        self.view.wallet_combobox.configure(values=wallet_names)
        
        self.view.clear_form()

    def _bind_events(self):
        self.view.wallet_combobox.configure(command=self._on_wallet_select)
        self.view.save_button.configure(command=self._save_payment)
    
    def _on_wallet_select(self, selected_wallet_name):
        wallet_info = self.wallets_data.get(selected_wallet_name)
        if wallet_info:
            balance = wallet_info['balance']
            self.view.wallet_balance_label.configure(text=f"الرصيد المتاح: {balance:.2f} جنيه")
        else:
            self.view.wallet_balance_label.configure(text="الرصيد المتاح: 0.00")
            
    def _save_payment(self):
        # ... (Validation part remains unchanged) ...
        factory_name = self.view.factory_combobox.get()
        wallet_name = self.view.wallet_combobox.get()
        amount_str = self.view.amount_entry.get()
        day = self.view.day_menu.get()
        month = self.view.month_menu.get()
        year = self.view.year_menu.get()
        
        if not factory_name or not wallet_name or not amount_str:
            messagebox.showerror("خطأ في الإدخال", "الرجاء ملء جميع الحقول.")
            return

        try:
            payment_date_obj = datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d").date()
            payment_date_str = payment_date_obj.strftime('%Y-%m-%d')
            amount_paid = float(amount_str)
            if amount_paid <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("خطأ في الإدخال", "الرجاء التحقق من صحة التاريخ والمبلغ المدخل.")
            return

        factory_info = self.factories_data[factory_name]
        wallet_info = self.wallets_data[wallet_name]
        factory_id = factory_info['id']
        wallet_id = wallet_info['id']

        if amount_paid > factory_info['balance']:
             if not messagebox.askyesno("تأكيد", f"المبلغ المدفوع ({amount_paid}) أكبر من رصيد المصنع المستحق ({factory_info['balance']}).\nهل تريد المتابعة؟"):
                 return
        
        # Call Model to Save
        success, result = self.model.add_payment(factory_id, wallet_id, amount_paid, payment_date_str)
        
        # Handle Result
        if success:
            messagebox.showinfo("نجاح", "تم تسجيل الدفعة بنجاح.")
            
            if messagebox.askyesno("طباعة", "هل تريد طباعة إيصال الدفع؟"):
                # <<< --- START OF CHANGE --- >>>
                # The 'result' dictionary now contains 'pay_id' from the model
                payment_details_for_report = {
                    'pay_id': result['pay_id'], # Get the new ID from the result
                    'factory_name': factory_name,
                    'amount_paid': amount_paid,
                    'payment_date': payment_date_str,
                    'balance_before': result['balance_before'],
                    'balance_after': result['balance_after'],
                    'wallet_name': wallet_name
                }
                # <<< --- END OF CHANGE --- >>>
                self._generate_report(payment_details_for_report)
            
            self._load_initial_data()
        else:
            messagebox.showerror("فشل الحفظ", result)

    def _generate_report(self, data):
        """Calls the report controller to generate a PDF."""
        from controller.Factory.factory_pay_report_controller import FactoryPayReportController
        report_controller = FactoryPayReportController(data)