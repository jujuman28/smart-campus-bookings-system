import tkinter as tk
from tkinter import messagebox
import sqlite3

from booking_rules import BookingRules


class LecturerWindow:

    def __init__(self, root, user, campus):

        self.root = root
        self.user = user
        self.campus = campus

        self.root.title("Lecturer - Resource Booking")
        self.root.geometry("800x650")
        self.root.resizable(False, False)

        # Heading
        title = tk.Label(
            self.root,
            text="Lecturer Resource Booking",
            font=("Times New Roman", 22, "bold")
        )
        title.pack(pady=20)

        # Lecturer name
        user_label = tk.Label(
            self.root,
            text=f"Lecturer: {self.user.name}",
            font=("Times New Roman", 13)
        )
        user_label.pack()

        # Campus
        campus_label = tk.Label(
            self.root,
            text=f"Active Campus: {self.campus[1]}",
            font=("Times New Roman", 14, "bold")
        )
        campus_label.pack(pady=10)

        # Booking policy
        policy_label = tk.Label(
            self.root,
            text=(
                f"Maximum duration: {self.campus[2]} hours | "
                f"Booking hours: {self.campus[3]}:00 - "
                f"{self.campus[4]}:00"
            ),
            font=("Times New Roman", 12)
        )
        policy_label.pack(pady=5)

        # Resource
        resource_label = tk.Label(
            self.root,
            text="Select Resource:",
            font=("Times New Roman", 13)
        )
        resource_label.pack(pady=(20, 5))

        self.resources = self.get_resources()

        self.resource_names = [
            resource[1] for resource in self.resources
        ]

        self.resource_var = tk.StringVar()

        self.resource_dropdown = tk.OptionMenu(
            self.root,
            self.resource_var,
            *self.resource_names
        )

        self.resource_dropdown.config(
            width=30,
            font=("Times New Roman", 12)
        )

        self.resource_dropdown.pack()

        # Booking date
        date_label = tk.Label(
            self.root,
            text="Booking Date (YYYY-MM-DD):",
            font=("Times New Roman", 13)
        )
        date_label.pack(pady=(15, 5))

        self.date_entry = tk.Entry(
            self.root,
            width=30,
            font=("Times New Roman", 12)
        )
        self.date_entry.pack()

        # Start time
        time_label = tk.Label(
            self.root,
            text="Start Time (HH:MM):",
            font=("Times New Roman", 13)
        )
        time_label.pack(pady=(15, 5))

        self.time_entry = tk.Entry(
            self.root,
            width=30,
            font=("Times New Roman", 12)
        )
        self.time_entry.pack()

        # Duration
        duration_label = tk.Label(
            self.root,
            text="Duration (hours):",
            font=("Times New Roman", 13)
        )
        duration_label.pack(pady=(15, 5))

        self.duration_entry = tk.Entry(
            self.root,
            width=30,
            font=("Times New Roman", 12)
        )
        self.duration_entry.pack()

        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        book_button = tk.Button(
            button_frame,
            text="Book Resource",
            width=18,
            font=("Times New Roman", 12, "bold"),
            command=self.create_booking
        )
        book_button.grid(row=0, column=0, padx=10)

        history_button = tk.Button(
            button_frame,
            text="Booking History",
            width=18,
            font=("Times New Roman", 12, "bold"),
            command=self.show_history
        )
        history_button.grid(row=0, column=1, padx=10)

    # Get resources for the selected campus
    def get_resources(self):

        connection = sqlite3.connect("smart_campus.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT resource_id, resource_name
            FROM resources
            WHERE campus_id = ?
        """, (self.campus[0],))

        resources = cursor.fetchall()

        connection.close()

        return resources

    # Create a booking
    def create_booking(self):

        resource_name = self.resource_var.get()
        booking_date = self.date_entry.get().strip()
        start_time = self.time_entry.get().strip()
        duration_text = self.duration_entry.get().strip()

        # Check empty fields
        if (
            resource_name == ""
            or booking_date == ""
            or start_time == ""
            or duration_text == ""
        ):
            messagebox.showerror(
                "Booking Error",
                "Please complete all booking fields."
            )
            return

        # Convert duration to integer
        try:
            duration = int(duration_text)
        except ValueError:
            messagebox.showerror(
                "Booking Error",
                "Duration must be a whole number."
            )
            return

        # Find resource ID
        resource_id = None

        for resource in self.resources:

            if resource[1] == resource_name:
                resource_id = resource[0]
                break

        if resource_id is None:
            messagebox.showerror(
                "Booking Error",
                "Please select a valid resource."
            )
            return

        # Check campus booking rules
        rules = BookingRules(
            self.campus[1],
            self.campus[2],
            self.campus[3],
            self.campus[4]
        )

        valid, message = rules.validate_booking(
            start_time,
            duration
        )

        if not valid:
            messagebox.showerror(
                "Booking Policy",
                message
            )
            return

        # Check for overlapping bookings
        if self.check_overlap(
            resource_id,
            booking_date,
            start_time,
            duration
        ):
            messagebox.showerror(
                "Resource Unavailable",
                "This resource is already booked during that time."
            )
            return

        # Save booking
        connection = sqlite3.connect("smart_campus.db")
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO bookings
            (
                user_id,
                resource_id,
                campus_id,
                booking_date,
                start_time,
                duration
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            1,
            resource_id,
            self.campus[0],
            booking_date,
            start_time,
            duration
        ))

        connection.commit()
        connection.close()

        messagebox.showinfo(
            "Booking Successful",
            "Your resource has been booked successfully."
        )

        # Clear fields
        self.resource_var.set("")
        self.date_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)

    # Check whether the resource is already booked
    def check_overlap(
        self,
        resource_id,
        booking_date,
        start_time,
        duration
    ):

        connection = sqlite3.connect("smart_campus.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT start_time, duration
            FROM bookings
            WHERE resource_id = ?
            AND booking_date = ?
        """, (
            resource_id,
            booking_date
        ))

        bookings = cursor.fetchall()

        connection.close()

        new_start = self.time_to_minutes(start_time)
        new_end = new_start + (duration * 60)

        for booking in bookings:

            existing_start = self.time_to_minutes(
                booking[0]
            )

            existing_end = (
                existing_start
                + (booking[1] * 60)
            )

            if (
                new_start < existing_end
                and new_end > existing_start
            ):
                return True

        return False

    # Convert HH:MM to minutes
    def time_to_minutes(self, time):

        hours, minutes = map(
            int,
            time.split(":")
        )

        return hours * 60 + minutes

    # Show booking history
    def show_history(self):

        history_window = tk.Toplevel(self.root)

        history_window.title("Booking History")
        history_window.geometry("700x400")

        title = tk.Label(
            history_window,
            text="My Booking History",
            font=("Times New Roman", 18, "bold")
        )
        title.pack(pady=15)

        booking_list = tk.Listbox(
            history_window,
            width=80,
            height=15,
            font=("Times New Roman", 11)
        )
        booking_list.pack(pady=10)

        connection = sqlite3.connect(
            "smart_campus.db"
        )

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                b.booking_date,
                b.start_time,
                b.duration,
                r.resource_name,
                c.campus_name
            FROM bookings b
            JOIN resources r
                ON b.resource_id = r.resource_id
            JOIN campuses c
                ON b.campus_id = c.campus_id
            WHERE b.user_id = ?
            ORDER BY b.booking_date
        """, (1,))

        bookings = cursor.fetchall()

        connection.close()

        for booking in bookings:

            booking_list.insert(
                tk.END,
                f"Date: {booking[0]} | "
                f"Time: {booking[1]} | "
                f"Duration: {booking[2]} hour(s) | "
                f"Resource: {booking[3]} | "
                f"Campus: {booking[4]}"
            )