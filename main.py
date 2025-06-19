import customtkinter as ctk
from controller.main_controller import MainController


ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')

def main():
    root = ctk.CTk()
    root.title('برنامج ادارة المخازن')
    root._state_before_windows_set_titlebar_color = 'zoomed'
    
    app = MainController(root)
    root.mainloop()

if __name__ == '__main__':
    main()