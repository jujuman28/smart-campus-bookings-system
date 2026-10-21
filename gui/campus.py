import tkinter as tk
from tkinter import messagebox
import sqlite3


class CampusWindow:

    def __init__(self, root, user):

        self.root = root
        self.user = user

        self.root.title("Smart Campus - Campus Selection")
        self.root.geometry("700x500")
        self.root.resizable(False, False)

        # Heading
        title = tk.Label(
            self.root,
            text="Campus Selection",
            font=("Times New Roman", 22, "bold")
        )
        title.pack(pady=25)

        # Logged-in user
        welcome = tk.Label(
            self.root,
            text=f"Welcome, {self.user.name}",
            font=("Times New Roman", 14)
        )
        welcome.pack(pady=5)

        # User role
        role = tk.Label(
            self.root,
            text=f"Role: {self.user.get_role()}",
            font=("Times New Roman", 13)
        )
        role.pack(pady=5)

        # Campus label
        campus_label = tk.Label(
            self.root,
            text="Select a campus:",
            font=("Times New Roman", 14)
        )
        campus_label.pack(pady=(25, 5))

        # Get campuses from database
        self.campuses = self.get_campuses()

        # Campus names
        self.campus_names = [
            campus[1] for campus in self.campuses
        ]

        # Campus dropdown
        self.campus_var = tk.StringVar()

        self.campus_dropdown = tk.OptionMenu(
            self.root,
            self.campus_var,
            *self.campus_names
        )

        self.campus_dropdown.config(
            width=30,
            font=("Times New Roman", 12)
        )

        self.campus_dropdown.pack(pady=10)

        # Select button
        select_button = tk.Button(
            self.root,
            text="Select Campus",
            width=20,
            font=("Times New Roman", 12, "bold"),
            command=self.select_campus
        )

        select_button.pack(pady=20)

        # Active campus
        self.active_label = tk.Label(
            self.root,
            text="Active Campus: None",
            font=("Times New Roman", 14, "bold")
        )

        self.active_label.pack(pady=10)

        # Booking policy
        self.policy_label = tk.Label(
            self.root,
            text="Booking Policy: None",
            font=("Times New Roman", 12),
            wraplength=600
        )

        self.policy_label.pack(pady=10)

    def get_campuses(self):

        connection = sqlite3.connect("smart_campus.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT campus_id,
                   campus_name,
                   max_duration,
                   start_hour,
                   end_hour
            FROM campuses
        """)

        campuses = cursor.fetchall()

        connection.close()

        return campuses

    def select_campus(self):

        selected_name = self.campus_var.get()

        if selected_name == "":
            messagebox.showerror(
                "Campus Selection",
                "Please select a campus."
            )
            return

        selected_campus = None

        for campus in self.campuses:

            if campus[1] == selected_name:
                selected_campus = campus
                break

        if selected_campus is None:
            return

        campus_id = selected_campus[0]
        campus_name = selected_campus[1]
        max_duration = selected_campus[2]
        start_hour = selected_campus[3]
        end_hour = selected_campus[4]

        # Display active campus
        self.active_label.config(
            text=f"Active Campus: {campus_name}"
        )

        # Display campus policy
        self.policy_label.config(
            text=(
                f"Booking Policy:\n"
                f"Maximum duration: {max_duration} hours\n"
                f"Booking hours: {start_hour}:00 - {end_hour}:00"
            )
        )

        messagebox.showinfo(
            "Campus Selected",
            f"{campus_name} is now the active campus."
        )