# =========================
# BASE USER CLASS
# =========================

class User:

    def __init__(self, name, username, password):

        self.name = name
        self.username = username
        self.password = password


# =========================
# LECTURER
# =========================

class Lecturer(User):

    def __init__(self, name, username, password):

        super().__init__(
            name,
            username,
            password
        )

        self.role = "Lecturer"


# =========================
# CAMPUS ADMINISTRATOR
# =========================

class CampusAdministrator(User):

    def __init__(self, name, username, password):

        super().__init__(
            name,
            username,
            password
        )

        self.role = "Campus Administrator"


# =========================
# SYSTEM OPERATOR
# =========================

class SystemOperator(User):

    def __init__(self, name, username, password):

        super().__init__(
            name,
            username,
            password
        )

        self.role = "System Operator"