import customtkinter as ctk

class Pay_frame(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root, fg_color='green',bg_color='green')
        self.pack(fill='both', expand=True)
        