import tkinter as tk
import random
import time

# Sample words for typing
words = ['horse', 'apple', 'morning', 'keyboard', 'python', 'application', 'school', 'university', 'grand', 'basic']

class TypingTrainer:
    def __init__(self, master):
        self.master = master
        self.master.title('Typing Trainer')
        
        # Starting time
        self.start_time = None

        self.word_label = tk.Label(master, font=("Arial", 12))
        self.word_label.pack()

        self.entry = tk.Entry(master, font=("Arial", 12))
        self.entry.pack()
        self.entry.bind('<Return>', self.check_word)

        self.result_label = tk.Label(master, font=("Arial", 12))
        self.result_label.pack()

        self.new_word()

    def new_word(self):
        self.random_word = random.choice(words)
        self.word_label.config(text=f"Type the word: {self.random_word}")
        self.entry.delete(0, tk.END)
        self.start_time = time.time()

    def check_word(self, event):
        if self.entry.get() == self.random_word:
            end_time = time.time()
            typing_speed = 60 / (end_time - self.start_time)
            self.result_label.config(text=f"Correct! Your speed was {typing_speed:.2f} words per minute.")
        else:
            self.result_label.config(text="Incorrect, try again.")
        self.new_word()


if __name__ == "__main__":
    root = tk.Tk()
    trainer = TypingTrainer(root)
    root.mainloop()
