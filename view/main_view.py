import customtkinter as ctk
from PIL import Image

class MainView:
    def __init__(self, root):
        self.root = root 
        self.buttons = []
        self.Frames = []
        
        self.side_bar()
        self.create_buttons()
        
        
    def side_bar(self):
        self.side_bar_frame = ctk.CTkFrame(self.root, width=160,border_width=5,border_color='yellow')
        self.side_bar_frame.pack_propagate(False)
        self.side_bar_frame.pack(side='left', fill='y')
        
        logo_image = Image.open('images/Elbahgy Logo.png')
        photo_image = ctk.CTkImage(light_image=logo_image,dark_image=logo_image,size=(100, 65))
        lbl_menuLogo = ctk.CTkLabel(self.side_bar_frame, image=photo_image, text='',bg_color='black')
        lbl_menuLogo.pack(side='top', fill='x')
        
        menu_label = ctk.CTkLabel(self.side_bar_frame, text='القائمة', bg_color='yellow', text_color='black',font=ctk.CTkFont(size=20, weight='bold'))
        menu_label.pack(side='top', fill='x')
        
        
    def create_buttons(self):
        buttons = [ 'الرئيسية', 'المصانع', 'المكاتب', 'الاحصائيات', 'الخروج']
        for button in buttons:
            button = ctk.CTkButton(self.side_bar_frame, text=button, state='normal', fg_color='black', text_color='yellow',font=ctk.CTkFont(size=20, weight='bold'),corner_radius=20, cursor="hand2", hover_color='red' ,height=50,)
            button.pack(side='top', fill='x',pady=10,padx=10)
            self.buttons.append(button)
        
