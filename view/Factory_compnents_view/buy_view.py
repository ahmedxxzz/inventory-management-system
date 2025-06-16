import customtkinter as ctk

class Buy_frame(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root, fg_color='red',bg_color='red')
        self.pack(fill='both', expand=True)
        