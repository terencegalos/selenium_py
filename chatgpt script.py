from tkinter import *
from selenium import webdriver

# Browser class to open a browser window
class Browser:
    def __init__(self, url):
        path = './chrome_driver/chromedriver'
        self.url = url
        self.driver = webdriver.Chrome(path) # or other browser driver
        self.driver.maximize_window()
        self.driver.get(url)

# Login class to create a login prompt with tkinter
class Login:
    def __init__(self, master):
        self.master = master
        master.title("Login")

        # Labels for username and password
        self.label_username = Label(master, text="Username:")
        self.label_password = Label(master, text="Password:")

        # Entries for username and password
        self.entry_username = Entry(master)
        self.entry_password = Entry(master, show="*")

        # Grid layout for labels and entries
        self.label_username.grid(row=0, sticky=E)
        self.label_password.grid(row=1, sticky=E)
        self.entry_username.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)

        # Login button
        self.logbtn = Button(master, text="Login", command=self._login_btn_clicked)
        self.logbtn.grid(columnspan=2)

    # Function to check if login is successful
    def _login_btn_clicked(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Check if username and password are correct
        if username == "root" and password == "toor":
            url = "https://www.google.com"
            browser = Browser(url)
            self.master.destroy() # Close login prompt if successful
        else:
            # Clear entries and display error message
            self.entry_username.delete(0, END)
            self.entry_password.delete(0, END)

            self.label_message = Label(self.master, text="Incorrect username or password")
            self.label_message.grid(row=2, columnspan=2)

# Main function
if __name__ == '__main__':
    # Create tkinter window and login prompt
    root = Tk()
    login = Login(root)
    root.mainloop()
