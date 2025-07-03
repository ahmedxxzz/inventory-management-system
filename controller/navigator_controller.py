from controller.customer_controller import CustomerController
from view.navigator_view import NavigatorView



class NavigatorController:
    def __init__(self, root_window) -> None:
        self.root = root_window # the window
        self.view = NavigatorView(self.root) # now this is the content frame 
        self._bind_events()


    def _bind_events(self):
        self.view.Golden_label.bind("<Button-1>", lambda e: self.on_image_click("golden rose"))
        self.view.Snow_label.bind("<Button-1>", lambda e: self.on_image_click("snow white"))




    def on_image_click(self, supplier):
        self.view.destroy()
        CustomerController(self.root, supplier)

    