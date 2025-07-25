from view.Customer_compnents_view.returns_view import ReturnView
from model.Customer_compnents_model.returns_model import ReturnModel
from controller.Customer_compnents_controller.report_controller import ReportController


class ReturnController:
    def __init__(self, root, supplier):
        self.root = root
        self.supplier = supplier
        self.view = ReturnView(self.root)
        self.model = ReturnModel(self.supplier)
        self.recommendation_type = ''
        
        self._bind_events()
        self.view.populate_treeview(self.model.get_returns_from_db())
        
    
    def _bind_events(self):
        for ent in [self.view.Entries[0], self.view.Entries[1]]:
            ent.bind('<FocusIn>', lambda event, ent = ent: self.recommendation_focusIn(ent, ent.cget("textvariable")))
            ent.bind('<KeyRelease>', lambda event, ent = ent, recommendation_type = self.recommendation_type: self.recommendation_KeyRelease(ent, ent.cget("textvariable"), recommendation_type))
            ent.bind('<FocusOut>', lambda event: self.recommendation_focusOut())

        self.view.button.configure(command=self.save_return)
    
    
    
    
    
    def save_return(self):
        '''
        # 1- check if inputs except 'reason' are not empty
        # 2- check if cusname exist and product code exist
        4- save the return
        المفروض minus the quantity بس خلى ده فى الاخر 

        '''
        
        
        data = [self.view.cus_name.get(),self.view.product_code.get(),self.view.quantity.get(),self.view.reason.get()]
        for item in data:
            if item == '':
                self.view.message('showinfo', 'عملية فاشلة', 'يرجى عدم ترك الحقول فارغة')
                return

        if not self.model.check_customer_name_exist(self.view.cus_name.get().strip()):
            self.view.message('showinfo', 'عملية فاشلة', 'اسم المصنع غير موجود')
            return

        if not self.model.check_product_code_exist(self.view.product_code.get()):
            self.view.message('showinfo', 'عملية فاشلة', 'كود المنتج غير موجود')
            return
        

        
        
        

        
        if self.model.save_return_to_db(data):
            self.view.message('showinfo', 'عملية ناجحة', 'تمت عملية الاسترجاع بنجاح')
            if self.view.message('yes_no', 'فاتورة', 'هل تريد طباعة الفاتورة ؟'):
                ReportController(data , 'return')
            self.view.clear_inputs()
        self.view.populate_treeview(self.model.get_returns_from_db())







    def recommendation_focusIn(self, ent, var):
        self.clear_recommendation_frames()
        self.view.recommended_frame.configure(border_width=5, fg_color= 'gray20', border_color='#21130d', scrollbar_button_color='#696969', scrollbar_button_hover_color='red', scrollbar_fg_color='#333333')
        
        self.recommendation_type = ''
        if ent == self.view.Entries[0]:# cuss names
            # [("جلوبال تك للتصنيع",500), ("حلول الروبوتات الدقيقة",4000)]
            self.view.recommendations = self.model.get_customer_names_and_money()
            self.recommendation_type = 'cus_names with money'


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
            for cus, money in self.view.recommendations:
                if var_text in str(cus):
                    matching_items.append((str(cus), money))
            
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
