import tkinter as tk
from tkinter import messagebox
import sqlite3

from gui.booking import BookingWindow


class LecturerDashboard:

    def __init__(self, root, username):

        self.root = root
        self.username = username

        self.root.title("Smart Campus - Lecturer Dashboard")
        self.root.geometry("800x550")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f4f8")

        # Main heading
        heading = tk.Label(
            self.root,
            text="SMART CAMPUS",
            font=("Arial", 26, "bold"),
            bg="#17365d",
            fg="white",
            pady=20
        )
        heading.pack(fill="x")

        # Dashboard subtitle
        subtitle = tk.Label(
            self.root,
            text="Lecturer Dashboard",
            font=("Arial", 18, "bold"),
            bg="#f0f4f8",
            fg="#17365d"
        )
        subtitle.pack(pady=(25, 5))

        # Welcome message
        welcome = tk.Label(
            self.root,
            text=f"Welcome, {self.username}!",
            font=("Arial", 13),
            bg="#f0f4f8",
            fg="#333333"
        )
        welcome.pack(pady=5)

        # Buttons container
        button_frame = tk.Frame(
            self.root,
            bg="#f0f4f8"
        )
        button_frame.pack(pady=20)

        # Make booking
        tk.Button(
            button_frame,
            text="Make a Booking",
            font=("Arial", 12, "bold"),
            width=25,
            height=2,
            bg="#2874a6",
            fg="white",
            command=self.make_booking
        ).pack(pady=8)

        # View bookings
        tk.Button(
            button_frame,
            text="My Bookings",
            font=("Arial", 12, "bold"),
            width=25,
            height=2,
            bg="#2874a6",
            fg="white",
            command=self.view_bookings
        ).pack(pady=8)

        # Logout
        tk.Button(
            button_frame,
            text="Logout",
            font=("Arial", 12, "bold"),
            width=25,
            height=2,
            bg="#922b21",
            fg="white",
            command=self.logout
        ).pack(pady=8)

        # Footer
        footer = tk.Label(
            self.root,
            text="Smart Campus Resource Booking System",
            font=("Arial", 9),
            bg="#f0f4f8",
            fg="#666666"
        )
        footer.pack(side="bottom", pady=12)

    # =========================
    # MAKE BOOKING
    # =========================

    def make_booking(self):

        booking_window = tk.Toplevel(self.root)

        BookingWindow(
            booking_window,
            self.username
        )

    # =========================
    # VIEW BOOKINGS
    # =========================

    def view_bookings(self):

        booking_window = tk.Toplevel(self.root)

        booking_window.title("My Bookings")
        booking_window.geometry("850x500")
        booking_window.resizable(False, False)

        # Heading
        tk.Label(
            booking_window,
            text="My Bookings",
            font=("Arial", 22, "bold")
        ).pack(pady=20)

        # Create frame for bookings
        table_frame = tk.Frame(booking_window)
        table_frame.pack(pady=10)

        # Table headings
        headings = [
            "Booking ID",
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
                width=15,
                relief="solid"
            ).grid(
                row=0,
                column=column
            )

        # Connect to database
        connection = sqlite3.connect(
            "smart_campus.db"
        )

        cursor = connection.cursor()

        # Get the lecturer's bookings
        cursor.execute("""
            SELECT
                bookings.booking_id,
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

            WHERE users.username = ?

            ORDER BY bookings.booking_date, bookings.start_time
        """, (self.username,))

        bookings = cursor.fetchall()

        connection.close()

        # Display bookings
        if len(bookings) == 0:

            tk.Label(
                booking_window,
                text="You have no bookings yet.",
                font=("Arial", 12)
            ).pack(pady=30)

        else:

            for row_number, booking in enumerate(bookings, start=1):

                for column, value in enumerate(booking):

                    tk.Label(
                        table_frame,
                        text=value,
                        width=15,
                        relief="solid"
                    ).grid(
                        row=row_number,
                        column=column
                    )

        # Close button

        tk.Button(
            booking_window,
            text="Cancel Booking",
            width=20,
            command=lambda: self.cancel_booking(booking_window)
        ).pack(pady=5)

        tk.Button(
            booking_window,
            text="Close",
            width=20,
            command=booking_window.destroy
        ).pack(pady=10)

    def cancel_booking(self, booking_window):

        cancel_window = tk.Toplevel(booking_window)

        cancel_window.title("Cancel Booking")
        cancel_window.geometry("400x250")
        cancel_window.resizable(False, False)

        tk.Label(
            cancel_window,
            text="Cancel a Booking",
            font=("Arial", 18, "bold")
        ).pack(pady=20)

        tk.Label(
            cancel_window,
            text="Enter the Booking ID you want to cancel:"
        ).pack(pady=5)

        booking_id_entry = tk.Entry(
            cancel_window,
            width=25
        )
        booking_id_entry.pack(pady=10)

        def confirm_cancellation():

            booking_id = booking_id_entry.get().strip()

            if not booking_id.isdigit():
                messagebox.showerror(
                    "Error",
                    "Please enter a valid Booking ID.",
                    parent=cancel_window
                )
                return

            connection = sqlite3.connect("smart_campus.db")
            cursor = connection.cursor()

            cursor.execute("""
                SELECT booking_id
                FROM bookings
                JOIN users
                ON bookings.user_id = users.user_id
                WHERE bookings.booking_id = ?
                AND users.username = ?
            """, (int(booking_id), self.username))

            booking = cursor.fetchone()

            if booking is None:
                connection.close()

                messagebox.showerror(
                    "Error",
                    "Booking not found or it does not belong to you.",
                    parent=cancel_window
                )
                return

            answer = messagebox.askyesno(
                "Confirm Cancellation",
                "Are you sure you want to cancel this booking?",
                parent=cancel_window
            )

            if not answer:
                connection.close()
                return

            cursor.execute("""
                DELETE FROM bookings
                WHERE booking_id = ?
            """, (int(booking_id),))

            connection.commit()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Booking cancelled successfully.",
                parent=cancel_window
            )

            cancel_window.destroy()
            booking_window.destroy()

        tk.Button(
            cancel_window,
            text="Confirm Cancellation",
            width=22,
            command=confirm_cancellation
        ).pack(pady=15)

    # =========================
    # LOGOUT
    # =========================

    def logout(self):

        self.root.destroy()