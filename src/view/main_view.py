import customtkinter as ctk
from PIL import Image
from tkinter import StringVar

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
            if title == 'الاشعارات':
                self.notification_button = button


    def create_distributor_popup(self, distributors):
        """create popup to choose distributor for the customer page

        Args:
            distributors (list): list of distributors from database

        Returns:
            distributor StringVar: to hold the distributor name chosen
        """
        popup = ctk.CTkToplevel(self, )
        popup.grab_set()
        popup.geometry(f'+900+450')
        
        
        self.distributor_var = StringVar(value="اختر الموزع")
        
        ctk.CTkLabel(popup, text='اختار الموزع', font=("Arial", 14)).pack(pady=10, padx=20)
        option_menu = ctk.CTkOptionMenu(popup, values=["اختر الموزع", *distributors], variable = self.distributor_var)
        option_menu.pack(pady=10, padx=20)
        
        button_frame = ctk.CTkFrame(popup, fg_color="transparent")
        button_frame.pack(pady=10)
        
        ok_btn = ctk.CTkButton(button_frame, text="موافق", command=popup.destroy)
        ok_btn.pack(side="left", padx=10)
        cnl_btn =ctk.CTkButton(button_frame, text="إلغاء", command=popup.destroy)
        cnl_btn.pack(side="left", padx=10)
        
        popup.bind('<Return>', lambda event: ok_btn.invoke())
        popup.bind("<Escape>", lambda event: cnl_btn.invoke())
        
        # block the code untill the popup is destroyed # i used it to change the password before return it .
        self.wait_window(popup)
        if self.distributor_var.get() == "اختر الموزع":
            self.distributor_var.set('')
        return self.distributor_var.get()



    def update_notification_count(self, count):
        """Updates the notification button text with the count of unseen notifications."""
        if count > 0:
            self.notification_button.configure(text=f"الاشعارات ({count})", fg_color="red")
        else:
            self.notification_button.configure(text="الاشعارات", fg_color="black")
