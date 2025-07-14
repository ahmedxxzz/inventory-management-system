import customtkinter as ctk


class DashboardView(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root, fg_color='red')
        self.pack(fill='both', expand=True)
        self.create_upper_frame()
        # self.create_bottom_frame()
    
    def create_upper_frame(self):
        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color='green')
        self.scrollable_frame.pack(side='top', fill='both', expand=True)
        
        
        
        
    
    
    # def data_frame(self):
    #     main_frame = ctk.CTkFrame(self, corner_radius=5,border_width=5,border_color='yellow')
    #     main_frame.pack(side='top', fill='x')
        
        