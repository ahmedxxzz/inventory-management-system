from view.main_view import MainView
from model.main_model import MainModel
from controller.Factory.factory_controller import FactoryController
from controller.Customer.customer_controller import CustomerController
from controller.Inventory.inventory_controller import InventoryController

class MainController:
    def __init__(self, root):
        """connect the view and model to control the navigation between main frames

        Args:
            root (ctk.CTk): this is the root window of the application
        """
        self.root = root
        self.model = MainModel()
        self.view = MainView(self.root)
        self._bind_events()
    
    
    
    def _bind_events(self):
        """bind each main side bar buttons to its frame
        """
        for button in self.view.buttons:
            button.configure(command= lambda button_obj=button: self._menu_buttons_switching(title = button_obj.cget("text"), button = button_obj))
        self._menu_buttons_switching(self.view.buttons[0].cget("text"),self.view.buttons[0])


    def _menu_buttons_switching(self, title, button):
        ''' controll the switching between menu buttons and show its frames
         
        steps:
            # change the color and disable the passed button and enable the other
            # destroy the frames
            # add the frame of clicked button
            # append the frame to the self.view.frames
        '''
        for btn in self.view.buttons:
            if title == 'الاشعارات':
                continue
            btn.configure(fg_color='black', state='normal', cursor="hand2")
        if title != 'الاشعارات':
            button.configure(fg_color='green', state='disabled', cursor="arrow")
            
        
        for frame in self.view.Frames:
            frame.destroy()
        self.view.Frames = []
        main_menu_button_map ={
            'المصانع': self.open_factory,
            'المكاتب': self.open_customer,
            'المخزن': self.open_inventory,
            'الخزنة': self.open_safe,
            'المصاريف': self.open_extra_costs,
            'الموزعين': self.open_distributors,
            'الاشعارات': self.open_notifications,
            'الخروج': self.root.destroy
        }
        main_menu_button_map[title]()
        

    def open_factory(self):
        factory = FactoryController(root = self.root, db_conn = self.model.conn)
        self.view.Frames.append(factory.view)


    def open_customer(self):
        customer = CustomerController(root = self.root, db_conn = self.model.conn)
        self.view.Frames.append(customer.view)


    def open_inventory(self):
        inventory = InventoryController(root = self.root, db_conn = self.model.conn)
        self.view.Frames.append(inventory.view)

    def open_safe(self):
        pass
    def open_extra_costs(self):
        pass
    def open_distributors(self):
        pass
    def open_notifications(self):
        pass