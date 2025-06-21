from view.Factory_compnents_view.buy_view import BuyView
from model.Factory_compnents_model.buy_model import BuyModel
from datetime import datetime

class BuyController:
    def __init__(self, root):
        self.root = root
        self.view = BuyView(self.root)
        self.model = BuyModel()
        self.recommendation_type = ''
        
        self._bind_events()
        self.view.populate_treeview(self.model.get_buys_from_db())
        


    def _bind_events(self):

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
            
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for opt in self.view.temp_operations:
            opt.insert(1, current_time)
            ## facname, current_time, productcode, price, quantity, discount, supplier
        
        if self.model.insert_buys_to_db(self.view.temp_operations):
        
            for btn in self.view.temp_operations_buttons:
                btn.destroy()
                btn = None
            self.view.temp_operations_buttons = []
            self.view.temp_operations = []
            self.view.temp_operations_frame.configure(border_width=0, fg_color='transparent',scrollbar_button_color='#333333', scrollbar_button_hover_color='#333333', scrollbar_fg_color='#333333')
            self.view.populate_treeview(self.model.get_buys_from_db())
            
            self.view.message("عملية ناجحة", "تم حفظ الفاتورة بنجاح")


    def cache_buy(self):
        if self.view.check_inputs_before_caching(): # validation input 
            data = [ # facname, productcode, price, quantity, discount, supplier 
                self.view.fac_name.get(), self.view.product_code.get(), self.view.price.get(), self.view.quantity.get(), self.view.discount.get(), self.view.supplier.get() 
                ]
            self.view.temp_operations.append(data)
            
            self.view.temp_operations_frame.configure(border_width=5, fg_color= 'gray20', border_color='#21130d', scrollbar_button_color='#696969', scrollbar_button_hover_color='red', scrollbar_fg_color='#333333')
            button = self.view.add_temp_operation_button()
            button.configure(command=lambda btn=button, data=data: self.cached_button_click(btn, data))
            
            for ent in [self.view.fac_name, self.view.product_code, self.view.price, self.view.quantity, self.view.discount, self.view.supplier]:
                if ent == self.view.supplier:
                    ent.set('snow white')
                    continue
                ent.set('')


    def cached_button_click(self, btn, data ):
        self.view.fac_name.set(data[0])
        self.view.product_code.set(data[1])
        self.view.price.set(data[2])
        self.view.quantity.set(data[3])
        self.view.discount.set(data[4])
        self.view.supplier.set(data[5])
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
        if ent == self.view.Entries[0]:# facs names
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
        self.view.recommended_frame.configure(border_width=0,  fg_color='transparent',scrollbar_button_color='#333333', scrollbar_button_hover_color='#333333', scrollbar_fg_color='#333333')


    def clear_recommendation_frames(self):
        for frame in self.view.recommendation_frames:
            frame.destroy()

        self.view.recommendation_frames = []
        self.view.recommended_frame._scrollbar.set(0.0, 0.0)
        self.view.recommended_frame._parent_canvas.yview_moveto(0.0)
