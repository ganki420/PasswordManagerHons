import tkinter as tk
import logging
import time
from tkinter import ttk, messagebox
import sqlite3
from encryption import encrypt_password, decrypt_password
from theme import theme_manager
from backup.backup import backup_database
from backup.backup import restore_database
import random
import string


class PasswordsPage(tk.Frame): # main password page
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.user_id = controller.user_id # gets logged in users ID

        colors = theme_manager.get_colors() # get theme
        self.configure(bg=colors["bg"])

        style = ttk.Style(self) # configuring the treeview style based on dark/light mode
        if theme_manager.dark_mode:
            style.theme_use('clam')
            style.configure("Treeview",
                background="#2a2a2a",
                foreground="white",
                fieldbackground="#2a2a2a",
                bordercolor="#2a2a2a",
                borderwidth=0)
            style.configure("Treeview.Heading", background="#1e1e1e", foreground="white")
        else:
            style.theme_use('default')
            style.configure("Treeview",
                background="white",
                foreground="black",
                fieldbackground="white")
            style.configure("Treeview.Heading", background="SystemButtonFace", foreground="black")

        # allowing resizing
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Header, user information and settings
        self.header = tk.Frame(self, bg=colors["bg"])
        self.header.grid(row=0, column=0, sticky="ew", pady=10)
        self.user_label = tk.Label(self.header, font=("Arial", 10, "bold"), bg=colors["bg"], fg=colors["fg"])
        self.user_label.pack(side="left", padx=10)
        tk.Button(self.header, text="SIGN OUT", font=("Arial", 10, "bold"), command=lambda: controller.show_page("LoginPage"), bg=colors["button_bg"]).pack(side="right", padx=10)
        tk.Button(self.header, text="SETTINGS", font=("Arial", 10, "bold"), command=self.open_settings, bg=colors["button_bg"]).pack(side="right", padx=10)

        # Title
        tk.Label(self, text="Password Manager", font=("Arial", 18, "bold"), bg=colors["bg"], fg=colors["fg"]).grid(row=1, column=0, pady=10)

        # Password table setup
        columns = ("Website", "Username", "Password")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=10)
        self.tree.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        self.tree.column("Website", width=150, anchor="center", stretch=True)
        self.tree.column("Username", width=150, anchor="center", stretch=True)
        self.tree.column("Password", width=100, anchor="center", stretch=True)

        for col in columns:
            self.tree.heading(col, text=col) # adds table headings

        # Buttons
        button_frame = tk.Frame(self, bg=colors["bg"])
        button_frame.grid(row=3, column=0, sticky="ew", pady=10)

        tk.Button(button_frame, text="ADD PASSWORD", font=("Arial", 12, "bold"), command=self.add_password, bg=colors["button_bg"]).pack(side="left", padx=5, fill="x", expand=True)
        tk.Button(button_frame, text="SHOW PASSWORD", font=("Arial", 12, "bold"), command=self.show_selected_password, bg=colors["button_bg"]).pack(side="left", padx=5, fill="x", expand=True)
        tk.Button(button_frame, text="EDIT PASSWORD", font=("Arial", 12, "bold"), command=self.edit_selected_password, bg=colors["button_bg"]).pack(side="left", padx=5, fill="x", expand=True)
        tk.Button(button_frame, text="REMOVE PASSWORD", font=("Arial", 12, "bold"), command=self.remove_selected_password, bg=colors["button_bg"]).pack(side="left", padx=5, fill="x", expand=True)

        self.load_passwords() # loads password entries from the database

    def generate_password(self, length=12): # function to generate passwords
        characters = string.ascii_letters + string.digits + string.punctuation # the allowed characters
        return ''.join(random.choice(characters) for _ in range(length)) # returns random password
    
    def restore_backup_and_reload(self): # function to restore from backup
        restore_database() # calls restore function from the backup 
        self.load_passwords() # reloads password list after the restoring

    def open_settings(self): # function to open settings window
        settings_win = tk.Toplevel(self) # creates a new window on top
        settings_win.title("Settings")
        settings_win.geometry("280x150")
        settings_win.configure(bg="white")

        mode_icon = tk.StringVar(value="DARK MODE" if not theme_manager.dark_mode else "LIGHT MODE") # toggle button text

        def toggle_dark_mode(): # function to switch themes
            theme_manager.toggle_theme() # toggling dark and lighjt mode
            mode_icon.set("LIGHT MODE" if theme_manager.dark_mode else "DARK MODE") # updates the label
            self.controller.refresh_theme() # refresh all the UI with the new theme
            settings_win.destroy() # close settings window

        #ui
        tk.Label(settings_win, text="Settings", font=("Arial", 12), bg="white").pack(pady=(20, 5))
        tk.Button(settings_win,textvariable=mode_icon,font=("Segoe UI", 12, "bold"),bg="#444444",fg="white",activebackground="#666666",activeforeground="white",padx=10,pady=5,relief="flat",command=toggle_dark_mode).pack(pady=10)
        tk.Button(settings_win,text="Restore Backup",font=("Segoe UI", 12, "bold"),bg="#880000",fg="white",activebackground="#aa0000",activeforeground="white", padx=10, pady=5,relief="flat",command=self.restore_backup_and_reload).pack(pady=5)

    def tkraise(self, aboveThis=None): # function to raise frame to front
        self.user_label.config(text=f"LOGGED IN AS: {self.controller.username}") # updates the header label
        super().tkraise(aboveThis) # raise the page
        self.load_passwords() # refresh password list


    def load_passwords(self): # function to load saved passwords into the table
        if not self.controller.user_id: # skip if not logged in
            return

        self.tree.delete(*self.tree.get_children()) # clear existing rows

        conn = sqlite3.connect("passwords.db") # opens database connection
        cursor = conn.cursor()

        #gets all passwords for the current user
        cursor.execute("SELECT id, website, username, password_iv, encrypted_password FROM passwords WHERE user_id = ?", (self.controller.user_id,))
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            password_id, website, username, iv, encrypted_password = row
            masked_password = "*" * 8 # shows password as hidden
            self.tree.insert("", "end", values=(website, username, masked_password), tags=(password_id,))

    def add_password(self): # function to open window for adding a new password
        add_win = tk.Toplevel(self) # makes a pop up window
        add_win.title("Add Password")
        add_win.geometry("300x300")
        
        #website field
        tk.Label(add_win, text="Website").pack()
        website_entry = tk.Entry(add_win)
        website_entry.pack(fill="x", padx=10, pady=5)

        #username field
        tk.Label(add_win, text="Username").pack()
        username_entry = tk.Entry(add_win)
        username_entry.pack(fill="x", padx=10, pady=5)

        #password field
        tk.Label(add_win, text="Password").pack()
        password_entry = tk.Entry(add_win, show="*")
        password_entry.pack(fill="x", padx=10, pady=5)

        # Checkbox to show and hide password
        show_password_var = tk.BooleanVar()
        tk.Checkbutton(add_win, text="Show Password", variable=show_password_var,
                       command=lambda: password_entry.config(show="" if show_password_var.get() else "*")).pack()

        #strength label
        strength_label = tk.Label(add_win, text="", font=("Arial", 10, "bold"))
        strength_label.pack(pady=(5, 0))

        def update_strength(password): # function to check password strength
            import re # local import for password strength
            length = len(password) >= 8
            lower = re.search(r"[a-z]", password)
            upper = re.search(r"[A-Z]", password)
            digit = re.search(r"[0-9]", password)
            special = re.search(r"[^a-zA-Z0-9]", password)
            score = sum(bool(x) for x in [length, lower, upper, digit, special])

            if score <= 2:
                strength, color = "Weak", "red"
            elif score in [3, 4]:
                strength, color = "Medium", "orange"
            else:
                strength, color = "Strong", "green"

            strength_label.config(text=f"Strength: {strength}", fg=color)

        def fill_generated_password(): # fill in a generated password 
            generated = self.generate_password() # use password generator
            password_entry.delete(0, tk.END)
            password_entry.insert(0, generated)

        tk.Button(add_win, text="Generate Password", command=fill_generated_password).pack(pady=5)

        # update strength as the user types
        password_entry.bind("<KeyRelease>", lambda e: update_strength(password_entry.get()))
        update_strength(password_entry.get()) # check initially

        def save_password(): # functin to save a new password entry
            import hashlib, requests # imports when needed.
            sha1 = hashlib.sha1(password_entry.get().encode('utf-8')).hexdigest().upper()
            prefix, suffix = sha1[:5], sha1[5:]
            url = f"https://api.pwnedpasswords.com/range/{prefix}"
            try:
                res = requests.get(url)
                if res.status_code == 200:
                    hashes = (line.split(':') for line in res.text.splitlines())
                    for h, count in hashes:
                        if h == suffix:
                            messagebox.showwarning("Warning", f"This password has been seen {count} times in data breaches. Please consider using a stronger password.") # message if password is detected in databreaches
                            break
            except Exception as e:
                print("Failed to check HIBP API:", e) # if couldnt check
            website = website_entry.get()
            username = username_entry.get()
            password = password_entry.get()

            if not website or not username or not password:
                messagebox.showerror("Error", "All fields are required.") # validation
                return

            iv, encrypted_password = encrypt_password(password) # encrypt the password

            conn = sqlite3.connect("passwords.db") # inserting into  database
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO passwords (user_id, website, username, password_iv, encrypted_password)
                VALUES (?, ?, ?, ?, ?)
            """, (self.controller.user_id, website, username, iv, encrypted_password))
            conn.commit()
            conn.close()

            logging.info(f"User '{self.controller.username}' added a password for website '{website}'.") #logging

            messagebox.showinfo("Success", "Password saved successfully!")
            backup_database() # makes backup after saving
            add_win.destroy() # closes the add window
            self.load_passwords() # reloads the entries

        tk.Button(add_win, text="Save", command=save_password).pack(pady=10)

    def show_selected_password(self): # function to show decrypted password for the selected password
        selected_item = self.tree.selection() # gets the selected row
        if not selected_item:
            messagebox.showerror("Error", "Please select a password entry.")
            return

        # gets selected values
        values = self.tree.item(selected_item, "values")
        website, username = values[:2]

        # gets the encrypted data from the database
        conn = sqlite3.connect("passwords.db")
        cursor = conn.cursor()
        cursor.execute("SELECT password_iv, encrypted_password FROM passwords WHERE user_id = ? AND website = ? AND username = ?",
                       (self.controller.user_id, website, username))
        row = cursor.fetchone()
        conn.close()

        if row:
            iv, encrypted_password = row
            decrypted_password = decrypt_password(iv, encrypted_password) #decrypts it

            # makes a popup window to show the password
            popup = tk.Toplevel(self)
            popup.title("Decrypted Password")
            popup.geometry("400x200")
            popup.configure(bg=theme_manager.get_colors()["bg"])

            # shows site, username and password
            tk.Label(popup, text=f"Website: {website}", font=("Arial", 12), bg=theme_manager.get_colors()["bg"], fg=theme_manager.get_colors()["fg"]).pack(pady=5)
            tk.Label(popup, text=f"Username: {username}", font=("Arial", 12), bg=theme_manager.get_colors()["bg"], fg=theme_manager.get_colors()["fg"]).pack(pady=5)
            tk.Label(popup,text=f"Password: {decrypted_password}",font=("Arial", 12),bg=theme_manager.get_colors()["bg"],fg=theme_manager.get_colors()["fg"]).pack(pady=5)

            def copy_to_clipboard(): # function to copy the password to clipboard
                self.clipboard_clear() # clears the already copied clipboard
                self.clipboard_append(decrypted_password) # adds password to clipboard
                self.update() # ensure clipboard is updated
                messagebox.showinfo("Copied", "Password copied to clipboard!") # shows confirmation

            tk.Button(popup, text="Copy Password", command=copy_to_clipboard, bg=theme_manager.get_colors()["button_bg"]).pack(pady=10) # copy button
        else:
            messagebox.showerror("Error", "Password not found.") # shows the error if it is missing

    def edit_selected_password(self): # function to edit selected password entry
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a password to edit.")
            return

        values = self.tree.item(selected_item, "values")
        website, username = values[:2] # gets current website and username

        edit_win = tk.Toplevel(self) # makes popup window
        edit_win.title("Edit Password")
        edit_win.geometry("300x300")

        # password input
        tk.Label(edit_win, text="New Password").pack()
        password_entry = tk.Entry(edit_win, show="*")
        password_entry.pack(fill="x", padx=10, pady=5)

        # show and hide password checkbox
        show_password_var = tk.BooleanVar()
        tk.Checkbutton(edit_win, text="Show Password", variable=show_password_var,
                       command=lambda: password_entry.config(show="" if show_password_var.get() else "*")).pack()
        
        # strength indicator
        strength_label = tk.Label(edit_win, text="", font=("Arial", 10, "bold"))
        strength_label.pack(pady=(5, 0))
        
        def update_strength(password): # again updte strength laberl based on new input
            import re
            length = len(password) >= 8
            lower = re.search(r"[a-z]", password)
            upper = re.search(r"[A-Z]", password)
            digit = re.search(r"[0-9]", password)
            special = re.search(r"[^a-zA-Z0-9]", password)
            score = sum(bool(x) for x in [length, lower, upper, digit, special])

            if score <= 2:
                strength, color = "Weak", "red"
            elif score in [3, 4]:
                strength, color = "Medium", "orange"
            else:
                strength, color = "Strong", "green"

            strength_label.config(text=f"Strength: {strength}", fg=color)

        def fill_generated_password(): # auto fill a generated strong password
            generated = self.generate_password()
            password_entry.delete(0, tk.END)
            password_entry.insert(0, generated)

        tk.Button(edit_win, text="Generate Password", command=fill_generated_password).pack(pady=5)

        password_entry.bind("<KeyRelease>", lambda e: update_strength(password_entry.get()))
        update_strength(password_entry.get()) # the initial call

        def update_password(): # function to update password in database
            # Check if password has been breached in HIBP
            import hashlib, requests
            sha1 = hashlib.sha1(password_entry.get().encode('utf-8')).hexdigest().upper()
            prefix, suffix = sha1[:5], sha1[5:]
            url = f"https://api.pwnedpasswords.com/range/{prefix}"
            try:
                res = requests.get(url)
                if res.status_code == 200:
                    hashes = (line.split(':') for line in res.text.splitlines())
                    for h, count in hashes:
                        if h == suffix:
                            messagebox.showwarning("Warning", f"This password has been seen {count} times in data breaches. Consider using a stronger password.")
                            break
            except Exception as e:
                print("Failed to check HIBP API:", e)
            new_password = password_entry.get()
            if not new_password:
                messagebox.showerror("Error", "Password cannot be empty.")
                return

            iv, encrypted_password = encrypt_password(new_password) # encrypt new password

            #update entry in database
            conn = sqlite3.connect("passwords.db")
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE passwords SET password_iv = ?, encrypted_password = ?
                WHERE user_id = ? AND website = ? AND username = ?
            """, (iv, encrypted_password, self.controller.user_id, website, username))
            conn.commit()
            conn.close()

            logging.info(f"User '{self.controller.username}' edited a password for website '{website}'.") # logging

            messagebox.showinfo("Success", "Password updated successfully!")
            backup_database() # makes abackup
            edit_win.destroy() # closes the popup
            self.load_passwords() # reloads the updated entries

        tk.Button(edit_win, text="Save", command=update_password).pack(pady=10) # save button

    def remove_selected_password(self): # function to delete selected password
        selected_item = self.tree.selection() # gets selected row in the table
        if not selected_item:
            messagebox.showerror("Error", "Please select a password to remove.") # error if nothing is selected
            return

        values = self.tree.item(selected_item, "values")
        website, username = values[:2] # get website and username from selected row

        # delete entry from the database
        conn = sqlite3.connect("passwords.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM passwords WHERE user_id = ? AND website = ? AND username = ?",
                       (self.controller.user_id, website, username))
        conn.commit()
        conn.close()

        logging.info(f"User '{self.controller.username}' deleted a password for website '{website}'.") # logging

        messagebox.showinfo("Success", "Password deleted successfully!") # confrim to user
        self.load_passwords() # refreshing the password list.
