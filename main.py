import tkinter as tk

from database import setup_database
from gui.login import LoginWindow


def main():

    # Create the database and tables
    setup_database()

    # Start the GUI
    window = tk.Tk()

    LoginWindow(window)

    window.mainloop()


if __name__ == "__main__":
    main()