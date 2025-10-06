import customtkinter as ctk
from PIL import Image

class MainView(ctk.CTkFrame):
    """create main side bar to navigate between main frames

    Inherits from: ctk.CTkFrame
    """
    def __init__(self, root):
        """initialize main side bar frame with its characteristics

        Args:
            root (ctk.CTk): this is the root window of the application
        """
        super().__init__(root,  width=160,border_width=2,border_color='yellow' )
        self.pack_propagate(False)
        self.pack(side='left', fill='y')
        
        
        self.root = root 
        self.buttons = []
        self.Frames = []
        
        self.side_bar()
        self.create_buttons()
        
    def side_bar(self):
        """add the logo to side bar frame
        """
        logo_image = Image.open('Z_Files/images/Elbahgy Logo.png')
        photo_image = ctk.CTkImage(light_image=logo_image,dark_image=logo_image,size=(100, 65))
        lbl_menuLogo = ctk.CTkLabel(self, image=photo_image, text='',bg_color='black')
        lbl_menuLogo.pack(side='top', fill='x')
        menu_label = ctk.CTkLabel(self, text='القائمة', bg_color='yellow', text_color='black',font=ctk.CTkFont(size=20, weight='bold'))
        menu_label.pack(side='top', fill='x')


    def create_buttons(self):
        """create buttons to navigate between main frames
        """
        titles  = ['المصانع', 'المكاتب', 'المخزن', 'الموزعين', 'الخزنة', 'المصاريف', 'الاشعارات', 'الخروج']
        for title in titles:
            button = ctk.CTkButton(self, text=title, state='normal', fg_color='black', text_color='yellow',font=ctk.CTkFont(size=20, weight='bold'),corner_radius=20, cursor="hand2", hover_color='red' ,height=50,)
            button.pack(side='top', fill='x',pady=10,padx=10)
            self.buttons.append(button)

