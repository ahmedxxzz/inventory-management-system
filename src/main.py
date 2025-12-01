import customtkinter as ctk
from controller.main_controller import MainController


PASSWORD = "2002"


def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    root.title("Elbahgy لادارة المخازن")
    root._state_before_windows_set_titlebar_color = "zoomed"

    app = MainController(root)
    root.mainloop()


if __name__ == "__main__":
    main()
