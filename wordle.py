import tkinter as tk
from tkinter import messagebox
import random
import os


ROWS, COLS = 6, 5
WORDLIST_FILE = 'all_words.txt'

if not os.path.exists(WORDLIST_FILE):
    raise FileNotFoundError(f"Could not find {WORDLIST_FILE}")
with open(WORDLIST_FILE) as f:
    all_words = [w.strip().upper() for w in f if len(w.strip()) == 5]

root = tk.Tk()
root.title("Wordle Pattern Maker")


buttons = [[None]*COLS for _ in range(ROWS)]
clicked = [[False]*COLS for _ in range(ROWS)]

def toggle_cell(r, c):
    clicked[r][c] = not clicked[r][c]
    color = 'orange' if clicked[r][c] else 'light grey'
    buttons[r][c].config(bg=color)

for r in range(ROWS):
    for c in range(COLS):
        btn = tk.Button(root,
                        width=6, height=3,
                        bg='light grey',
                        command=lambda r=r, c=c: toggle_cell(r, c))
        btn.grid(row=r, column=c, padx=2, pady=2)
        buttons[r][c] = btn

entry = tk.Entry(root, font=('Arial', 14))
entry.grid(row=ROWS, column=0, columnspan=COLS-1, pady=10, sticky='we')


def reset_grid():
    entry.delete(0, tk.END)
    for r in range(ROWS):
        for c in range(COLS):
            clicked[r][c] = False
            buttons[r][c].config(bg='light grey', text='')

def confirm():
    answer = entry.get().strip().upper()
    if len(answer) != 5 or answer not in all_words:
        messagebox.showerror("Invalid Entry",
                             "Please enter a valid 5-letter Wordle word.")
        return

    guesses = []

    for r in range(ROWS):
        pattern = clicked[r]
        candidates = []
        for w in all_words:
            valid = True
            for c in range(COLS):
                if pattern[c]:
                    if w[c] != answer[c]:
                        valid = False
                        break
                else:
                    if answer[c] in w:
                        valid = False
                        break
            if valid:
                candidates.append(w)

        if not candidates:
            messagebox.showinfo("Impossible",
                                "This combination is impossible.")
            reset_grid()
            return
        guesses.append(random.choice(candidates))
    for r, guess in enumerate(guesses):
        for c, letter in enumerate(guess):
            buttons[r][c].config(text=letter, fg='white', font=('Arial', 16, 'bold'))

confirm_btn = tk.Button(root, text="Confirm", command=confirm,
                        bg='sky blue', font=('Arial', 12, 'bold'))
confirm_btn.grid(row=ROWS, column=COLS-1, pady=10)

root.mainloop()