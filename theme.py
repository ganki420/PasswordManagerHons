class ThemeManager: # class to handle the toggling of light and dark mode for the main password manager
    def __init__(self):
        self.dark_mode = False # starting with light mode 

    def toggle_theme(self): # change the theme, if dark switch to light and vice versa
        self.dark_mode = not self.dark_mode

    def get_colors(self):
        if self.dark_mode:
            return {
                "bg": "#1e1e1e", # background
                "fg": "#ffffff", # text colour
                "button_bg": "#333333", # background of button
                "entry_bg": "#2a2a2a", # field background
                "entry_fg": "#ffffff" # field text
            }
        else:
            return {
                "bg": "white", # background
                "fg": "black", # text
                "button_bg": "SystemButtonFace", # default button style
                "entry_bg": "white", # field background
                "entry_fg": "black" # field text
            }

theme_manager = ThemeManager() # instance that I can use in the whole program 
