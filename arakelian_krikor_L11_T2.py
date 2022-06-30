import random
from tkinter import *


class Hangman:
    def __init__(self, word_file):
        self.word = ""
        self.word_to_show = []
        self.tries_remaining = 6
        self.word_file = word_file

    def new_word(self):
        self.tries_remaining = 6
        self.word = ""
        self.word_to_show = []
        self.word = random.choice(self.word_file)
        for letter in self.word:
            if letter == self.word[0] or letter == self.word[-1]:
                self.word_to_show.append(letter)
            else:
                self.word_to_show.append("_")

    def letter_in_word(self, letter):
        if letter in self.word:
            for idx in range(len(self.word)):
                if self.word[idx] == letter:
                    self.word_to_show[idx] = letter
        else:
            self.tries_remaining -= 1

    def word_to_print(self):
        return "".join(self.word_to_show)

    def have_won(self):
        return "_" not in self.word_to_show and self.tries_remaining > 0

    def have_lost(self):
        return self.tries_remaining == 0


def new_game(word):
    word.new_word()
    end_frame()
    create_keys()
    return word


def funcs_for_keys(x):
    hangman.letter_in_word(x)
    word_on_screen.configure(text=hangman.word_to_print())
    mistake_counter.configure(text=f"Tries remaining:{hangman.tries_remaining}")
    end_game()


# Keyboard generator
def create_keys():
    col = 0
    row = 0
    counter = 0
    for i in range(65, 91):
        buttons = Button(frame_keys, text=chr(i), width=2, height=1, font=MAIN_FONT, padx=8, pady=4, relief=RAISED,
                         background=BUTTON_COLOR, foreground=TEXT_COLOR, command=lambda x=chr(i): funcs_for_keys(x))
        buttons.grid(column=col, row=row, padx=8, pady=4)
        col += 1
        counter += 1
        if counter == 9:
            col = 0
            row += 1
            counter = 0


def end_frame():
    global frame_keys
    frame_keys.destroy()
    frame_keys = Frame(main_window, width=mw_width, height=mw_height / 2, background=MAIN_COLOR)
    frame_keys.grid(columnspan=10, rowspan=4, sticky="we")


def end_game():
    if hangman.have_won():
        end_frame()
        end_text = Label(frame_keys, text="Congratulations, you win!", font=MAIN_FONT, background=MAIN_COLOR,
                         foreground=TEXT_COLOR, justify=CENTER)
        end_text.place(relx=0.5, rely=0.5, anchor=CENTER)
    if hangman.have_lost():
        end_frame()
        end_text = Label(frame_keys, text="GAME OVER", font=MAIN_FONT, background=MAIN_COLOR,
                         foreground=TEXT_COLOR, justify=CENTER)
        end_text.place(relx=0.5, rely=0.5, anchor=CENTER)


# Open text file and read contents
with open("words.txt") as file:
    words = [word.strip("\n") for word in file.readlines()]

# Universal attributes:
MAIN_FONT = 'Verdana'
MAIN_COLOR = "#49809E"
BUTTON_COLOR = "#83C7EB"
TEXT_COLOR = "#4A3520"

# Main window and frames of app
main_window = Tk()
main_window.title("Hangman Game")
main_window.iconbitmap("./hangman.ico")
main_window.configure(background=MAIN_COLOR)
mw_height = 360
mw_width = 595
frame_word = Frame(main_window, width=mw_width, height=mw_height / 3, background=MAIN_COLOR)
frame_word.grid(columnspan=10, rowspan=1)
frame_buttons = Frame(main_window, width=mw_width, height=mw_height / 3, background=MAIN_COLOR)
frame_buttons.grid(columnspan=10, rowspan=1)
frame_keys = Frame(main_window, width=mw_width, height=mw_height / 3, background=MAIN_COLOR)
frame_keys.grid(columnspan=10, rowspan=3, sticky="swe")

# Center main window on the screen
screen_w = main_window.winfo_screenwidth()
screen_h = main_window.winfo_screenheight()
scr_center_x = int(screen_w / 2 - mw_width / 2)
scr_center_y = int(screen_h / 2 - mw_height / 2)
main_window.geometry(f'{mw_width}x{mw_height}+{scr_center_x}+{scr_center_y}')

# Prevent resizing of app window
main_window.resizable(False, False)

# Word, mistake counter, new game button and keys
hangman = Hangman(words)
hangman.new_word()
word_on_screen = Label(frame_word, text=hangman.word_to_print(), foreground=TEXT_COLOR, justify=CENTER,
                       font=MAIN_FONT, height=2, pady=5, background=MAIN_COLOR)
word_on_screen.place(relx=0.5, rely=0.5, anchor=CENTER)

mistake_counter = Label(frame_buttons, text=f"Tries remaining: {hangman.tries_remaining}", font=MAIN_FONT,
                        background=MAIN_COLOR, foreground=TEXT_COLOR)
mistake_counter.grid(column=2, row=0, sticky="e", padx=4, pady=4)

new_game_button = Button(frame_buttons, text="New Game",
                         command=lambda: [new_game(hangman), word_on_screen.configure(
                             text=hangman.word_to_print()),
                                          mistake_counter.configure(
                                              text=f"Tries remaining: {hangman.tries_remaining}")],
                         font=MAIN_FONT, padx=4, pady=4, relief=RAISED, background=BUTTON_COLOR, foreground=TEXT_COLOR)
new_game_button.grid(column=0, row=0, sticky="w", padx=30, pady=4)

create_keys()

main_window.mainloop()
