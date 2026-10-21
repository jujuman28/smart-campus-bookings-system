import sqlite3

from models import (
    Lecturer,
    CampusAdministrator,
    SystemOperator
)


class Authentication:

    def __init__(self, database_name="smart_campus.db"):
        self.database_name = database_name

    def login(self, username, password):

        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT user_id, name, username, password, role
            FROM users
            WHERE username = ?
        """, (username,))

        user = cursor.fetchone()

        connection.close()

        # Username does not exist
        if user is None:
            return None, "Username not found."

        user_id, name, username, stored_password, role = user

        # Check password
        if password != stored_password:
            return None, "Incorrect password."

        # Create the correct object based on the user's role
        if role == "Lecturer":

            logged_in_user = Lecturer(
                name,
                username,
                stored_password
            )

        elif role == "Campus Administrator":

            logged_in_user = CampusAdministrator(
                name,
                username,
                stored_password
            )

        elif role == "System Operator":

            logged_in_user = SystemOperator(
                name,
                username,
                stored_password
            )

        else:
            return None, "Invalid user role."

        return logged_in_user, "Login successful."