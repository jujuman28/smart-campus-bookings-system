import tkinter as tk
from tkinter import messagebox
import sqlite3

from authentication import Authentication
from gui.dashboard import LecturerDashboard
from gui.administrator import AdministratorDashboard
from gui.operator import SystemOperatorDashboard


class LoginWindow:

    def __init__(self, root):

        self.root = root
        self.root.title("Smart Campus - Login")
        self.root.geometry("600x450")
        self.root.resizable(False, False)

        self.authentication = Authentication()

        # =========================
        # HEADING
        # =========================

        heading = tk.Label(
            self.root,
            text="Smart Campus Resource Booking System",
            font=("Arial", 18, "bold")
        )
        heading.pack(pady=30)

        # =========================
        # USERNAME
        # =========================

        tk.Label(
            self.root,
            text="Username",
            font=("Arial", 11)
        ).pack()

        self.username_entry = tk.Entry(
            self.root,
            width=35
        )
        self.username_entry.pack(pady=5)

        # =========================
        # PASSWORD
        # =========================

        tk.Label(
            self.root,
            text="Password",
            font=("Arial", 11)
        ).pack()

        self.password_entry = tk.Entry(
            self.root,
            width=35,
            show="*"
        )
        self.password_entry.pack(pady=5)

        # =========================
        # LOGIN BUTTON
        # =========================

        tk.Button(
            self.root,
            text="Login",
            width=20,
            command=self.login
        ).pack(pady=15)

        # =========================
        # REGISTER BUTTON
        # =========================

        tk.Button(
            self.root,
            text="Register",
            width=20,
            command=self.register
        ).pack(pady=5)

    # =========================
    # LOGIN
    # =========================

    def login(self):

        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        # Check empty fields
        if username == "" or password == "":

            messagebox.showerror(
                "Login Error",
                "Please enter your username and password."
            )

            return

        # Authenticate user
        user, message = self.authentication.login(
            username,
            password
        )

        # Check if login was successful
        if user is not None:

            self.root.destroy()

            dashboard_window = tk.Tk()

            # Lecturer
            if user.role == "Lecturer":

                LecturerDashboard(
                    dashboard_window,
                    username
                )

            # Campus Administrator
            # Campus Administrator
            elif user.role == "Campus Administrator":

                AdministratorDashboard(
                    dashboard_window,
                    username
                )

            # System Operator
            elif user.role == "System Operator":

                SystemOperatorDashboard(
                    dashboard_window,
                    username
                )

            # Unknown role
            else:

                messagebox.showerror(
                    "Login Error",
                    "Unknown user role."
                )

                dashboard_window.destroy()

                return

            dashboard_window.mainloop()

        else:

            messagebox.showerror(
                "Login Error",
                message
            )

    # =========================
    # REGISTER
    # =========================

    def register(self):

        register_window = tk.Toplevel(
            self.root
        )

        register_window.title(
            "Smart Campus - Register"
        )

        register_window.geometry(
            "500x500"
        )

        register_window.resizable(
            False,
            False
        )

        # =========================
        # HEADING
        # =========================

        tk.Label(
            register_window,
            text="Create Lecturer Account",
            font=("Arial", 20, "bold")
        ).pack(pady=20)

        # =========================
        # NAME
        # =========================

        tk.Label(
            register_window,
            text="Full Name"
        ).pack()

        name_entry = tk.Entry(
            register_window,
            width=35
        )

        name_entry.pack(pady=5)

        # =========================
        # USERNAME
        # =========================

        tk.Label(
            register_window,
            text="Username"
        ).pack()

        username_entry = tk.Entry(
            register_window,
            width=35
        )

        username_entry.pack(pady=5)

        # =========================
        # PASSWORD
        # =========================

        tk.Label(
            register_window,
            text="Password"
        ).pack()

        password_entry = tk.Entry(
            register_window,
            width=35,
            show="*"
        )

        password_entry.pack(pady=5)

        # =========================
        # CONFIRM PASSWORD
        # =========================

        tk.Label(
            register_window,
            text="Confirm Password"
        ).pack()

        confirm_entry = tk.Entry(
            register_window,
            width=35,
            show="*"
        )

        confirm_entry.pack(pady=5)

        # =========================
        # SAVE REGISTRATION
        # =========================

        def save_registration():

            name = name_entry.get().strip()
            username = username_entry.get().strip()
            password = password_entry.get()
            confirm_password = confirm_entry.get()

            # Check empty fields
            if (
                name == ""
                or username == ""
                or password == ""
                or confirm_password == ""
            ):

                messagebox.showerror(
                    "Registration Error",
                    "Please fill in all fields."
                )

                return

            # Check passwords
            if password != confirm_password:

                messagebox.showerror(
                    "Registration Error",
                    "Passwords do not match."
                )

                return

            # Connect to database
            connection = sqlite3.connect(
                "smart_campus.db"
            )

            cursor = connection.cursor()

            # Check if username already exists
            cursor.execute(
                """
                SELECT username
                FROM users
                WHERE username = ?
                """,
                (username,)
            )

            existing_user = cursor.fetchone()

            if existing_user is not None:

                connection.close()

                messagebox.showerror(
                    "Registration Error",
                    "Username already exists."
                )

                return

            # Create lecturer account
            cursor.execute(
                """
                INSERT INTO users
                (name, username, password, role)
                VALUES (?, ?, ?, ?)
                """,
                (
                    name,
                    username,
                    password,
                    "Lecturer"
                )
            )

            connection.commit()
            connection.close()

            messagebox.showinfo(
                "Registration Successful",
                "Lecturer account created successfully."
            )

            register_window.destroy()

        # =========================
        # CREATE ACCOUNT BUTTON
        # =========================

        tk.Button(
            register_window,
            text="Create Account",
            width=20,
            command=save_registration
        ).pack(pady=25)