
import customtkinter as ctk
from .Factory_compnents_view.buy_view import Buy_frame
from .Factory_compnents_view.pay_view import Pay_frame
class Factory_frame(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root)
        self.pack(fill='both', expand=True)
        self.buttons = []
        self.Frames = []
        
        self.create_options_buttons()
        self.switching_options_frames('شراء')
        
    
    def create_options_buttons(self):
        header_frame = ctk.CTkFrame(self, width=200, corner_radius=5,height=30)
        # header_frame.pack_propagate(False)
        header_frame.pack(side='top', padx=10)
        options = ['شراء', 'دفعات', 'استرجاع', 'حسابات المصانع']
        for option in options:
            button = ctk.CTkButton(header_frame, text=option,  font=("Arial", 16, "bold"), width=200, height=40)
            button.pack(side= 'left',padx=10)
            self.buttons.append(button)
        self.buttons[0].configure(fg_color='yellow', state='disabled', cursor="arrow")
        for button in self.buttons:
            button.configure(command= lambda button=button: self.options_button_click(button))
    
    def options_button_click(self, button):
        for btn in self.buttons:
            btn.configure(fg_color='#206ca4', state='normal', cursor="hand2")
        button.configure(fg_color='yellow', state='disabled', cursor="arrow")
        
        self.switching_options_frames(button.cget('text'))
    
    def switching_options_frames(self, text):
        self.destroy_frames()
        
        content_frame = ''
        if text == 'شراء':
            content_frame = Buy_frame(self)
        elif text == 'دفعات':
            content_frame = Pay_frame(self)
        # elif text == 'استرجاع':
        #     content_frame = Return_frame(self)
        # elif text == 'حسابات المصانع':
        #     content_frame = Account_frame(self)
        self.Frames.append(content_frame)
    
    def destroy_frames(self):
        for frame in self.Frames:
            frame.destroy()