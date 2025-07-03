from view.customer_view import CustomerView
from controller.Customer_compnents_controller.buy_controller import BuyController
from controller.Customer_compnents_controller.pay_controller import PayController
from controller.Customer_compnents_controller.return_controller import ReturnController
from controller.Customer_compnents_controller.customer_account_controller import CustomerAccountController

class CustomerController:
    def __init__(self, root_window, supplier) -> None:
        self.root = root_window # the window
        self.supplier = supplier
        self.view = CustomerView(self.root) # now this is the content frame 
        self._bind_events()


    def _bind_events(self):
        for index, btn in enumerate(self.view.buttons):
            btn.configure(command= lambda i=index, button=btn: self._menu_buttons_switching(i, button))
        self._menu_buttons_switching(0,self.view.buttons[0])
        self.view.back_btn.configure(command=self.back)


    def _menu_buttons_switching(self, index, btn):
        '''
        # change the color and disable the button and enable the other
        # destroy the frames
        # add the frame of clicked button
        # append the frame to the self.view.frames
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
        buy = BuyController(self.view, self.supplier)
        self.view.Frames.append(buy.view)


    def open_pay(self):
        pay = PayController(self.view, self.supplier)
        self.view.Frames.append(pay.view)


    def open_return(self):
        returns = ReturnController(self.view, self.supplier)
        self.view.Frames.append(returns.view)


    def open_account(self):
        account = CustomerAccountController(self.view, self.supplier)
        self.view.Frames.append(account.view)


    def back(self):
        from controller.navigator_controller import NavigatorController
        self.view.destroy()
        navigator = NavigatorController(self.root)

