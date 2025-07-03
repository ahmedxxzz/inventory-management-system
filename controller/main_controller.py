from view.main_view import MainView
from model.main_model import MainModel
from controller.dashboard_controller import DashboardController
from controller.factory_controller import FactoryController
from controller.inventory_controller import InventoryController
# from controller.customer_controller import CustomerController
from controller.navigator_controller import NavigatorController

from controller.safe_controller import SafeController


class MainController:
    def __init__(self, root_window):
        self.root = root_window # this is the window
        self.view = MainView(self.root) # this is the left slide with its buttons
        self.model = MainModel()
        self._bind_events()
        
        


    def _bind_events(self):
        for index, btn in enumerate(self.view.buttons):
            btn.configure(command= lambda i=index, button=btn: self._menu_buttons_switching(i, button))
        self._menu_buttons_switching(1,self.view.buttons[1])
    

    def _menu_buttons_switching(self, index, btn):
        '''
        # change the color and disable the button and enable the other
        # destroy the frames
        # add the frame of clicked button
        # append the frame to the self.view.frames
        '''
        for button in self.view.buttons:
            button.configure(fg_color='black', state='normal', cursor="hand2")
        btn.configure(fg_color='green', state='disabled', cursor="arrow")
        
        for frame in self.view.Frames:
            frame.destroy()
        self.view.Frames = []
        
        if index == 0:
            self.open_dashboard()
        elif index == 1:
            self.open_factory()
        elif index == 2:
            self.open_customer()
        elif index == 3:
            self.open_inventory()
        elif index == 4:
            self.open_safe()
        else:
            self.root.destroy()
            exit()
        
        
        
        
    def open_dashboard(self):
        dashboard = DashboardController(self.root)
        self.view.Frames.append(dashboard.view)
    
    def open_factory(self):
        factory = FactoryController(self.root)
        self.view.Frames.append(factory.view)
    
    def open_customer(self):
        customer = NavigatorController(self.root)
        self.view.Frames.append(customer.view)

    def open_inventory(self):
        inventory = InventoryController(self.root)
        self.view.Frames.append(inventory.view)

    def open_safe(self):
        safe = SafeController(self.root)
        self.view.Frames.append(safe.view)