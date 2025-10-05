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
        for btn in self.view.buttons:
            btn.configure(fg_color='#206ca4', state='normal', cursor="hand2")
        button.configure(fg_color='yellow', state='disabled', cursor="arrow")    
        
        for frame in self.view.Frames:
            frame.destroy()
        self.view.Frames = []
        
        factory_menu_button_map ={
            'فاتورة': self.open_buy,
            'دفعة': self.open_pay,
            'مرتجع': self.open_return,
            'حسابات المصانع': self.open_account,
        }
        factory_menu_button_map[title]()


    def open_buy(self):
        pass
    def open_pay(self):
        pass
    def open_return(self):
        pass
    def open_account(self):
        pass