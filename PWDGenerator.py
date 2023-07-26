import random
import string
import pyperclip
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("(GUI) Password Generator")

        # Create a custom style for modern dark mode
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(".", foreground="white", background="gray15", font=("Roboto", 12))
        self.style.configure("TLabel", foreground="white", background="gray15", font=("Roboto", 12))
        self.style.configure("TEntry", foreground="white", background="gray25", fieldbackground="gray30", font=("Roboto", 12))
        self.style.map("TEntry", background=[("active", "gray30")])
        self.style.configure("TCheckbutton", foreground="white", background="gray15", font=("Roboto", 12))

        # Set the main window background to a dark gray
        self.root.configure(background="gray15")

        # Create a style for the buttons when hovering
        self.style.map("TButton", background=[("active", "gray25")], foreground=[("active", "white")])

        # Create a style for the options when hovering
        self.style.map("TCheckbutton", background=[("active", "gray20")])

        # Add icons to buttons
        self.generate_icon = Image.open("./key.png")
        self.generate_icon = self.generate_icon.resize((20, 20), Image.LANCZOS)  # Use Image.LANCZOS
        self.generate_icon = ImageTk.PhotoImage(self.generate_icon)

        self.copy_icon = Image.open("./clipboard.png")
        self.copy_icon = self.copy_icon.resize((20, 20), Image.LANCZOS)  # Use Image.LANCZOS
        self.copy_icon = ImageTk.PhotoImage(self.copy_icon)


        self.password_var = tk.StringVar()
        self.password_length_var = tk.IntVar(value=12)
        self.use_uppercase_var = tk.BooleanVar(value=True)
        self.use_lowercase_var = tk.BooleanVar(value=True)
        self.use_digits_var = tk.BooleanVar(value=True)
        self.use_special_var = tk.BooleanVar(value=False)
        self.allow_repeating_var = tk.BooleanVar(value=False)
        self.exclude_ambiguous_var = tk.BooleanVar(value=False)

        self.create_widgets()
        
        self.password_history = []
        self.load_password_history()

    def create_widgets(self):
        password_label = ttk.Label(self.root, text="Password:")
        password_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        password_entry = ttk.Entry(self.root, textvariable=self.password_var, state='readonly')
        password_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

        password_length_label = ttk.Label(self.root, text="Length:")
        password_length_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

        password_length_entry = ttk.Entry(self.root, textvariable=self.password_length_var)
        password_length_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

        uppercase_checkbox = ttk.Checkbutton(self.root, text="Use Uppercase", variable=self.use_uppercase_var)
        uppercase_checkbox.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

        lowercase_checkbox = ttk.Checkbutton(self.root, text="Use Lowercase", variable=self.use_lowercase_var)
        lowercase_checkbox.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

        digits_checkbox = ttk.Checkbutton(self.root, text="Numbers", variable=self.use_digits_var)
        digits_checkbox.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

        special_checkbox = ttk.Checkbutton(self.root, text="Special Characters", variable=self.use_special_var)
        special_checkbox.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)

        allow_repeating_checkbox = ttk.Checkbutton(self.root, text="Allow Repeating Characters", variable=self.allow_repeating_var)
        allow_repeating_checkbox.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)

        exclude_ambiguous_checkbox = ttk.Checkbutton(self.root, text="Exclude Ambiguous Characters", variable=self.exclude_ambiguous_var)
        exclude_ambiguous_checkbox.grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)

        generate_button = ttk.Button(self.root, text="Generate password", image=self.generate_icon, compound=tk.LEFT, command=self.generate_password)
        generate_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        copy_button = ttk.Button(self.root, text="Copy to Clipboard", image=self.copy_icon, compound=tk.LEFT, command=self.copy_to_clipboard)
        copy_button.grid(row=6, column=0, columnspan=2, padx=10, pady=5)
        
        info_label = ttk.Label(self.root, text="Note: The password will be automatically copied to the clipboard when generated.")
        info_label.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

    def generate_password(self):
        password_length = self.password_length_var.get()
        use_uppercase = self.use_uppercase_var.get()
        use_lowercase = self.use_lowercase_var.get()
        use_digits = self.use_digits_var.get()
        use_special = self.use_special_var.get()
        allow_repeating = self.allow_repeating_var.get()
        exclude_ambiguous = self.exclude_ambiguous_var.get()

        characters = ''
        if use_uppercase:
            characters += string.ascii_uppercase
        if use_lowercase:
            characters += string.ascii_lowercase
        if use_digits:
            characters += string.digits
        if use_special:
            characters += string.punctuation

        if not characters:
            messagebox.showerror("Error", "You must select at least one character type.")
            return

        if not allow_repeating:
            characters = ''.join(set(characters))

        if exclude_ambiguous:
            ambiguous_characters = "l1I0O"
            characters = ''.join(c for c in characters if c not in ambiguous_characters)

        if len(characters) == 0:
            messagebox.showerror("Error", "The selected options result in an empty character set.")
            return
        elif password_length > 256:
            messagebox.showerror("Error", "Password length cannot exceed 256 characters.")
            return

        password = ''.join(random.choice(characters) for _ in range(password_length))
        self.password_var.set(password)
        self.password_history.append(password)
        self.save_password_history()
        
        strength = self.evaluate_strength(password)
        messagebox.showinfo("Strength", f"Password Strength: {strength}")
        
        pyperclip.copy(password)
        messagebox.showinfo("Success", "Password generated and copied successfully!")
    
    def save_password_history(self):
        with open("pwd_history.txt", "w") as file:
            for password in self.password_history:
                file.write(password + "\n")
        
    def load_password_history(self):
        try:
            with open("pwd_history.txt", "r") as file:
                self.password_history = file.read().splitlines()
        except FileNotFoundError:
            # If the file is not found, no need to raise an error; the history will remain empty
            pass

    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Success", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No password generated yet!")

    def evaluate_strength(self, password):
        # Evaluate password strength based on length and character types
        length_score = min(1, len(password) / 12)  # Normalized length score between 0 and 1
        uppercase_score = 1 if any(c.isupper() for c in password) else 0
        lowercase_score = 1 if any(c.islower() for c in password) else 0
        digit_score = 1 if any(c.isdigit() for c in password) else 0
        special_score = 1 if any(c for c in password if c in string.punctuation) else 0

        # Total strength score (normalized between 0 and 1)
        total_score = (length_score + uppercase_score + lowercase_score + digit_score + special_score) / 5

        if total_score >= 0.8:
            return "Strong"
        elif total_score >= 0.5:
            return "Medium"
        else:
            return "Weak"

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()