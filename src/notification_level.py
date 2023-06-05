from enum import IntEnum

class NotificationLevel(IntEnum):
    """
    An enumeration representing the different levels of notification that can be used in the application.

    The available notification levels are:
    - INFO: Used for general information messages.
    - ERROR: Used for error messages.
    """
    INFO = 1
    ERROR = 2