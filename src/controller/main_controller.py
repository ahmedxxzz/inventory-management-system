from view.main_view import MainView
from model.main_model import MainModel
from controller.Factory.factory_controller import FactoryController
from controller.Customer.customer_controller import CustomerController
from controller.Inventory.inventory_controller import InventoryController
from controller.distributor_controller import DistributorController
from controller.wallet_controller import WalletController
from controller.extra_costs_controller import ExtraCostController
import threading

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
        initial_check_thread = threading.Thread(target=self.check_for_notifications, daemon=True)
        initial_check_thread.start()


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
        if title == 'المكاتب':
            distributor = self.choose_customer_distributor()
            if not distributor:
                return None
        for btn in self.view.buttons:
            if btn.cget("text") == 'الاشعارات':
                continue
            btn.configure(fg_color='black', state='normal', cursor="hand2")
        if title != 'الاشعارات':
            button.configure(fg_color='green', state='disabled', cursor="arrow")
            
        
        for frame in self.view.Frames:
            frame.destroy()
        self.view.Frames.clear()
        main_menu_button_map ={
            'المصانع': self.open_factory,
            'المكاتب': self.open_customer,
            'المخزن': self.open_inventory,
            'الموزعين': self.open_distributors,
            'الخزنة': self.open_wallet,
            'المصاريف': self.open_extra_costs,
            'الاشعارات': self.open_notifications,
            'الخروج': self.root.destroy
        }
        if title == 'المكاتب':
            main_menu_button_map[title](distributor)
        else:
            main_menu_button_map[title]()
        

    def open_factory(self):
        factory = FactoryController(root = self.root, db_conn = self.model.conn)
        self.view.Frames.append(factory.view)


    def open_customer(self, distributor = None):
        customer = CustomerController(root = self.root, db_conn = self.model.conn, distributor = distributor)
        self.view.Frames.append(customer.view)


    def open_inventory(self):
        inventory = InventoryController(root = self.root, db_conn = self.model.conn)
        self.view.Frames.append(inventory.view)


    def open_distributors(self):
        distributor = DistributorController(root = self.root, db_conn = self.model.conn)
        self.view.Frames.append(distributor.view)


    def open_wallet(self):
        wallet = WalletController(root = self.root, db_conn = self.model.conn)
        self.view.Frames.append(wallet.view)


    def open_extra_costs(self):
        costs = ExtraCostController(root = self.root, db_conn = self.model.conn)
        self.view.Frames.append(costs.view)


    def open_notifications(self):
        """Opens the full notification history page with filtering capabilities."""
        def on_notifications_updated():
            # This will be called by the notification controller to update the count
            count = self.model.get_unseen_notification_count()
            self.view.update_notification_count(count)

        # We need the list of distributors for the filter
        distributors = self.model.get_distributors()
        from controller.notification_controller import NotificationController

        notifications_page = NotificationController(
            root=self.root, 
            db_conn=self.model.conn,
            on_close_callback=on_notifications_updated,
            distributors=distributors # Pass the list to the controller
        )
        self.view.Frames.append(notifications_page.view)


    def choose_customer_distributor(self):
        return self.view.create_distributor_popup(self.model.get_distributors())


    def check_for_notifications(self):
        """
        Generates new notifications, updates the count on the view,
        and schedules itself to run again.
        """
        print("Checking for new notifications...")
        # 1. Generate new notifications in the database
        self.model.generate_all_notifications()
        
        # 2. Get the count of unseen notifications
        count = self.model.get_unseen_notification_count()
        
        # 3. Update the view with the new count
        self.view.update_notification_count(count)
        
        # 4. Schedule this check to run again after 1 hour (3,600,000 milliseconds)
        # For testing, you can set it to a shorter time, e.g., 30000 for 30 seconds.
        self.root.after(3600000, self.check_for_notifications)