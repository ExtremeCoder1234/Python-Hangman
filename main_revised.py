import tkinter as tk
import os
from PIL import ImageTk, Image
import easygui
import random

# I used AI to clean this up a bit and fix some errors, I implemented most of the ideas myself, but AI helped with the code structure and some of the logic.
# AI also added some error handling for file not found errors and empty files.
# Copyright (C) 2025 Jordan Al-Fanek, all rights reserved.
# Copyright TWT Pictures (C) Tech With Tim, all rights reserved.
# Copyright Homemade Pictures (C) 2025 Jordan Al-Fanek, all rights reserved.

# Constants
WIDTH = 500
HEIGHT = 500
LETTERS_PER_LINE = 13
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
WORDS_FILE = "words.txt"
IMAGE_DIR = "C:/Users/jorda/Projects/Code/Python/Hangman/assets"
ICON_PATH = "C:/Users/jorda/Projects/Code/Python/Hangman/assets/logo.ico"
MAX_WRONG_GUESSES = 6

fancy_or_homemade = easygui.ynbox("Do you want to use a homemade or online found picture?", "Picture Choice", ("Online", "Homemade"))
if fancy_or_homemade:
    IMAGE_DIR = "C:/Users/jorda/Projects/Code/Python/Hangman/assets/TWT Pictures"
else:
    IMAGE_DIR = "C:/Users/jorda/Projects/Code/Python/Hangman/assets/Homemade Pictures"
    
def get_word_from_text_file(file_path):
    """Gets a random word from a text file."""
    try:
        with open(file_path, "r") as words_file:
            words = [word.strip().upper() for word in words_file.readlines() if word.strip()]
            if not words:
                raise ValueError("The file is empty")
            return random.choice(words)
    except FileNotFoundError:
        tk.messagebox.showwarning("File Error", f"Error: Words file '{file_path}' not found.")
        exit()

def get_word_from_user():
    """Gets a word from the user via a dialog."""
    word = tk.simpledialog.askstring("Word", "Please enter a word for the player to guess").upper().strip()
    if not word or any(char in word for char in "!.\"?'@;"):
        tk.messagebox.showwarning("Invalid input. Please enter a valid word.", "Input Error")
        exit()
    return word

def get_player_count():
    """Gets the number of players and returns the word to guess."""
    players = tk.simpledialog.askinteger("Players", "How many players are playing?")
    if players is None or players <= 0:
        exit()
    return get_word_from_text_file(WORDS_FILE) if players == 1 else get_word_from_user()

class LetterButton:
    """Represents a letter button."""
    def __init__(self, root, letter, position, word_class):
        self.word_class = word_class
        self.letter = letter
        self.button = tk.Button(root, text=letter, font=("Arial", 10), command=self.check_and_destroy)
        self.button.place(x=30 * (position % LETTERS_PER_LINE + 1), y=200 + 50 * (position // LETTERS_PER_LINE))

    def check_and_destroy(self):
        """Checks the letter and destroys the button."""
        if self.word_class.check_letter(self.letter):
            self.button.destroy()
        else:
            self.word_class.wrong_guess()
            self.button.destroy()

class WordToGuess:
    """Represents the word to guess."""
    def __init__(self, root, word):
        self.root = root
        self.word = word
        self.guessed_word = [char if char == " " else "-" for char in word]
        self.wrong_guesses = 0
        self.word_label = tk.Label(root, text="".join(self.guessed_word), font=("Arial", 30), bg="white", wraplength=WIDTH - 20)
        self.word_label.place(x=WIDTH / 2 - self.word_label.winfo_reqwidth() / 2, y=50)

    def check_letter(self, letter):
        """Checks if the letter is in the word and updates the display."""
        found = False
        for i, char in enumerate(self.word):
            if char.upper() == letter.upper():
                self.guessed_word[i] = char
                found = True
        if found:
            self.update_display()
            if "-" not in self.guessed_word:
                self.game_over(True)
        return found

    def wrong_guess(self):
        """Handles a wrong guess."""
        self.wrong_guesses += 1
        update_image(self.root, self.wrong_guesses)
        if self.wrong_guesses >= MAX_WRONG_GUESSES:
            self.game_over(False)

    def update_display(self):
        """Updates the displayed word."""
        self.word_label.config(text="".join(self.guessed_word))

    def game_over(self, win):
        """Handles game over logic."""
        message = "Congrats, you win!" if win else "Sorry, you lost."
        if easygui.ynbox(f"{message}\nPlay again?", "Game Over"):
            self.reset_game()
        else:
            self.root.quit()

    def reset_game(self):
        """Resets the game."""
        self.word = get_player_count()
        self.guessed_word = [char if char == " " else "-" for char in self.word]
        self.wrong_guesses = 0
        self.update_display()
        update_image(self.root, 0)
        setup_ui(self.root, self.word, self)

class HangmanGame(tk.Tk):
    """Main Hangman game class."""
    def __init__(self):
        super().__init__()
        self.title("Hangman")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.resizable(False, False)
        self.configure(bg="white")
        self.iconbitmap(ICON_PATH)
        self.word_to_guess = WordToGuess(self, get_player_count())
        update_image(self, 0)
        setup_ui(self, self.word_to_guess.word, self.word_to_guess) #pass self

def update_image(root, guess_count):
    """Updates the hangman image."""
    try:
        image = Image.open(os.path.join(IMAGE_DIR, f"hangman{guess_count}.png"))
        resize_image = image.resize((200, 190))
        root_image = ImageTk.PhotoImage(resize_image)
        image_label = tk.Label(root, image=root_image, borderwidth=0, highlightthickness=0)
        image_label.image = root_image
        image_label.place(x=0, y=0)
    except FileNotFoundError:
        tk.messagebox.showwarning(f"Error: Hangman image 'hangman{guess_count}.png' not found.", "Image Error")
        exit()

def setup_ui(root, word, word_class): #add root as parameter
    """Sets up the UI with letter buttons."""
    for i, letter in enumerate(ALPHABET):
        LetterButton(root, letter, i, word_class)

if __name__ == "__main__":
    root = HangmanGame()
    print(help(setup_ui))  # Print the help message for the root window
    root.mainloop()