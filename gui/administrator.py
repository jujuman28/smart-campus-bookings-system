import tkinter as tk
import sqlite3


class AdministratorDashboard:

    def __init__(self, root, username):

        self.root = root
        self.username = username

        self.root.title("Smart Campus - Administrator")
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        # Heading
        tk.Label(
            self.root,
            text="Administrator Dashboard",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        # Welcome message
        tk.Label(
            self.root,
            text=f"Welcome, {self.username}",
            font=("Arial", 14)
        ).pack(pady=5)

        # View bookings button
        tk.Button(
            self.root,
            text="View All Bookings",
            width=25,
            height=2,
            command=self.view_bookings
        ).pack(pady=15)

        # View resources button
        tk.Button(
            self.root,
            text="View Resources",
            width=25,
            height=2,
            command=self.view_resources
        ).pack(pady=15)

        # Logout button
        tk.Button(
            self.root,
            text="Logout",
            width=25,
            height=2,
            command=self.logout
        ).pack(pady=15)

    # =========================
    # VIEW ALL BOOKINGS
    # =========================

    def view_bookings(self):

        window = tk.Toplevel(self.root)

        window.title("All Bookings")
        window.geometry("1000x500")
        window.resizable(False, False)

        tk.Label(
            window,
            text="All Resource Bookings",
            font=("Arial", 20, "bold")
        ).pack(pady=20)

        table_frame = tk.Frame(window)
        table_frame.pack()

        headings = [
            "ID",
            "Lecturer",
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
                users.name,
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
                text="There are no bookings yet.",
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
    # VIEW RESOURCES
    # =========================

    def view_resources(self):

        window = tk.Toplevel(self.root)

        window.title("Resources")
        window.geometry("700x500")
        window.resizable(False, False)

        tk.Label(
            window,
            text="Campus Resources",
            font=("Arial", 20, "bold")
        ).pack(pady=20)

        table_frame = tk.Frame(window)
        table_frame.pack()

        headings = [
            "Resource ID",
            "Resource",
            "Campus"
        ]

        for column, heading in enumerate(headings):

            tk.Label(
                table_frame,
                text=heading,
                font=("Arial", 10, "bold"),
                width=20,
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
                resources.resource_id,
                resources.resource_name,
                campuses.campus_name

            FROM resources

            JOIN campuses
            ON resources.campus_id = campuses.campus_id

            ORDER BY campuses.campus_name,
                     resources.resource_name
        """)

        resources = cursor.fetchall()

        connection.close()

        for row_number, resource in enumerate(
            resources,
            start=1
        ):

            for column, value in enumerate(resource):

                tk.Label(
                    table_frame,
                    text=value,
                    width=20,
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