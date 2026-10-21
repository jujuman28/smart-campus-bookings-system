from datetime import datetime


class BookingRules:

    def __init__(self, campus_name, max_duration, start_hour, end_hour):
        self.campus_name = campus_name
        self.max_duration = max_duration
        self.start_hour = start_hour
        self.end_hour = end_hour

    def check_duration(self, duration):
        if duration <= 0:
            return False, "Booking duration must be greater than 0 hours."

        if duration > self.max_duration:
            return False, (
                f"{self.campus_name} allows a maximum booking "
                f"duration of {self.max_duration} hours."
            )

        return True, "Duration is valid."

    def check_time(self, start_time, duration):
        try:
            booking_time = datetime.strptime(start_time, "%H:%M")
        except ValueError:
            return False, "Please enter the time in HH:MM format."

        start_hour = booking_time.hour
        end_hour = start_hour + duration

        if start_hour < self.start_hour:
            return False, (
                f"Bookings at {self.campus_name} can only start "
                f"from {self.start_hour}:00."
            )

        if end_hour > self.end_hour:
            return False, (
                f"Bookings at {self.campus_name} must end "
                f"by {self.end_hour}:00."
            )

        return True, "Booking time is valid."

    def validate_booking(self, start_time, duration):
        duration_valid, duration_message = self.check_duration(duration)

        if not duration_valid:
            return False, duration_message

        time_valid, time_message = self.check_time(
            start_time,
            duration
        )

        if not time_valid:
            return False, time_message

        return True, "Booking follows the campus policy."