import customtkinter as ctk
from tkinter import StringVar, ttk , messagebox, filedialog

class DistributorView(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root, fg_color="transparent")
        self.pack(fill="both", expand=True, padx=20, pady=20)
        self.distributor_name_var = StringVar()
        self.logo_path_var = StringVar()
        self.buttons = []
        self.create_upper_frame()
        self.create_bottom_frame()

    def create_upper_frame(self):
        upper_frame = ctk.CTkFrame(self, corner_radius=5, border_width=5, border_color='yellow')
        upper_frame.pack(side='top', padx=10, fill='x')
        
        # Frame for Distributor Name
        adding_distributor_frame = ctk.CTkFrame(upper_frame)
        adding_distributor_frame.pack(side='top', pady=(10, 5), padx=10, fill='x')
        lbl_name = ctk.CTkLabel(adding_distributor_frame, text='اسم الموزع', font=("Arial", 16, "bold"), text_color='white', width=150, height=40)
        lbl_name.pack(side='right', pady=5, padx=10)
        ent_name = ctk.CTkEntry(adding_distributor_frame, textvariable=self.distributor_name_var, font=("Arial", 16, "bold"), height=40, justify='right')
        ent_name.pack(side='right', padx=10, pady=5, fill='x', expand=True)

        # Frame for Logo Path
        logo_frame = ctk.CTkFrame(upper_frame)
        logo_frame.pack(side='top', pady=(5, 10), padx=10, fill='x')
        lbl_logo = ctk.CTkLabel(logo_frame, text='صورة اللوجو', font=("Arial", 16, "bold"), text_color='white', width=150, height=40)
        lbl_logo.pack(side='right', pady=5, padx=10)
        self.logo_path_entry = ctk.CTkEntry(logo_frame, textvariable=self.logo_path_var, font=("Arial", 12), height=40, justify='left', state='readonly') # Read-only
        self.logo_path_entry.pack(side='right', padx=10, pady=5, fill='x', expand=True)
        self.browse_button = ctk.CTkButton(logo_frame, text="اختر صورة...", font=("Arial", 14, "bold"), width=120)
        self.browse_button.pack(side='right', padx=10)
        
        # Buttons Frame
        btns_frame = ctk.CTkFrame(upper_frame, corner_radius=5)
        btns_frame.pack(side='top', padx=10, pady=10, fill='x')
        btns = ['اضافة', 'حذف', 'تعديل', 'تنظيف المدخلات']
        for i, btn in enumerate(btns):
            button = ctk.CTkButton(btns_frame, text=btn, font=("Arial", 18, "bold"), text_color='white',width=200, height=40, fg_color='green' if i ==0 else 'red' if i == 1 else '#309aee' if i == 2 else '#30eee5')
            button.pack(side='right', padx=110, pady=10)
            self.buttons.append(button)

    def create_bottom_frame(self):
        bottom_frame = ctk.CTkFrame(self, corner_radius=5)
        bottom_frame.pack(fill='both', expand=True, padx=10, pady=10)
        bottom_frame.grid_rowconfigure(0, weight=1); bottom_frame.grid_columnconfigure(0, weight=1)

        style = ttk.Style() 
        style.theme_use("default"); style.configure("Treeview",background="#2b2b2b",foreground="white",rowheight=25,fieldbackground="#2b2b2b",bordercolor="#343638",borderwidth=0); style.map('Treeview', background=[('selected', '#8B0000')], foreground=[('selected', 'white')]); style.configure("Treeview.Heading",background="#565b5e",foreground="white",relief="flat",font=('Arial', 12, 'bold')); style.map("Treeview.Heading",background=[('active', '#3484F0')])

        # ADD 'logo_path' to columns
        self.tree_columns = ('logo_path', 'distributor_name')
        self.tree_headers = ['مسار اللوجو', 'اسم الموزع']
        self.tree = ttk.Treeview(bottom_frame, columns=self.tree_columns, show='headings', selectmode="extended")
        
        for i, col in enumerate(self.tree_columns):
            self.tree.heading(col, text=self.tree_headers[i], anchor='center')
        
        self.tree.column('distributor_name', anchor='center')
        self.tree.column('logo_path', anchor='w', width=400) # 'w' = west (left)

        v_scrollbar = ttk.Scrollbar(bottom_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(bottom_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        self.tree.grid(row=0, column=0, sticky='nsew'); v_scrollbar.grid(row=0, column=1, sticky='ns'); h_scrollbar.grid(row=1, column=0, sticky='ew')

    def browse_for_image(self):
        """Opens a file dialog to select an image and returns the path."""
        file_path = filedialog.askopenfilename(
            title="اختر صورة اللوجو",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
        )
        if file_path:
            self.logo_path_var.set(file_path)
            return file_path
        return None

    def populate_treeview(self, data):
        for item in self.tree.get_children(): self.tree.delete(item)
        for row_data in data: self.tree.insert("", "end", values=row_data)
        
    def bind_table(self, function=None):
        self.tree.bind('<<TreeviewSelect>>', lambda e, func=function: self.on_row_select(e, func))

    def on_row_select(self, event, func):
        selected_item_id = self.tree.focus()
        if selected_item_id: func(self.tree.item(selected_item_id, 'values'))

    def message(self, mstype, info_text, text):
        if mstype == "yes_no": return messagebox.askyesno(info_text, text)
        elif mstype == "showinfo": messagebox.showinfo(info_text, text)

