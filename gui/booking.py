
import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime, date, timedelta

from booking_rules import BookingRules


class BookingWindow:

    def __init__(self, root, username):

        self.root = root
        self.username = username

        self.root.title("Smart Campus - Make a Booking")
        self.root.geometry("600x650")
        self.root.resizable(False, False)

        tk.Label(
            self.root,
            text="Make a Resource Booking",
            font=("Arial", 22, "bold")
        ).pack(pady=20)

        tk.Label(
            self.root,
            text=f"Lecturer: {self.username}",
            font=("Arial", 12)
        ).pack(pady=5)

        # Campus selection
        tk.Label(
            self.root,
            text="Select Campus",
            font=("Arial", 11)
        ).pack(pady=(20, 5))

        self.campus_var = tk.StringVar()
        self.load_campuses()

        campus_options = self.campuses or ["No campuses available"]
        self.campus_var.set(campus_options[0])

        self.campus_menu = tk.OptionMenu(
            self.root,
            self.campus_var,
            *campus_options
        )
        self.campus_menu.config(width=30)
        self.campus_menu.pack()

        # Resource selection
        tk.Label(
            self.root,
            text="Select Resource",
            font=("Arial", 11)
        ).pack(pady=(15, 5))

        self.resource_var = tk.StringVar(value="")
        self.resource_menu = tk.OptionMenu(
            self.root,
            self.resource_var,
            "Select a campus first"
        )
        self.resource_menu.config(width=30)
        self.resource_menu.pack()

        self.campus_var.trace_add(
            "write",
            self.update_resources
        )

        # Date
        tk.Label(
            self.root,
            text="Booking Date (YYYY-MM-DD)",
            font=("Arial", 11)
        ).pack(pady=(15, 5))

        self.date_entry = tk.Entry(self.root, width=35)
        self.date_entry.pack()

        tk.Label(
            self.root,
            text="Example: 2026-10-20",
            font=("Arial", 9)
        ).pack()

        # Start time
        tk.Label(
            self.root,
            text="Start Time (HH:MM)",
            font=("Arial", 11)
        ).pack(pady=(15, 5))

        self.start_time_entry = tk.Entry(self.root, width=35)
        self.start_time_entry.pack()

        tk.Label(
            self.root,
            text="Example: 09:00",
            font=("Arial", 9)
        ).pack()

        # Duration
        tk.Label(
            self.root,
            text="Duration (whole hours)",
            font=("Arial", 11)
        ).pack(pady=(15, 5))

        self.duration_entry = tk.Entry(self.root, width=35)
        self.duration_entry.pack()

        tk.Label(
            self.root,
            text="Example: 2",
            font=("Arial", 9)
        ).pack()

        # Submit
        tk.Button(
            self.root,
            text="Submit Booking",
            width=25,
            height=2,
            command=self.submit_booking
        ).pack(pady=25)

    # =========================
    # LOAD CAMPUSES
    # =========================

    def load_campuses(self):

        connection = sqlite3.connect("smart_campus.db")

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT campus_id, campus_name
                FROM campuses
                ORDER BY campus_name
            """)

            rows = cursor.fetchall()

        finally:
            connection.close()

        self.campus_ids = {
            campus_name: campus_id
            for campus_id, campus_name in rows
        }

        self.campuses = [
            campus_name
            for campus_id, campus_name in rows
        ]

        self.resource_ids = {}

    # =========================
    # LOAD RESOURCES
    # =========================

    def update_resources(self, *args):

        campus = self.campus_var.get()
        campus_id = self.campus_ids.get(campus)

        self.resource_ids = {}
        self.resource_var.set("")

        menu = self.resource_menu["menu"]
        menu.delete(0, "end")

        if campus_id is None:

            menu.add_command(
                label="No resources available",
                command=lambda: None
            )
            return

        connection = sqlite3.connect("smart_campus.db")

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT resource_id, resource_name
                FROM resources
                WHERE campus_id = ?
                ORDER BY resource_name
            """, (campus_id,))

            rows = cursor.fetchall()

        finally:
            connection.close()

        for resource_id, resource_name in rows:

            self.resource_ids[resource_name] = resource_id

            menu.add_command(
                label=resource_name,
                command=lambda value=resource_name:
                    self.resource_var.set(value)
            )

        if rows:

            self.resource_var.set(rows[0][1])

        else:

            menu.add_command(
                label="No resources available",
                command=lambda: None
            )

    # =========================
    # SUBMIT BOOKING
    # =========================

    def submit_booking(self):

        campus = self.campus_var.get()
        resource = self.resource_var.get()
        booking_date = self.date_entry.get().strip()
        start_time = self.start_time_entry.get().strip()
        duration_text = self.duration_entry.get().strip()

        # Check required fields
        if not all([
            campus,
            resource,
            booking_date,
            start_time,
            duration_text
        ]):

            messagebox.showerror(
                "Booking Error",
                "Please fill in all fields.",
                parent=self.root
            )
            return

        # Check date format and validity
        try:
            selected_date = datetime.strptime(
                booking_date,
                "%Y-%m-%d"
            ).date()

            if selected_date.isoformat() != booking_date:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Invalid Date",
                "Enter a valid date in YYYY-MM-DD format.",
                parent=self.root
            )
            return

        # Reject dates in the past
        if selected_date < date.today():

            messagebox.showerror(
                "Invalid Date",
                "You cannot book a date in the past.",
                parent=self.root
            )
            return

        # Check start time
        try:
            parsed_time = datetime.strptime(
                start_time,
                "%H:%M"
            )

            if parsed_time.strftime("%H:%M") != start_time:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Invalid Time",
                "Enter a valid time in HH:MM format, such as 09:00.",
                parent=self.root
            )
            return

        # Check duration
        try:
            duration = int(duration_text)

        except ValueError:

            messagebox.showerror(
                "Invalid Duration",
                "Duration must be a whole number of hours.",
                parent=self.root
            )
            return

        if duration <= 0:

            messagebox.showerror(
                "Invalid Duration",
                "Duration must be greater than zero.",
                parent=self.root
            )
            return

        campus_id = self.campus_ids.get(campus)
        resource_id = self.resource_ids.get(resource)

        if campus_id is None or resource_id is None:

            messagebox.showerror(
                "Booking Error",
                "Please select a valid campus and resource.",
                parent=self.root
            )
            return

        # Get campus rules
        connection = sqlite3.connect("smart_campus.db")

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT max_duration, start_hour, end_hour
                FROM campuses
                WHERE campus_id = ?
            """, (campus_id,))

            campus_rules = cursor.fetchone()

            cursor.execute("""
                SELECT user_id
                FROM users
                WHERE username = ?
            """, (self.username,))

            user = cursor.fetchone()

        finally:
            connection.close()

        if campus_rules is None:

            messagebox.showerror(
                "Booking Error",
                "Campus information could not be found.",
                parent=self.root
            )
            return

        if user is None:

            messagebox.showerror(
                "Booking Error",
                "Lecturer account could not be found.",
                parent=self.root
            )
            return

        max_duration, start_hour, end_hour = campus_rules
        user_id = user[0]

        # Check maximum duration
        rules = BookingRules(
            campus_name=campus,
            max_duration=max_duration,
            start_hour=start_hour,
            end_hour=end_hour
        )

        valid, message = rules.check_duration(duration)

        if not valid:

            messagebox.showerror(
                "Booking Not Allowed",
                message,
                parent=self.root
            )
            return

        # Check actual start and end times, including minutes
        start_minutes = (
            parsed_time.hour * 60 + parsed_time.minute
        )

        end_minutes = start_minutes + duration * 60

        campus_open = start_hour * 60
        campus_close = end_hour * 60

        if start_minutes < campus_open:

            messagebox.showerror(
                "Booking Not Allowed",
                f"Bookings can only start from {start_hour:02d}:00.",
                parent=self.root
            )
            return

        if end_minutes > campus_close:

            messagebox.showerror(
                "Booking Not Allowed",
                f"Your booking must end by {end_hour:02d}:00.",
                parent=self.root
            )
            return

        # Reject a start time that has already passed today
        if selected_date == date.today():

            booking_datetime = datetime.combine(
                selected_date,
                parsed_time.time()
            )

            if booking_datetime <= datetime.now():

                messagebox.showerror(
                    "Invalid Time",
                    "You cannot book a start time that has already passed.",
                    parent=self.root
                )
                return

        # =========================
        # CHECK DOUBLE-BOOKING
        # =========================

        connection = sqlite3.connect("smart_campus.db")

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT start_time, duration
                FROM bookings
                WHERE resource_id = ?
                AND booking_date = ?
            """, (resource_id, booking_date))

            existing_bookings = cursor.fetchall()

            new_start = datetime.combine(
                selected_date,
                parsed_time.time()
            )

            new_end = new_start + timedelta(hours=duration)

            for existing_time, existing_duration in existing_bookings:

                existing_start_time = datetime.strptime(
                    existing_time,
                    "%H:%M"
                ).time()

                existing_start = datetime.combine(
                    selected_date,
                    existing_start_time
                )

                existing_end = existing_start + timedelta(
                    hours=existing_duration
                )

                # Two bookings overlap if these conditions are true
                if (
                    new_start < existing_end
                    and new_end > existing_start
                ):

                    messagebox.showerror(
                        "Booking Conflict",
                        "This resource is already booked during that time.",
                        parent=self.root
                    )
                    return

            # =========================
            # SAVE BOOKING
            # =========================

            cursor.execute("""
                INSERT INTO bookings (
                    user_id,
                    resource_id,
                    campus_id,
                    booking_date,
                    start_time,
                    duration
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                user_id,
                resource_id,
                campus_id,
                booking_date,
                start_time,
                duration
            ))

            connection.commit()

        except sqlite3.Error as error:

            messagebox.showerror(
                "Database Error",
                f"Could not save booking.\n\n{error}",
                parent=self.root
            )
            return

        finally:
            connection.close()

        messagebox.showinfo(
            "Booking Successful",
            "Your booking has been saved successfully.",
            parent=self.root
        )

        self.root.destroy()
