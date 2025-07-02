from view.inventory_view import InventoryView
from controller.Inventory_components_controller.adding_type_controller import AddingTypeController


class InventoryController:
    def __init__(self, root):
        self.root = root # this is the window (there is a left slide inside the window but i can't access it here)
        self.view = InventoryView(self.root)
        self._bind_events()
        

    def _bind_events(self):
        for index, btn in enumerate(self.view.buttons):
            btn.configure(command= lambda i=index, button=btn: self._menu_buttons_switching(i, button))
        self._menu_buttons_switching(0,self.view.buttons[0])

    def _menu_buttons_switching(self, index, btn):
        '''
        # change the color and disable the button and enable the other
        # destroy the frames
        add the frame of clicked button
        append the frame to the self.view.frames
        '''
        for button in self.view.buttons:
            button.configure(fg_color='#206ca4', state='normal', cursor="hand2")
        btn.configure(fg_color='yellow', state='disabled', cursor="arrow")
        
        for frame in self.view.Frames:
            frame.destroy()
        self.view.Frames = []
        
        
        
        if index == 0:
            self.open_adding_type()
        # elif index == 1:
        #     self.open_pay()

        
        
        
    def open_adding_type(self):
        add_type = AddingTypeController(self.view)
        self.view.Frames.append(add_type.view)
    
    # def open_pay(self):
    #     pay = PayController(self.view)
    #     self.view.Frames.append(pay.view)

