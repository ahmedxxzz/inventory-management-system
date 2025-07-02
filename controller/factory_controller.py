from view.factory_view import FactoryView
from controller.Factory_compnents_controller.buy_controller import BuyController
from controller.Factory_compnents_controller.pay_controller import PayController
from controller.Factory_compnents_controller.return_controller import ReturnController
from controller.Factory_compnents_controller.factory_account_controller import FactoryAccountController

class FactoryController:
    def __init__(self, root_window) -> None:
        self.root = root_window # the window
        self.view = FactoryView(self.root) # now this is the content frame 
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
            self.open_buy()
        elif index == 1:
            self.open_pay()
        elif index == 2:
            self.open_return()
        elif index == 3:
            self.open_account()

        
        
        
        
    def open_buy(self):
        buy = BuyController(self.view)
        self.view.Frames.append(buy.view)
    
    def open_pay(self):
        pay = PayController(self.view)
        self.view.Frames.append(pay.view)

    def open_return(self):
        returns = ReturnController(self.view)
        self.view.Frames.append(returns.view)

    def open_account(self):
        account = FactoryAccountController(self.view)
        self.view.Frames.append(account.view)