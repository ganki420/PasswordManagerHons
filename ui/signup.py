import tkinter as tk
from tkinter import messagebox
from auth import register_user
from theme import theme_manager
import re

class SignUpPage(tk.Frame): # signup page
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller # refers to the main app

        # sets background and foreground colours from the them
        self.configure(bg=theme_manager.get_colors()["bg"])
        self.bg_color = theme_manager.get_colors()["bg"]
        self.fg_color = theme_manager.get_colors()["fg"]

        # singup label
        tk.Label(self, text="Sign Up", font=("Arial", 20, "bold"), bg=self.bg_color, fg=self.fg_color).pack(pady=20) 

        #username lable and input
        tk.Label(self, text="Username:", bg=self.bg_color, fg=self.fg_color).pack()
        self.username_entry = tk.Entry(self) # field for username
        self.username_entry.pack(pady=5) 

        #password label and input
        tk.Label(self, text="Password:", bg=self.bg_color, fg=self.fg_color).pack()
        self.password_entry = tk.Entry(self, show="*") # field for password
        self.password_entry.pack(pady=5) 

        self.show_password_var = tk.BooleanVar() # variable to show and hide passwords
        tk.Checkbutton(self, text="Show Password", variable=self.show_password_var,
                       command=lambda: self.password_entry.config(show="" if self.show_password_var.get() else "*"), # toggles the masking
                       bg=self.bg_color, fg=self.fg_color, selectcolor=self.bg_color).pack()
        
        # password strength label
        self.strength_label = tk.Label(self, text="", font=("Arial", 10, "bold"), bg=self.bg_color, fg=self.fg_color)
        self.strength_label.pack(pady=(5, 0))

        self.password_entry.bind("<KeyRelease>", self.update_strength) # calls strength check on each keystroke

        # confirms password label and entry
        tk.Label(self, text="Confirm Password:", bg=self.bg_color, fg=self.fg_color).pack()
        self.confirm_entry = tk.Entry(self, show="*") # confirms password field
        self.confirm_entry.pack(pady=5)

        #register and back buttons
        tk.Button(self, text="Register", command=self.register, bg=theme_manager.get_colors()["button_bg"]).pack(pady=10) # submit the form
        tk.Button(self, text="Back to Login", command=lambda: controller.show_page("LoginPage"), bg=theme_manager.get_colors()["button_bg"]).pack() # go back

    def update_strength(self, event): # function to check password strength
        password = self.password_entry.get() # get typed password
        length = len(password) >= 8
        lower = re.search(r"[a-z]", password)
        upper = re.search(r"[A-Z]", password)
        digit = re.search(r"[0-9]", password)
        special = re.search(r"[^a-zA-Z0-9]", password)
        score = sum(bool(x) for x in [length, lower, upper, digit, special]) # score from 0-5

        # sets strength label text and colour
        if score <= 2:
            strength, color = "Weak", "red"
        elif score in [3, 4]:
            strength, color = "Medium", "orange"
        else:
            strength, color = "Strong", "green"

        self.strength_label.config(text=f"Strength: {strength}", fg=color) # updating the label

    def register(self): # function to register a new user
        username = self.username_entry.get() # get username
        password = self.password_entry.get() # gets password
        confirm_password = self.confirm_entry.get() # get confirmed password

        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "All fields are required.") # checking for empty fields
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.") # checking if passwords match
            return

        success = register_user(username, password) # try to register new user
        if success:
            messagebox.showinfo("Success", "Account created successfully!") # show success message
            self.controller.show_page("LoginPage") # go to login page
        else:
            messagebox.showerror("Error", "Username already exists.") # show error if username is taken
