import customtkinter as ctk

class InventoryView(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root)
        self.pack(side='left', fill='both', expand=True)
        
        self.buttons = []
        self.Frames = []
        
        self.create_options_buttons()


 
    def create_options_buttons(self):
        options_frame = ctk.CTkFrame(self, width=200, corner_radius=5,height=30)
        options_frame.pack(side ='top',padx = 10)
        
        options = ['اضافة صنف', 'عرض مخزون المصانع', 'بلااااا', 'بلاااا']
        for option in options:
            button = ctk.CTkButton(options_frame, text=option,  font=("Arial", 16, "bold"), width=200, height=40)
            button.pack(side='left',padx=10)
            self.buttons.append(button)
        
        
        