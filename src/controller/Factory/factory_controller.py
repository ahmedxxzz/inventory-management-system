from view.Factory.factory_view import FactoryView

class FactoryController:
    def __init__(self, root, db_conn):
        """create the factory main frame

        Args:
            root (ctk.CTk): this is the root window of the application but contains the side bar frame
            db_conn (sqlite3.Connection): database connection, that is the connection object to the database
        """
        self.root = root
        self.db_conn = db_conn
        self.view = FactoryView(root)
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
        # in factory accounts , we need to check password before destroy frames
        if title == 'حسابات المصانع':
            if not self.check_password():
                return 
        for btn in self.view.buttons:
            btn.configure(fg_color='#206ca4', state='normal', cursor="hand2")
        button.configure(fg_color='yellow', state='disabled', cursor="arrow")    
    
        for frame in self.view.Frames:
            frame.destroy()
        self.view.Frames.clear()
        
        factory_menu_button_map ={
            'فاتورة': self.open_buy,
            'دفعة': self.open_pay,
            'مرتجع': self.open_return,
            'حسابات المصانع': self.open_account,
        }
        factory_menu_button_map[title]()


    def open_buy(self):
        from controller.Factory.factory_buy_controller import FactoryBuyController
        factory_buy = FactoryBuyController(self.view, self.db_conn)
        self.view.Frames.append(factory_buy.view)


    def open_pay(self):
        from controller.Factory.factory_pay_controller import FactoryPayController
        factory_pay = FactoryPayController(self.view, self.db_conn)
        self.view.Frames.append(factory_pay.view)


    def open_return(self):
        from controller.Factory.factory_return_controller import FactoryReturnController
        factory_return = FactoryReturnController(self.view, self.db_conn)
        self.view.Frames.append(factory_return.view)


    def open_account(self):
        from controller.Factory.factory_account_controller import FactoryAccountController
        factory_account = FactoryAccountController(self.view, self.db_conn, self.view.Frames)
        self.view.Frames.append(factory_account.view)

    
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

