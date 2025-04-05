import tkinter as tk
import customtkinter as ctk
import tkinter.simpledialog as simpledialog

def set_icon_dir(varibale, value):
    """Sets the icon directory."""
    varibale = value


class CustomFrame(ctk.CTkFrame):
    """Custom frame with center at the center."""
    def __init__(self, master=None, theme="dark", **kwargs):
        ctk.set_appearance_mode(theme.capitalize())  # Set the appearance mode (light/dark)
        super().__init__(master, fg_color="white", **kwargs)
        self.place_forget()

    def show_frame(self):
        self.place(relx=0.5, rely=0.5, anchor="center")

    def hide_frame(self):
        self.place_forget()
        

class OnlineHomemadeDialog(tk.Toplevel):
    def __init__(self, parent, callback=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.title("Online or Homemade")
        self.callback = callback  # Function to call when a button is clicked

        ok_button = tk.Button(self, text="Online", command=self.online)
        ok_button.pack(pady=10)

        cancel_button = tk.Button(self, text="Homemade", command=self.homemade)
        cancel_button.pack(pady=10)

        self.protocol("WM_DELETE_WINDOW", self.on_window_closing)

    def online(self):
        if self.callback:
            self.callback(self, "Online")
        self.destroy()  # Close the secondary window

    def homemade(self):
        if self.callback:
            self.callback(self, "Homemade")
        self.destroy()  # Close the secondary window

    def on_window_closing(self):
        self.callback(self, "INVALID")  # Call the callback with None
