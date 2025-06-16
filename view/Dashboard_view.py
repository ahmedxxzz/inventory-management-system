import customtkinter as ctk


class Dashboard_frame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, bg_color='red')
        self.pack(fill='both', expand=True)