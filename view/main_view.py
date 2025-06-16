import customtkinter as ctk
from PIL import Image
from .Dashboard_view import Dashboard_frame 
from .Factory_view import Factory_frame 






ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self._state_before_windows_set_titlebar_color = 'zoomed'
        self.title('برنامج ادارة المخازن')
        self.buttons = []
        self.Frames = []
        
        
        
        
        
        self.side_bar()
        self.create_buttons()
        
        
    def side_bar(self):
        self.side_bar_frame = ctk.CTkFrame(self, width=160,border_width=5,border_color='yellow')
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
        self.buttons[0].configure(fg_color='green',  state='disabled',cursor="arrow")
        for button in self.buttons:
            button.configure(command= lambda button=button: self.menu_button_click(button))
        
        self.Frames.append(Dashboard_frame(self))
    
    def menu_button_click(self, button):
        for btn in self.buttons:
            btn.configure(fg_color='black', state='normal', cursor="hand2")
        button.configure(fg_color='green', state='disabled', cursor="arrow")
        
        self.switching_frames(button.cget('text'))

    
    def switching_frames(self, text):
        self.destroy_frames()
        
        content_frame = ''
        if text == 'الرئيسية':
            content_frame = Dashboard_frame(self)
        elif text == 'المصانع':
            content_frame = Factory_frame(self)
        self.Frames.append(content_frame)

    def destroy_frames(self):
        for frame in self.Frames:
            frame.destroy()
