import tkinter as tk 
import logging
import time
from ui.login import LoginPage
from ui.signup import SignUpPage
from ui.passwords import PasswordsPage

#logging, first setting name name of the logging file that will be saved
# logging information
# fortmat is: timestamp log lvl and the log message
logging.basicConfig( filename="user_actions.log",level=logging.INFO,format="%(asctime)s - %(levelname)s - %(message)s")

SESSION_TIMEOUT = 5 * 60  # 5 minutes for inactivity auto logout

class PasswordManagerApp(tk.Tk): # main class for the app
    def __init__(self):
        super().__init__() # initialising Tkinter
        self.title("Password Manager") # title of the window

        #window size
        window_width = 800
        window_height = 400

        self.username = None # storing username of the user that is logged in
        self.geometry(f"{window_width}x{window_height}") # setting window dimentions
        self.minsize(600, 400)  # set minimum window size 
        self.center_window(window_width, window_height) # centring the window on screen
        self.user_id = None  # Storing the ID of the logged in user

        # letting the window layout expand and become smaller properly
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # making main container frome where the login, signup and main manager page is shown
        self.container = tk.Frame(self)
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # initialising all the pages
        self.pages = {}
        for PageClass in (LoginPage, SignUpPage, PasswordsPage):
            page_name = PageClass.__name__ # getting the names of the class as a string
            page = PageClass(parent=self.container, controller=self) # page instance
            self.pages[page_name] = page # store it in the pages dictionary
            page.grid(row=0, column=0, sticky="nsew") # stacking all the pages in the same grid cell 

        # session timeout setup
        self.last_activity_time = time.time() # tracking the time of the last user interaction
        self.after(10000, self.check_session_timeout)  # Check every 10 seconds

        #making any key press or mouse click reset the timer
        self.bind_all("<Key>", lambda e: self.reset_timer())
        self.bind_all("<Button>", lambda e: self.reset_timer())
        self.show_page("LoginPage") # Show login page on startup

    def reset_timer(self): # function to reset the session timer
        self.last_activity_time = time.time() # update the activity time

    def check_session_timeout(self): # function to check if the session timed out
        if time.time() - self.last_activity_time > SESSION_TIMEOUT:  # chjecking if activity time goes over the timeout limit
            logging.info(f"User '{self.username}' was logged out due to inactivity.") # log a message saying the user was logged to inactivity
        
            # popup telling the user
            tk.messagebox.showinfo("Session Timed Out", "You have been logged out due to being inactive for 5 minutes.")

            #reset the data and go back to the login page
            self.user_id = None
            self.username = None
            self.show_page("LoginPage")
        else:
            self.after(10000, self.check_session_timeout)  # check every 10 seconds

    #center the window on the screen
    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate x and y position to center it
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def show_page(self, page_name): # function to make tthe specified page visible
        page = self.pages[page_name] # gets page from the dictionary
        page.tkraise() # brings the page to the front 

    def refresh_theme(self): # function to refresh pages to apply the theme
        for name, page in self.pages.items(): # loop through all apges
            page.destroy() # delete the old page
            new_page = type(page)(self.container, self) # remake the page with the updated theme
            self.pages[name] = new_page # replaces the old page in the dictionary
            new_page.grid(row=0, column=0, sticky="nsew") # add thhe new page layout
        self.show_page("PasswordsPage") # shows the password apge after refreshing

if __name__ == "__main__": # runs the app only if this file is run
    app = PasswordManagerApp() # makes an instance of the app
    app.mainloop() # starts a Tkinter loop
