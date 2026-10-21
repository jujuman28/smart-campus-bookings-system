import tkinter as tk
import sqlite3


class SystemOperatorDashboard:

    def __init__(self, root, username):

        self.root = root
        self.username = username

        self.root.title("Smart Campus - System Operator")
        self.root.geometry("800x550")
        self.root.resizable(False, False)

        # =========================
        # HEADING
        # =========================

        tk.Label(
            self.root,
            text="System Operator Dashboard",
            font=("Arial", 24, "bold")
        ).pack(pady=25)

        tk.Label(
            self.root,
            text=f"Welcome, {self.username}",
            font=("Arial", 14)
        ).pack(pady=5)

        # =========================
        # USERS BUTTON
        # =========================

        tk.Button(
            self.root,
            text="View Users",
            width=25,
            height=2,
            command=self.view_users
        ).pack(pady=15)

        # =========================
        # CAMPUSES BUTTON
        # =========================

        tk.Button(
            self.root,
            text="View Campuses",
            width=25,
            height=2,
            command=self.view_campuses
        ).pack(pady=15)

        # =========================
        # BOOKINGS BUTTON
        # =========================

        tk.Button(
            self.root,
            text="View All Bookings",
            width=25,
            height=2,
            command=self.view_bookings
        ).pack(pady=15)

        # =========================
        # LOGOUT BUTTON
        # =========================

        tk.Button(
            self.root,
            text="Logout",
            width=25,
            height=2,
            command=self.logout
        ).pack(pady=15)

    # =========================
    # VIEW USERS
    # =========================

    def view_users(self):

        window = tk.Toplevel(self.root)

        window.title("System Users")
        window.geometry("750x500")
        window.resizable(False, False)

        tk.Label(
            window,
            text="System Users",
            font=("Arial", 20, "bold")
        ).pack(pady=20)

        table_frame = tk.Frame(window)
        table_frame.pack()

        headings = [
            "User ID",
            "Name",
            "Username",
            "Role"
        ]

        for column, heading in enumerate(headings):

            tk.Label(
                table_frame,
                text=heading,
                font=("Arial", 10, "bold"),
                width=18,
                relief="solid"
            ).grid(
                row=0,
                column=column
            )

        connection = sqlite3.connect(
            "smart_campus.db"
        )

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                user_id,
                name,
                username,
                role
            FROM users
            ORDER BY user_id
        """)

        users = cursor.fetchall()

        connection.close()

        for row_number, user in enumerate(
            users,
            start=1
        ):

            for column, value in enumerate(user):

                tk.Label(
                    table_frame,
                    text=value,
                    width=18,
                    relief="solid"
                ).grid(
                    row=row_number,
                    column=column
                )

        tk.Button(
            window,
            text="Close",
            width=20,
            command=window.destroy
        ).pack(pady=25)

    # =========================
    # VIEW CAMPUSES
    # =========================

    def view_campuses(self):

        window = tk.Toplevel(self.root)

        window.title("Campuses")
        window.geometry("800x450")
        window.resizable(False, False)

        tk.Label(
            window,
            text="Campus Information",
            font=("Arial", 20, "bold")
        ).pack(pady=20)

        table_frame = tk.Frame(window)
        table_frame.pack()

        headings = [
            "Campus ID",
            "Campus",
            "Max Duration",
            "Start Hour",
            "End Hour"
        ]

        for column, heading in enumerate(headings):

            tk.Label(
                table_frame,
                text=heading,
                font=("Arial", 10, "bold"),
                width=16,
                relief="solid"
            ).grid(
                row=0,
                column=column
            )

        connection = sqlite3.connect(
            "smart_campus.db"
        )

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                campus_id,
                campus_name,
                max_duration,
                start_hour,
                end_hour
            FROM campuses
            ORDER BY campus_id
        """)

        campuses = cursor.fetchall()

        connection.close()

        for row_number, campus in enumerate(
            campuses,
            start=1
        ):

            for column, value in enumerate(campus):

                tk.Label(
                    table_frame,
                    text=value,
                    width=16,
                    relief="solid"
                ).grid(
                    row=row_number,
                    column=column
                )

        tk.Button(
            window,
            text="Close",
            width=20,
            command=window.destroy
        ).pack(pady=25)

    # =========================
    # VIEW BOOKINGS
    # =========================

    def view_bookings(self):

        window = tk.Toplevel(self.root)

        window.title("All Bookings")
        window.geometry("1000x500")
        window.resizable(False, False)

        tk.Label(
            window,
            text="All System Bookings",
            font=("Arial", 20, "bold")
        ).pack(pady=20)

        table_frame = tk.Frame(window)
        table_frame.pack()

        headings = [
            "Booking ID",
            "User",
            "Resource",
            "Campus",
            "Date",
            "Start Time",
            "Duration"
        ]

        for column, heading in enumerate(headings):

            tk.Label(
                table_frame,
                text=heading,
                font=("Arial", 10, "bold"),
                width=14,
                relief="solid"
            ).grid(
                row=0,
                column=column
            )

        connection = sqlite3.connect(
            "smart_campus.db"
        )

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                bookings.booking_id,
                users.username,
                resources.resource_name,
                campuses.campus_name,
                bookings.booking_date,
                bookings.start_time,
                bookings.duration

            FROM bookings

            JOIN users
            ON bookings.user_id = users.user_id

            JOIN resources
            ON bookings.resource_id = resources.resource_id

            JOIN campuses
            ON bookings.campus_id = campuses.campus_id

            ORDER BY bookings.booking_date,
                     bookings.start_time
        """)

        bookings = cursor.fetchall()

        connection.close()

        if len(bookings) == 0:

            tk.Label(
                window,
                text="No bookings have been made yet.",
                font=("Arial", 12)
            ).pack(pady=30)

        else:

            for row_number, booking in enumerate(
                bookings,
                start=1
            ):

                for column, value in enumerate(booking):

                    tk.Label(
                        table_frame,
                        text=value,
                        width=14,
                        relief="solid"
                    ).grid(
                        row=row_number,
                        column=column
                    )

        tk.Button(
            window,
            text="Close",
            width=20,
            command=window.destroy
        ).pack(pady=25)

    # =========================
    # LOGOUT
    # =========================

    def logout(self):

        self.root.destroy()