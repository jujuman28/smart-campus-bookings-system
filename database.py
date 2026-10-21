import sqlite3


# Connect to the database
def connect_database():
    connection = sqlite3.connect("smart_campus.db")
    return connection


# Create all required database tables
def create_tables():

    connection = connect_database()
    cursor = connection.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    # Campuses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS campuses (
            campus_id INTEGER PRIMARY KEY AUTOINCREMENT,
            campus_name TEXT UNIQUE NOT NULL,
            max_duration INTEGER NOT NULL,
            start_hour INTEGER NOT NULL,
            end_hour INTEGER NOT NULL
        )
    """)

    # Resources table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resources (
            resource_id INTEGER PRIMARY KEY AUTOINCREMENT,
            resource_name TEXT NOT NULL,
            campus_id INTEGER NOT NULL,
            FOREIGN KEY (campus_id) REFERENCES campuses(campus_id)
        )
    """)

    # Bookings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            resource_id INTEGER NOT NULL,
            campus_id INTEGER NOT NULL,
            booking_date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            duration INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (resource_id) REFERENCES resources(resource_id),
            FOREIGN KEY (campus_id) REFERENCES campuses(campus_id)
        )
    """)

    connection.commit()
    connection.close()


# Add the starting campuses
def add_default_campuses():

    connection = connect_database()
    cursor = connection.cursor()

    campuses = [
        ("Pretoria Campus", 2, 8, 18),
        ("Johannesburg Campus", 3, 8, 19),
        ("Cape Town Campus", 4, 7, 20)
    ]

    for campus in campuses:

        cursor.execute("""
            INSERT OR IGNORE INTO campuses
            (campus_name, max_duration, start_hour, end_hour)
            VALUES (?, ?, ?, ?)
        """, campus)

    connection.commit()
    connection.close()


# Add the starting resources
def add_default_resources():

    connection = connect_database()
    cursor = connection.cursor()

    resources = [
        ("Lecture Room 1", "Pretoria Campus"),
        ("Lecture Room 2", "Pretoria Campus"),
        ("Computer Lab 1", "Pretoria Campus"),
        ("Library", "Pretoria Campus"),

        ("Lecture Room 1", "Johannesburg Campus"),
        ("Computer Lab 1", "Johannesburg Campus"),
        ("Library", "Johannesburg Campus"),

        ("Lecture Room 1", "Cape Town Campus"),
        ("Computer Lab 1", "Cape Town Campus"),
        ("Laboratory 1", "Cape Town Campus")
    ]

    for resource_name, campus_name in resources:

        # Find the campus ID
        cursor.execute("""
            SELECT campus_id
            FROM campuses
            WHERE campus_name = ?
        """, (campus_name,))

        campus = cursor.fetchone()

        if campus is not None:

            campus_id = campus[0]

            # Check if resource already exists
            cursor.execute("""
                SELECT resource_id
                FROM resources
                WHERE resource_name = ?
                AND campus_id = ?
            """, (resource_name, campus_id))

            existing_resource = cursor.fetchone()

            if existing_resource is None:

                cursor.execute("""
                    INSERT INTO resources
                    (resource_name, campus_id)
                    VALUES (?, ?)
                """, (resource_name, campus_id))

    connection.commit()
    connection.close()


# Add the starting users
def add_default_users():

    connection = connect_database()
    cursor = connection.cursor()

    users = [
        ("Lecturer User", "lecturer", "1234", "Lecturer"),
        ("Campus Administrator", "admin", "1234", "Campus Administrator"),
        ("System Operator", "operator", "1234", "System Operator")
    ]

    for user in users:

        cursor.execute("""
            INSERT OR IGNORE INTO users
            (name, username, password, role)
            VALUES (?, ?, ?, ?)
        """, user)

    connection.commit()
    connection.close()


# Run database setup
def setup_database():

    create_tables()
    add_default_campuses()
    add_default_resources()
    add_default_users()

    print("Database setup completed successfully.")


# Run this file directly
if __name__ == "__main__":
    setup_database()