import tkinter as tk

root = tk.Tk()



frame = tk.Frame(root, borderwidth=5, relief=tk.RAISED, highlightbackground="black", highlightthickness=3)
frame.place_forget()  # Initially hide the frame (using place_forget)

def show_frame():
    frame.place(x=50, y=50, width=200, height=100)  # Place the frame with specific coordinates and size

def hide_frame():
    frame.place_forget()

show_button = tk.Button(root, text="Show Frame", command=show_frame)
show_button.place(x=1080 - 10, y=10) # Place the show button

hide_button = tk.Button(frame, text="Hide Frame", command=hide_frame)
hide_button.place(x=10, y=10) # Place the hide button within the frame

root.mainloop()