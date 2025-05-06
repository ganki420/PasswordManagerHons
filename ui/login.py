import tkinter as tk
import logging
from tkinter import messagebox
from auth import authenticate_user
from theme import theme_manager

class LoginPage(tk.Frame): # login page
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        colors = theme_manager.get_colors() # gets theme colours
        self.configure(bg=colors["bg"]) # sets background colour

        self.grid_rowconfigure(0, weight=1) # allows resizing
        self.grid_columnconfigure(0, weight=1)

        # login label
        tk.Label(self, text="Password Manager", font=("Arial", 18, "bold"), bg=colors["bg"], fg=colors["fg"]).grid(row=0, column=0, pady=20)

        # username field
        tk.Label(self, text="USERNAME", font=("Arial", 12, "bold"), bg=colors["bg"], fg=colors["fg"]).grid(row=1, column=0, pady=5)
        self.username_entry = tk.Entry(self, width=30, bg=colors["entry_bg"], fg=colors["entry_fg"])
        self.username_entry.grid(row=2, column=0, pady=5)

        # password field
        tk.Label(self, text="PASSWORD", font=("Arial", 12, "bold"), bg=colors["bg"], fg=colors["fg"]).grid(row=3, column=0, pady=5)
        self.password_entry = tk.Entry(self, width=30, show="*", bg=colors["entry_bg"], fg=colors["entry_fg"])
        self.password_entry.grid(row=4, column=0, pady=5)

        # show/hide password checkbox
        self.show_password_var = tk.BooleanVar()
        self.show_password_cb = tk.Checkbutton(self, text="Show Password", variable=self.show_password_var, command=self.toggle_password, bg=colors["bg"], fg=colors["fg"], selectcolor=colors["bg"])
        self.show_password_cb.grid(row=5, column=0, pady=5)

        # login, register and forgot password buttons
        tk.Button(self, text="LOGIN", font=("Arial", 12, "bold"), width=20, command=self.login, bg=colors["button_bg"]).grid(row=6, column=0, pady=5)
        tk.Button(self, text="CREATE ACCOUNT", font=("Arial", 10, "bold"), width=20, command=lambda: controller.show_page("SignUpPage"), bg=colors["button_bg"]).grid(row=7, column=0, pady=5)
        tk.Button(self, text="FORGOT PASSWORD", font=("Arial", 8), width=20, command=self.forgot_password, bg=colors["button_bg"]).grid(row=8, column=0, pady=5)

    def toggle_password(self): # function to toggle password visibility
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def login(self): # gets input values
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_id = authenticate_user(username, password) # authenticates user
        
        if user_id:
            self.controller.user_id = user_id # store user ID 
            self.controller.username = username  # logs sucess
            self.controller.show_page("PasswordsPage") # go to the main password page
            logging.info(f"User '{self.controller.username}' logged in.") # logging
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.") # log failed login
            print(f"Login failed for: {username}") # pop up error


    def forgot_password(self): # placeholder for future password recovery features
        messagebox.showinfo("Forgot Password", "Password recovery is not implemented yet.")