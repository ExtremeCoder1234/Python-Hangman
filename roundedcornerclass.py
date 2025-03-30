import tkinter as tk
import customtkinter as ctk

class CustomFrame(ctk.CTkFrame):
    """Custom frame with center at the center."""
    def __init__(self, master=None, theme="dark", **kwargs):
        ctk.set_appearance_mode(theme.capitalize())  # Set the appearance mode (light/dark)
        super().__init__(master, **kwargs)
        self.place_forget()

    def show_frame(self):
        self.place(relx=0.5, rely=0.5, anchor="center")

    def hide_frame(self):
        self.place_forget()