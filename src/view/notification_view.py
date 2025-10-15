import customtkinter as ctk
from tkinter import ttk

class NotificationView(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root)
        self.pack(fill='both', expand=True, padx=10, pady=10)
        self.configure(fg_color="transparent")

        title_font = ctk.CTkFont(family="Arial", size=20, weight="bold")
        main_font = ctk.CTkFont(family="Arial", size=14)
        
        # --- Top frame for title and filter ---
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(top_frame, text="سجل الإشعارات", font=title_font).pack(side="right", padx=20)
        
        # Distributor filter
        self.distributor_filter_menu = ctk.CTkOptionMenu(top_frame, font=main_font, width=200)
        self.distributor_filter_menu.pack(side="left", padx=20)
        ctk.CTkLabel(top_frame, text=":فلترة حسب الموزع", font=main_font).pack(side="left")

        # --- Table frame ---
        table_frame = ctk.CTkFrame(self)
        table_frame.pack(fill='both', expand=True, padx=10, pady=5)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))
        self.tree = ttk.Treeview(table_frame, columns=("status", "message", "date"), show="headings")
        
        self.tree.heading("date", text="التاريخ والوقت", anchor='center')
        self.tree.heading("message", text="الإشعار", anchor='e')
        self.tree.heading("status", text="الحالة", anchor='center')
        self.tree.column("date", width=150, anchor='center')
        self.tree.column("message", width=600, anchor='e')
        self.tree.column("status", width=100, anchor='center')
        self.tree.pack(side='right', fill='both', expand=True)

        self.tree.tag_configure('unseen', background='#552222', font=('Arial', 10, 'bold'))
        self.tree.tag_configure('seen', background='#2a2d2e', foreground='gray')

        # --- Button ---
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=10)
        self.mark_seen_button = ctk.CTkButton(button_frame, text="تحديد الكل كمقروء", font=('Arial', 14, 'bold'))
        self.mark_seen_button.pack()