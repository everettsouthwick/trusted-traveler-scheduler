class Schedule:
    """
    A class representing a schedule of appointments for a Trusted Traveler program.

    Attributes:
        appointment_date (str): The date of the appointment in the format 'YYYY-MM-DD'.
        appointment_times (list): A list of appointment times in the format 'HH:MM AM/PM'.
    """
    def __init__(self, appointment_date, appointment_times):
        # Default values are set
        self.appointment_date = appointment_date
        self.appointment_times = appointment_times