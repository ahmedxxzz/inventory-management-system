# import customtkinter as ctk
from tkinter import *

from PIL import Image, ImageTk



class NavigatorView(Frame):
    def __init__(self, root):
        super().__init__(root)
        self.pack(side='left', fill='both', expand=True)
        self.create_image_label()
        self.bind("<Configure>", self.update_images)
        self.update_images()


    def create_image_label(self):
        self.golden_rose_img = Image.open("images/Golden_Rose.png")
        self.snow_white_img = Image.open("images/snow_white.png")
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        # Create image containers with padding and border
        self.Golden_label =Label(self, padx=30, pady=40, borderwidth=2, relief="solid", background='#2b2b2b')
        self.Snow_label =Label(self, padx=30, pady=40, borderwidth=2, relief="solid", background='#2b2b2b')
        # Place labels in grid
        self.Golden_label.grid(row=0, column=0, sticky="nsew")
        self.Snow_label.grid(row=0, column=1, sticky="nsew")



    def update_images(self, event=None):
        # Get current window size
        window_width = self.winfo_width()
        window_height = self.winfo_height()

        # Calculate label size (each label gets half the window width)
        label_width = window_width // 2
        label_height = window_height

        # Calculate available space after padding
        padx = 30
        pady = 30
        available_width = label_width - 2 * padx
        available_height = label_height - 2 * pady

        # Skip update if window is too small
        if available_width <= 0 or available_height <= 0:
            return

        # Resize images while maintaining aspect ratio
        for original_img, label in [(self.golden_rose_img, self.Golden_label), (self.snow_white_img, self.Snow_label)]:
            original_width, original_height = (400,300)
            # Calculate scaling factors
            scale_width = available_width / original_width
            scale_height = available_height / original_height
            # Compute new dimensions
            new_width = int(original_width * scale_width)
            new_height = int(original_height * scale_height)
            # Resize image
            resized_img = original_img.resize((new_width, new_height))
            tk_img = ImageTk.PhotoImage(resized_img)
            # Update label
            label.config(image=tk_img)
            label.image = tk_img # Keep a reference to avoid garbage collection

