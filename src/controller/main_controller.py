from view.main_view import MainView
from model.main_model import MainModel

class MainController:
    def __init__(self, root):
        self.root = root
        self.model = MainModel()
        self.view = MainView(self.root)
        self._bind_events()
    
    
    
    def _bind_events(self):
        """bind each main side bar buttons to its frame
        """
        for button in self.view.buttons:
            button.configure(command= lambda button_obj=button: self._menu_buttons_switching(title = button_obj.cget("text"), button = button_obj))


    def _menu_buttons_switching(self, title, button):
        ''' controll the switching between menu buttons and show its frames
         
        steps:
            # change the color and disable the passed button and enable the other
            # destroy the frames
            # add the frame of clicked button
            # append the frame to the self.view.frames
        '''
        for button in self.view.buttons:
            if title == 'الاشعارات':
                continue
            button.configure(fg_color='black', state='normal', cursor="hand2")
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
            'الاشعارات': self.open_notifications,
            'الخروج': self.root.destroy
        }
        main_menu_button_map[title]()
        

    def open_factory(self):
        pass
    def open_customer(self):
        pass
    def open_inventory(self):
        pass
    def open_safe(self):
        pass
    def open_extra_costs(self):
        pass
    def open_notifications(self):
        pass
    