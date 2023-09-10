from __future__ import annotations
from datetime import datetime

from typing import TYPE_CHECKING, List

import apprise
from .schedule import Schedule

from .notification_level import NotificationLevel

if TYPE_CHECKING:  # pragma: no cover
    from .schedule_retriever import ScheduleRetriever


class NotificationHandler:
    """Handles all notifications that will be sent to the user either via Apprise or the console"""

    def __init__(self, schedule_retriever: ScheduleRetriever) -> None:
        self.schedule_retriever = schedule_retriever
        self.notification_urls = self.schedule_retriever.config.notification_urls
        self.notification_level = self.schedule_retriever.config.notification_level
        self.locations = self.schedule_retriever.config.locations

    def _get_location_name(self, location_id: int) -> str:
        """
        Returns the name of the location with the given ID.

        Args:
            location_id (int): The ID of the location.

        Returns:
            str: The name of the location with the given ID, or an empty string if no location was found.
        """
        result = next((location for location in self.locations if location["id"] == location_id), None)
        return result['name'] if result else ''

    def send_notification(self, body: str, level: int = 1) -> None:
        """
        Sends a notification to the user via Apprise or the console, depending on the configuration.

        Args:
            body (str): The message to send.
            level (int, optional): The level of the notification. If the level is less than the configured notification
                level, the notification will not be sent. Defaults to 1.
        """
        print(body)

        # Check the level to see if we still want to send it. If level is none, it means
        # the message will always be printed. For example, this is used when testing notifications.
        if level and level < self.notification_level:
            return

        title = "Trusted Traveler Scheduler"

        apobj = apprise.Apprise(self.notification_urls)
        result = apobj.notify(title=title, body=body, body_format=apprise.NotifyFormat.TEXT)

        # If you encounter Apprise errors, https://github.com/caronc/apprise/wiki/Development_LogCapture
        # may be useful.
        if result is None:
            print('error: No notifications sent (configuration error)')
        elif result is False:
            print('error: At least 1 notification failed to send')

    def new_appointment(self, location_id: int, appointments: List[Schedule]) -> None:
        """
        Sends a notification to the user if new appointments are available for the given location.

        Args:
            location_id (int): The ID of the location.
            appointments (List[Schedule]): A list of Schedule objects representing the new appointments.

        Returns:
            None
        """
        # Don't send notifications if no appointments are available
        if len(appointments) == 0:
            return

        appointment_message = f"New appointment(s) found for {self._get_location_name(location_id)}\n"
        for appointment in appointments:
                limited_times = appointment.appointment_times[:3]
                time_strings = [item.time().strftime('%I:%M %p') for item in limited_times]
                times = ", ".join(time_strings)

                if len(appointment.appointment_times) > 3:
                    times += f', and {len(appointment.appointment_times) - 3} more'

                appointment_message += f"- {datetime.strftime(appointment.appointment_date, '%a, %B %d, %Y')} [{times}]\n"

        self.send_notification(appointment_message, NotificationLevel.INFO)
