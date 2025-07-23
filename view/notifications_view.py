import customtkinter as ctk


class NotificationsView(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root, corner_radius=5,border_width=5)
        self.pack(side='top', fill='both',expand=True)
        
        self.supplier = ctk.StringVar(value='snow white')
        
        self.create_upper_frame()
        self.create_scrollable_frame()
        
    def create_upper_frame(self):
        upper_frame = ctk.CTkFrame(self, corner_radius=5,border_width=5,border_color='yellow')
        upper_frame.pack(side='top', fill='x')
        
        self.supplier_opt = ctk.CTkOptionMenu(upper_frame, values=['golden rose', 'snow white'], variable=self.supplier)
        self.supplier_opt.pack(side='top', padx=10, pady=10)
        
    def create_scrollable_frame(self):
        self.scrollable_frame = ctk.CTkScrollableFrame(self, corner_radius=5, width=1000)
        self.scrollable_frame.pack(side='top', fill='y',expand=True)
        
    
    def create_notification_frame(self, message='احه المكتب ده فشخك ب 500 جنيه '):
        notification_frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=5,border_width=5,border_color='yellow', height=100)
        notification_frame.pack(side='top', fill='x',padx=10, pady=10)
        close_button = ctk.CTkButton(notification_frame,text="X", text_color="red", font=("Arial", 25), width=3, fg_color='transparent',hover=False)
        close_button.pack(side="right", padx=5, pady=5)
        
        message_label = ctk.CTkLabel(notification_frame, text=message, font=("Arial", 20, "bold"), text_color='white',width=200, height=40)
        message_label.pack(side='top', padx=10, pady=10)
        
        return notification_frame, close_button
        