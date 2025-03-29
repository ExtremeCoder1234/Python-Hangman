from tkinter import *
import tkinter as tk
import os
from PIL import ImageTk, Image
from tkinter.ttk import *
import easygui
import time
import random
import bg_rem


os.chdir("C:/Users/jorda/Projects/Code/Python/Hangman")

root = tk.Tk()
root.title("Hangman")
root.configure(bg="white")
WIDTH = 500
HEIGHT = 500
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(False, False)
letters_per_line = 13
abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
message = ""
# Load the image for the buttons
root.iconbitmap("logo.ico")

def get_word_from_text_file(file):
    with open(file, "r") as f:
        words = f.readlines()
        if len(words) <= 0:
            raise ValueError("The file is empty")
        else:
            return random.choice(words)


def get_word_from_user():
    msg = tk.simpledialog.askstring("Word", "Please enter a word for the player to guess", parent=root).upper()
    if msg == None or msg == "" or "!" in msg or "." in msg or "?" in msg or "@" in msg or ";" in msg or "\"" in msg or "'" in msg or "@" in msg or "@" in msg or "@" in msg or "@" in msg:  # If the user presses cancel or the input is empty
        root.quit()
    else: 
        return msg





def check_player_count():
    global message
    players = tk.simpledialog.askinteger("Players", "How many players are playing?", parent=root)
    if players == None or players <= 0:
        root.quit()
    elif players == 1:
        message = str(get_word_from_text_file("words.txt")).upper().strip()
    else:
        message = str(get_word_from_user()).upper().strip()
        
    print(message)


#----------------------------------------------------------------------------------------------------


check_player_count()


"""Create a class for the letter buttons

Raises:
    ValueError: Invald position for button
"""
class LetterButton:

    def __init__(self, root, letter, pos, word_class):
        self.word_class = word_class
        self.pos = pos
        self.letter = letter
        self.root = root
        self.button = tk.Button(root, text=self.letter, compound="center", font=("Arial", 10), relief="raised", command=self.check_and_destroy)
        self.button.grid(column=0, row=2)
        
        if pos <= letters_per_line:
            self.line = 1
        elif letters_per_line < pos < letters_per_line * 2 + 1: 
            self.line = 2
        else:
            raise ValueError("Invalid position for button")
        

        if self.line == 1:
            self.button.place(x=30 * (pos + 1), y=200)
        elif self.line == 2:
            self.button.place(x=30 * ((pos - letters_per_line) + 1), y=250)


    def check_and_destroy(self):
        found = False
        for i in range(len(self.word_class.word)):
            if self.word_class.word[i].upper() == self.letter.upper():
                self.word_class.update_word_dashes(i)
                found = True
            
        if not found:
            WORD_CLASS.wrong_guesses += 1
            if WORD_CLASS.wrong_guesses == 6:
                update_image()
                WORD_CLASS.check_win(False)
                
            update_image()
            
        self.button.destroy()
            
        

# Create a class for the word to guess


class WordToGuess:
    def __init__(self, root, word):
        """The function for the word to guess

        Arguments:
            root {tk.Tk()} -- The root window for the application
            word {string} -- The word to be guessed by the player
        """
        self.word = word
        self.wrong_guesses = 0
        self.strWithSpaces = ""
        for i in range(len(word)):
            if word[i] != " ":
                self.strWithSpaces += "-"
            else:
                self.strWithSpaces += " "

        self.word_str = StringVar(root, self.strWithSpaces)
        self.new_word_str = StringVar(root, "")
        self.root = root
        self.word_label = None 
                
        self.reset_label()
        
    def update_word_dashes(self, indexOfReplacment):
        word_list = list(self.word_str.get())
        word_list[indexOfReplacment] = self.word[indexOfReplacment]
        self.word_str.set("".join(word_list))
        self.reset_label()
        if "-" not in self.word_str.get():
            self.check_win(True)
        
    def check_win(self, msg_good):
        play_again = None
        msg = ""
        if msg_good:
            msg = "Congrats,\nDo you want to play again?"
        else:
            msg = "Sorry, you lost.\nDo you want to play again?"
        play_again = easygui.ynbox(msg=msg, title='')
        if play_again:
            self.reset_game()
        else:
            self.root.quit()
            
    def reset_label(self):
        if self.word_label != None:
            self.word_label.destroy()
        self.word_label = tk.Label(self.root, text=self.word_str.get(), font=("Arial", 30), pady=9, background="white")
        self.word_label.grid(row=0, column=0, rowspan=1, columnspan=4)
        self.root.update()
        self.word_label.place(x=(self.root.winfo_width() / 2) - (self.word_label.winfo_width() / 2), y=50)

    def reset_game(self):
        self.word_label.destroy()
        self.wrong_guesses = 0
        check_player_count()
        self.word = message
        self.word_str.set("-" * len(self.word))  # Reset the word_str variable
        self.wrong_guesses = 0
        self.reset_label()
        setup_ui(message)
        

class CustomFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(borderwidth=5, relief=tk.RAISED, highlightbackground="black", highlightthickness=3)
        self.place(x=0, y=0, width=WIDTH, height=HEIGHT)  # Set the size of the frame



WORD_CLASS = WordToGuess(root, message)



def update_image():
    image = Image.open(f"C:/Users/jorda/Projects/Code/Python/Hangman/hangman{WORD_CLASS.wrong_guesses}.png")
 
    # Resize the image using resize() method
    resize_image = image.resize((200, 190))
 
    root.image = ImageTk.PhotoImage(resize_image)
 
    image_label = tk.Label(root, image=root.image, borderwidth=0, highlightthickness=0).place(x=0, y=0)
    root.update()

def setup_ui(message):
    for i in range(len(abc) + 1):
        if i != 26:
            LetterButton(root, abc[i], i + 1, word_class=WORD_CLASS)
            

    update_image()
    
        
    

setup_ui(message)
root.mainloop()