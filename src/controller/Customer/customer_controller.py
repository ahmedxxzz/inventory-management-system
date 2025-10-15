from view.Customer.customer_view import CustomerView

class CustomerController:
    def __init__(self, root, db_conn, distributor):
        """create the customer main frame

        Args:
            root (ctk.CTk): this is the root window of the application but contains the side bar frame
            db_conn (sqlite3.Connection): database connection, that is the connection object to the database
            distributor (str): distributor name
        """
        self.root = root
        self.db_conn = db_conn
        self.distributor = distributor
        self.view = CustomerView(root)
        self._bind_events()
    
    
    def _bind_events(self):
        for button in self.view.buttons:
            button.configure(command= lambda button_obj=button: self._menu_buttons_switching(title = button_obj.cget("text"), button = button_obj))
        self._menu_buttons_switching(self.view.buttons[0].cget("text"),self.view.buttons[0])


    def _menu_buttons_switching(self, title, button):
        """handle switching between frames

        Args:
            title (str): button title
            button (ctk.CTkButton): button object that is clicked
        
        Steps:
            # change the color and disable the passed button and enable the other
            # destroy the frames
            # add the frame of clicked button
            # append the frame to the self.view.frames
        """
        # in gactory accounts , we need to check password before destroy frames
        if title == 'حسابات المكاتب':
            if not self.check_password():
                return 
        for btn in self.view.buttons:
            btn.configure(fg_color='#206ca4', state='normal', cursor="hand2")
        button.configure(fg_color='yellow', state='disabled', cursor="arrow")    
        
        for frame in self.view.Frames:
            frame.destroy()
        self.view.Frames.clear()
        
        customer_menu_button_map ={
            'فاتورة': self.open_buy,
            'دفعة': self.open_pay,
            'مرتجع': self.open_return,
            'حسابات المكاتب': self.open_account,
        }
        customer_menu_button_map[title]()


    def open_buy(self):
        from controller.Customer.customer_sales_controller import CustomerSalesController
        customer_sales = CustomerSalesController(self.view, self.db_conn, self.distributor)
        self.view.Frames.append(customer_sales.view)


    def open_pay(self):
        pass
    def open_return(self):
        pass


    def open_account(self):
        from controller.Customer.customer_account_controller import CustomerAccountController
        customer_account = CustomerAccountController(self.view, self.db_conn, self.distributor, self.view.Frames)
        self.view.Frames.append(customer_account.view)


    def check_password(self):
        from main import PASSWORD
        password = self.view.create_password_popup()
        if password == PASSWORD:
            return True
        elif password !=PASSWORD  and password is not None :
            self.view.message("showinfo", "خطأ", "كلمة المرور غير صحيحة")
            return self.check_password()
        if password is None:
            return False

