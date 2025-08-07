from view.Factory_compnents_view.buy_view import BuyView
from model.Factory_compnents_model.buy_model import BuyModel
# from controller.Factory_compnents_controller.account_report_controller import AccountReportController
from datetime import datetime

class BuyController:
    def __init__(self, root):
        self.root = root
        self.view = BuyView(self.root)
        self.model = BuyModel()
        self.recommendation_type = ''
        
        self._bind_events()
        self.view.populate_treeview(self.model.get_buys_from_db())

    def view_destroy(self, event=None):
        self.model.conn.close()

    def _bind_events(self):
        self.view.bind('<Destroy>', self.view_destroy)

        for ent in [self.view.Entries[0], self.view.Entries[1]]:
            ent.bind('<FocusIn>', lambda event,var = ent.cget("textvariable"), ent = ent: self.recommendation_focusIn(ent, var))
            ent.bind('<KeyRelease>', lambda event,var = ent.cget("textvariable"), ent = ent, recommendation_type = self.recommendation_type: self.recommendation_KeyRelease(ent, var, recommendation_type))
            ent.bind('<FocusOut>', lambda event,var = ent.cget("textvariable"), ent = ent: self.recommendation_focusOut())
    
        self.view.save_buys_button.configure(command=self.save_buys)
        self.view.cache_buy_button.configure(command=self.cache_buy)
    
    
    


    def save_buys(self):
        if  not self.view.temp_operations:
            self.view.message("عملية فاشلة", "لا توجد عمليات لحفظها")
            return
        
        
        if self.model.insert_buys_to_db(self.view.temp_operations):

            for btn in self.view.temp_operations_buttons:
                btn.destroy()
                btn = None
            self.view.temp_operations_buttons = []
            self.view.temp_operations = []
            self.view.temp_operations_frame.configure(border_width=0, fg_color='transparent',scrollbar_button_color='#333333', scrollbar_button_hover_color='#333333', scrollbar_fg_color='#333333')
            self.view.populate_treeview(self.model.get_buys_from_db())
            
            self.view.message("عملية ناجحة", "تم حفظ الفاتورة بنجاح")
            # if self.view.message('طباعة','هل تريد طباعة الفاتورة','yes_no'):
            #     ReportController(self.view.temp_operations)
        else:
            self.view.message("عملية فاشلة", "لم يتم حفظ الفاتورة")


    def cache_buy(self):
        if self.view.check_inputs_before_caching(factory_names = self.model.get_factory_names_and_money(),products_codes = self.model.get_products_codes()): # validation input 
            current_time = datetime.now().strftime("%H:%M:%S")
            data = {
                        'facname': self.view.fac_name.get(),
                        'productcode': self.view.product_code.get(),
                        'price': self.view.price.get(),
                        'quantity': self.view.quantity.get(),
                        'discount': self.view.discount.get(),
                        'supplier': self.model.get_supplier_from_procode(self.view.product_code.get().strip()),
                        'paid': self.view.checkbox_var.get(),
                        'date': f"{self.view.year_var.get()}-{self.view.month_var.get().zfill(2)}-{self.view.day_var.get().zfill(2)} {current_time}"
                    }
            self.view.temp_operations.append(data)
            
            self.view.temp_operations_frame.configure(border_width=5, fg_color= 'gray20', border_color='#21130d', scrollbar_button_color='#696969', scrollbar_button_hover_color='red', scrollbar_fg_color='#333333')
            button = self.view.add_temp_operation_button()
            button.configure(command=lambda btn=button, data=data: self.cached_button_click(btn, data))
            
            for ent in [self.view.fac_name, self.view.product_code, self.view.price, self.view.quantity, self.view.discount, self.view.checkbox_var]:
                if ent == self.view.checkbox_var:
                    ent.set('0')
                    continue
                ent.set('')


    def cached_button_click(self, btn, data ):
        self.view.fac_name.set(data['facname'])
        self.view.product_code.set(data['productcode'])
        self.view.price.set(data['price'])
        self.view.quantity.set(data['quantity'])
        self.view.discount.set(data['discount'])
        self.view.checkbox_var.set(data['paid'])
        self.view.temp_operations_buttons.remove(btn)
        self.view.temp_operations.remove(data)
        btn.destroy()
        btn = None
        if len(self.view.temp_operations_buttons) == 0:
            self.view.temp_operations_frame.configure(border_width=0, fg_color='transparent',scrollbar_button_color='#333333', scrollbar_button_hover_color='#333333', scrollbar_fg_color='#333333')



    def recommendation_focusIn(self, ent, var):
        self.clear_recommendation_frames()
        self.view.recommended_frame.configure(border_width=5, fg_color= 'gray20', border_color='#21130d', scrollbar_button_color='#696969', scrollbar_button_hover_color='red', scrollbar_fg_color='#333333')
        
        self.recommendation_type = ''
        if ent == self.view.Entries[0]:
            # [("جلوبال تك للتصنيع",500), ("حلول الروبوتات الدقيقة",4000)]
            self.view.recommendations = self.model.get_factory_names_and_money()
            self.recommendation_type = 'fac_names with money'
            
        elif ent == self.view.Entries[1]:# products id
            # [1001, 1002, 1003,]
            self.view.recommendations = self.model.get_products_codes()

                
            self.recommendation_type = 'product codes'
        
        
        if var.get()=='':
            if self.view.recommendations :
                self.view.recommendation_focusIn(var, self.recommendation_type)
        
        else: 
            self.recommendation_KeyRelease(ent, var,self.recommendation_type)


    def recommendation_KeyRelease(self, ent, var, recommendation_type):
        var_text = var.get().strip() 
        if  var_text !='':
            self.clear_recommendation_frames()
            
            matching_items =[]
            for fac, money in self.view.recommendations:
                if var_text in str(fac):
                    matching_items.append((str(fac), money))
            
            if matching_items :
                self.view.recommendation_KeyRelease(var, matching_items, self.recommendation_type)

        else:
            self.recommendation_focusIn(ent, var)


    def recommendation_focusOut(self):
        self.clear_recommendation_frames()
        self.view.recommendations = []
            ## hide the recommendation frame
        self.view.recommended_frame.configure(border_width=0,  fg_color='transparent',scrollbar_button_color='#2b2b2b', scrollbar_button_hover_color='#2b2b2b', scrollbar_fg_color='#2b2b2b')


    def clear_recommendation_frames(self):
        for frame in self.view.recommendation_frames:
            frame.destroy()

        self.view.recommendation_frames = []
        self.view.recommended_frame._scrollbar.set(0.0, 0.0)
        self.view.recommended_frame._parent_canvas.yview_moveto(0.0)
