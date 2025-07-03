
import customtkinter as ctk


class CustomerView(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root,)
        self.pack(fill='both', expand=True)
        self.buttons = []
        self.Frames = []
        
        self.create_options_buttons()
        
    def create_options_buttons(self):
        self.back_btn = ctk.CTkButton(self, text='رجوع',  font=("Arial", 16, "bold"), width=100, height=30)
        self.back_btn.place(relx=0, rely=0, anchor="nw")

        options_frame = ctk.CTkFrame(self, width=200, corner_radius=5,height=30)
        options_frame.pack(side='top', padx=10)

        options = ['شراء', 'دفعات', 'مرتجع', 'حسابات المكاتب']
        for option in options:
            button = ctk.CTkButton(options_frame, text=option,  font=("Arial", 16, "bold"), width=200, height=40)
            button.pack(side= 'left',padx=10)
            self.buttons.append(button)
