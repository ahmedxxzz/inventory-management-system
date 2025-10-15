from datetime import date, datetime

from view.Customer.customer_pay_view import CustomerPayView, END
from model.Customer.customer_pay_model import CustomerPayModel

class CustomerPayController:
    def __init__(self, root, db_conn, distributor_name):
        self.root = root
        self.model = CustomerPayModel(db_conn)
        self.distributor_name = distributor_name
        self.distributor_id = self.model.get_distributor_id_by_name(distributor_name)
        self.view = CustomerPayView(self.root, distributor_name)

        self.customers_data = {}
        self.wallets_data = {}

        self._load_initial_data()
        self._bind_events()

    def _load_initial_data(self):
        customers = self.model.get_customers_by_distributor(self.distributor_id)
        self.customers_data = {name: {'id': cust_id, 'balance': balance} for cust_id, name, balance in customers}
        self.view.customer_combobox.configure(values=list(self.customers_data.keys()))
        
        wallets = self.model.get_all_wallets()
        self.wallets_data = {name: wal_id for wal_id, name, _ in wallets}
        self.view.wallet_combobox.configure(values=list(self.wallets_data.keys()))
        
        self.clear_form()

    def _bind_events(self):
        self.view.customer_combobox.configure(command=self._on_customer_select)
        self.view.save_button.configure(command=self._save_payment)
        self.view.clear_button.configure(command=self.clear_form)

    def _on_customer_select(self, selected_customer_name):
        """Updates the customer balance label when a customer is selected."""
        customer_info = self.customers_data.get(selected_customer_name)
        if customer_info:
            balance = customer_info.get('balance', 0.0)
            self.view.customer_balance_label.configure(text=f"الرصيد الحالي المستحق: {balance:,.2f} ج.م")
        else:
            self.view.customer_balance_label.configure(text="الرصيد الحالي: 0.00")

    def _save_payment(self):
        customer_name = self.view.customer_combobox.get()
        wallet_name = self.view.wallet_combobox.get()
        amount_str = self.view.amount_entry.get()

        if not customer_name or not wallet_name or not amount_str:
            return self.view.show_error("خطأ في الإدخال", "الرجاء ملء جميع الحقول.")

        try:
            payment_date = datetime(int(self.view.year_menu.get()), int(self.view.month_menu.get()), int(self.view.day_menu.get())).strftime('%Y-%m-%d')
            amount_paid = float(amount_str)
            if amount_paid <= 0: raise ValueError
        except ValueError:
            return self.view.show_error("خطأ في الإدخال", "الرجاء التحقق من صحة التاريخ والمبلغ المدخل.")

        customer_id = self.customers_data[customer_name]['id']
        wallet_id = self.wallets_data[wallet_name]

        success, result = self.model.add_payment(customer_id, self.distributor_id, wallet_id, amount_paid, payment_date)

        if success:
            self.view.show_info("نجاح", "تم تسجيل الدفعة بنجاح.")
            if self.view.ask_yes_no("طباعة", "هل تريد طباعة إيصال استلام نقدية؟"):
                from controller.Customer.customer_pay_report_controller import CustomerPayReportController
                report_data = {
                    'pay_id': result['pay_id'],
                    'customer_name': customer_name,
                    'distributor_name': self.distributor_name,
                    'date': payment_date,
                    'amount_paid': amount_paid,
                    'balance_before': result['balance_before'],
                    'balance_after': result['balance_after']
                }
                # 2. Generate the report
                try:
                    report_generator = CustomerPayReportController(report_data)
                    report_generator.generate_pdf()
                except Exception as e:
                    self.view.show_error("خطأ في الطباعة", f"فشل إنشاء التقرير:\n{e}")
            self._load_initial_data() # Refresh data
        else:
            self.view.show_error("فشل الحفظ", result)

    def clear_form(self):
        self.view.customer_combobox.set("")
        self.view.wallet_combobox.set("")
        self.view.amount_entry.delete(0, END)
        self.view.customer_balance_label.configure(text="الرصيد الحالي: 0.00")
        today = date.today()
        self.view.day_menu.set(str(today.day)); self.view.month_menu.set(str(today.month)); self.view.year_menu.set(str(today.year))

