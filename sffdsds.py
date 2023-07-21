import tkinter as tk
from tkinter import messagebox

def predict_spam():
    message = entry.get()
    if message:
        message_counts = vectorizer.transform([message])
        prediction = classifier.predict(message_counts)
        if prediction == 1:
            messagebox.showinfo("Prediction", "This message is likely spam.")
        else:
            messagebox.showinfo("Prediction", "This message is likely not spam.")
    else:
        messagebox.showwarning("No Input", "Please enter a message to predict.")

# Create the main window
window = tk.Tk()
window.title("Spam Detection System")

# Create a text entry field
entry = tk.Entry(window, width=50)
entry.pack()

# Create a prediction button
predict_button = tk.Button(window, text="Predict", command=predict_spam)
predict_button.pack()

# Run the application
window.mainloop()
