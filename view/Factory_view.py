
import customtkinter as ctk


class FactoryView(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root,)
        self.pack(fill='x')
        self.buttons = []
        self.Frames = []
        
        self.create_options_buttons()
        
    def create_options_buttons(self):
        header_frame = ctk.CTkFrame(self, width=200, corner_radius=5,height=30)
        header_frame.pack(side='top', padx=10)
        options = ['شراء', 'دفعات', 'استرجاع', 'حسابات المصانع']
        for option in options:
            button = ctk.CTkButton(header_frame, text=option,  font=("Arial", 16, "bold"), width=200, height=40)
            button.pack(side= 'left',padx=10)
            self.buttons.append(button)
