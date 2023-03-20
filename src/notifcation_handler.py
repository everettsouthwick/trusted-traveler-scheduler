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

    def _get_location_name(self, location_id: str) -> str:
        result = next((location for location in self.locations if str(location["id"]) == location_id), None)
        return result['name'] if result else ''

    def send_notification(self, body: str, level: int = 1) -> None:
        print(body)

        # Check the level to see if we still want to send it. If level is none, it means
        # the message will always be printed. For example, this is used when testing notifications.
        if level and level < self.notification_level:
            return

        title = "Trusted Traveler Scheduler"

        apobj = apprise.Apprise(self.notification_urls)
        apobj.notify(title=title, body=body, body_format=apprise.NotifyFormat.TEXT)

    def new_appointment(self, location_id: str, appointments: List[Schedule]) -> None:
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

                appointment_message += f"- {datetime.strftime(appointment.appointment_date, '%A, %B %d, %Y')} [{times}]\n"

        self.send_notification(appointment_message, NotificationLevel.INFO)