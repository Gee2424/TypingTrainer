import tkinter as tk
from tkinter import ttk
import random
import time

class TypingTrainer:
    def __init__(self, master):
        self.master = master
        self.master.title('Typing Trainer')

        # Sample words for typing
        self.words = ['horse', 'apple', 'morning', 'keyboard', 'python', 'application', 'school', 'university', 'grand', 'basic']
        random.shuffle(self.words)
        self.current_word = None
        self.start_time = None
        self.total_time = 0
        self.words_typed = 0
        self.errors = 0

        self.word_label = ttk.Label(master, font=("Arial", 14))
        self.word_label.pack(pady=20)

        self.entry = ttk.Entry(master, font=("Arial", 14))
        self.entry.pack(pady=10)
        self.entry.bind('<Return>', self.check_word)

        self.result_label = ttk.Label(master, font=("Arial", 12))
        self.result_label.pack(pady=10)

        self.progress_label = ttk.Label(master, text="Your Progress:", font=("Arial", 12))
        self.progress_label.pack()
        self.progress_bar = ttk.Progressbar(master, length=400)
        self.progress_bar.pack()

        self.tip_label = ttk.Label(master, text="Tip: Keep your fingers on the home row.", font=("Arial", 10), wraplength=500)
        self.tip_label.pack(pady=10)

        self.new_word()

    def new_word(self):
        if not self.words:
            self.result_label.config(text="Congratulations! You have completed all words.")
            self.entry.unbind('<Return>')  # Disable typing when all words are completed
            return

        self.current_word = self.words.pop()
        self.word_label.config(text=f"Type the word: {self.current_word}")
        self.entry.delete(0, tk.END)
        self.start_time = time.time()

    def check_word(self, event):
        typed_word = self.entry.get()
        if typed_word == self.current_word:
            end_time = time.time()
            elapsed_time = end_time - self.start_time
            self.total_time += elapsed_time
            self.words_typed += 1
            typing_speed_wps = self.words_typed / self.total_time  # Words per second
            typing_speed_lps = len(typed_word) / self.total_time  # Letters per second
            accuracy = (self.words_typed / (self.words_typed + self.errors)) * 100

            self.result_label.config(text=f"Correct! Your speed: {typing_speed_wps:.2f} words per second | {typing_speed_lps:.2f} letters per second | Accuracy: {accuracy:.2f}%")
            self.progress_bar['value'] = (self.words_typed / len(self.words)) * 100
            self.update_tip()
        else:
            self.result_label.config(text="Incorrect, try again.")
            self.errors += 1

        self.new_word()

    def update_tip(self):
        tips = [
            "Tip: Keep your fingers on the home row.",
            "Tip: Use all your fingers, not just two or three.",
            "Tip: Try not to look at the keyboard, your fingers know where the keys are.",
            "Tip: Practice regularly, consistency is key."
        ]
        self.tip_label.config(text=random.choice(tips))

if __name__ == "__main__":
    root = tk.Tk()
    trainer = TypingTrainer(root)
    root.mainloop()
