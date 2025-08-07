from view.Customer_compnents_view.pay_view import PayView
from model.Customer_compnents_model.pay_model import PayModel
# from controller.Customer_compnents_controller.account_report_controller import AccountReportController
from datetime import datetime


class PayController:
    def __init__(self, root, supplier):
        self.root = root
        self.supplier = supplier
        self.view = PayView(self.root)
        self.model = PayModel(self.supplier)
        self._bind_events()
        self.view.populate_treeview(self.model.get_pays_from_db())
        
    
    
    def _bind_events(self):
        self.view.cus_name_entry.bind('<FocusIn>', lambda event, ent = self.view.cus_name_entry: self.recommendation_focusIn(ent, ent.cget("textvariable")))
        self.view.cus_name_entry.bind('<KeyRelease>', lambda event, ent = self.view.cus_name_entry: self.recommendation_KeyRelease(ent,  ent.cget("textvariable")))
        self.view.cus_name_entry.bind('<FocusOut>', lambda event : self.recommendation_focusOut())
        
        self.view.option_menu.configure(values=self.model.get_safes())
        
        self.view.button.configure(command=self.save_pay)
        


    def save_pay(self):

        if self.check_inputs():
            current_time = datetime.now().strftime("%H:%M:%S")
            date = f"{self.view.year_var.get()}-{self.view.month_var.get().zfill(2)}-{self.view.day_var.get().zfill(2)} {current_time}"
            if self.model.save_pay_to_db(self.view.cus_name.get().strip(), float(self.view.money_amount.get()), self.view.safe_type.get().strip(), date):
                self.view.message('showinfo', 'عملية ناجحة', 'تمت عملية الدفع بنجاح')
                # if self.view.message('yes_no', 'فاتورة', 'هل تريد طباعة الفاتورة ؟'):
                #     AccountReportController([self.view.cus_name.get().strip(), float(self.view.money_amount.get()), self.view.safe_type.get().strip()], 'pay')
                self.view.clear_inputs()
                self.view.populate_treeview(self.model.get_pays_from_db())


    def check_inputs(self):
        if self.view.cus_name.get().strip() == '' or self.view.money_amount.get().strip() == '':
            self.view.message('showinfo', ' خطأ', 'يرجى عدم ترك الحقول فارغة')
            return False
        if self.view.safe_type.get().strip() == 'اختار نوع الخزنة':
            self.view.message('showinfo', ' خطاء', 'يرجى اختيار نوع الخزنة')
            return False
        
        if float(self.view.money_amount.get()) <= 0.0:
            self.view.message('showinfo', 'عملية فاشلة', 'مبلغ الدفع يجب ان يكون اكبر من 0')
            return False
        
        if not self.model.check_customer_name_exist(self.view.cus_name.get().strip()):
            self.view.message('showinfo', 'عملية فاشلة', 'اسم المصنع غير موجود')
            return False
        
        
        if self.model.check_customer_money(self.view.cus_name.get().strip()) < float(self.view.money_amount.get()):
            self.view.message('showinfo', 'عملية فاشلة', 'المبلغ المدفوع اكبر من المبلغ المستحق')
            return False
        
        if float(self.view.money_amount.get()) > float(self.model.check_safe_money(self.view.safe_type.get().strip())):
            self.view.message('showinfo', 'عملية فاشلة', 'المبلغ المدفوع اكبر من المبلغ الموجود في الخزنة')
            return False
        
        return True

    def recommendation_focusIn(self, ent, var):
        self.clear_recommendation_frames()
        self.view.recommended_frame.configure(border_width=5, fg_color= 'gray20', border_color='#21130d', scrollbar_button_color='#696969', scrollbar_button_hover_color='red', scrollbar_fg_color='#333333')
        
        self.view.recommendations = self.model.get_customer_names_and_money()
        '''return [('حماده طلبة', 50000.0),('عمرو هلال', 75000.0),('علاء احمد', 30000.0),]'''        
        
        if var.get()=='':
            if self.view.recommendations :
                ''' create a frame inside the recommendation frame and add a button inside it and label with the money'''
                self.view.recommendation_focusIn(var)
        
        else: 
            self.recommendation_KeyRelease(ent, var)


    def recommendation_KeyRelease(self, ent, var):
        var_text = var.get().strip() 
        if  var_text !='':
            self.clear_recommendation_frames()
            
            matching_items =[]
            for cus, money in self.view.recommendations:
                if var_text in str(cus):
                    matching_items.append((str(cus), money))
            
            if matching_items :
                self.view.recommendation_KeyRelease(var, matching_items)

        else:
            self.recommendation_focusIn(ent, var)


    def recommendation_focusOut(self):
        self.clear_recommendation_frames()
        self.view.recommendations = []
            ## hide the recommendation frame
        self.view.recommended_frame.configure(border_width=5,  fg_color='transparent', border_color='#333333',scrollbar_button_color='#333333', scrollbar_button_hover_color='#333333', scrollbar_fg_color='#333333')


    def clear_recommendation_frames(self):
        for btn in self.view.recommendation_frames:
            btn.destroy()

        self.view.recommendation_frames = []
        self.view.recommended_frame._scrollbar.set(0.0, 0.0)
        self.view.recommended_frame._parent_canvas.yview_moveto(0.0)

