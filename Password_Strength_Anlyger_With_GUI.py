import tkinter as tk
from tkinter import messagebox
from zxcvbn import zxcvbn
import itertools
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import nltk

# Download required NLTK resources (only first time)
nltk.download('wordnet')
nltk.download('omw-1.4')

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()


# ---------------- PASSWORD STRENGTH CHECK ---------------- #
def check_password_strength():
    password = password_entry.get()
    if not password:
        messagebox.showwarning("Input Error", "Please enter a password")
        return

    result = zxcvbn(password)
    score = result['score']
    feedback = result['feedback']

    strength_labels = ["Very Weak", "Weak", "Medium", "Strong", "Very Strong"]
    strength = strength_labels[score]

    strength_label.config(text=f"Strength: {strength}", fg="green" if score >= 3 else "red")

    feedback_text = "\n".join(feedback['suggestions'])
    if feedback['warning']:
        feedback_text += f"\nWarning: {feedback['warning']}"
    feedback_label.config(text=f"Suggestions:\n{feedback_text}")


# ---------------- WORDLIST GENERATION WITH NLTK ---------------- #
def expand_with_nltk(word):
    """ Expand a word with NLTK: lemmatization + synonyms """
    variants = set()
    variants.add(lemmatizer.lemmatize(word))

    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            variants.add(lemma.name().lower())

    return variants


def generate_wordlist():
    words = wordlist_entry.get().split(',')
    words = [w.strip() for w in words if w.strip()]

    if not words:
        messagebox.showwarning("Input Error", "Please enter at least one word")
        return

    leetspeak = {'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5'}
    years = ['1990', '2000', '2020', '2023', '2025']
    wordlist = set()

    for word in words:
        wordlist.add(word)

        for expanded in expand_with_nltk(word):
            wordlist.add(expanded)

        leet_word = ''.join(leetspeak.get(c.lower(), c) for c in word)
        wordlist.add(leet_word)

        for year in years:
            wordlist.add(word + year)

    for w1, w2 in itertools.permutations(words, 2):
        wordlist.add(w1 + w2)

    # Save to file
    with open("custom_wordlist.txt", "w") as f:
        for item in sorted(wordlist):
            f.write(item + "\n")

    # Show inside GUI preview
    preview_box.delete(1.0, tk.END)
    preview_box.insert(tk.END, "\n".join(sorted(wordlist)))

    messagebox.showinfo("Success", "Wordlist generated and saved as custom_wordlist.txt")


# ---------------- TKINTER GUI ---------------- #
root = tk.Tk()
root.title("Password Strength Analyzer & Wordlist Generator")
root.geometry("550x600")

# Password Section
tk.Label(root, text="Enter Password:").pack(pady=5)
password_entry = tk.Entry(root, show="*", width=40)
password_entry.pack(pady=5)
tk.Button(root, text="Check Strength", command=check_password_strength).pack(pady=5)

strength_label = tk.Label(root, text="Strength: ", font=("Arial", 12, "bold"))
strength_label.pack(pady=5)

feedback_label = tk.Label(root, text="", wraplength=500, justify="left", fg="blue")
feedback_label.pack(pady=5)

# Wordlist Section
tk.Label(root, text="Enter Words (comma separated):").pack(pady=5)
wordlist_entry = tk.Entry(root, width=40)
wordlist_entry.pack(pady=5)
tk.Button(root, text="Generate & Save Wordlist", command=generate_wordlist).pack(pady=5)

# Preview Box
tk.Label(root, text="Generated Wordlist Preview:").pack(pady=5)
preview_box = tk.Text(root, height=15, width=60, wrap="word", bg="#f4f4f4")
preview_box.pack(pady=5)

# Run App
root.mainloop()
