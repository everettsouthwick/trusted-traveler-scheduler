import time

from typing import List

from .schedule import Schedule

from .notifcation_handler import NotificationHandler
import requests
from datetime import datetime

from .config import Config

GOES_URL_FORMAT = 'https://ttp.cbp.dhs.gov/schedulerapi/slots?orderBy=soonest&limit=250&locationId={0}&minimum=1'

class ScheduleRetriever:
    """
    Retrieve schedule based on the location id provided.
    """

    def __init__(self, config: Config) -> None:
        self.config = config
        self.notification_handler = NotificationHandler(self)

    def _evaluate_timestamp(self, schedule: List[Schedule], timestamp: str):
        parsed_date = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M')

        for dates in schedule:
            if dates.appointment_date.date() == parsed_date.date():
                dates.appointment_times.append(parsed_date)
                return schedule
        
        if self.config.current_appointment_date is None or self.config.current_appointment_date > parsed_date:
            schedule.append(Schedule(parsed_date, [parsed_date]))

        return schedule

    def _get_schedule(self, location_id: int) -> None:
        try:
            appointments = requests.get(GOES_URL_FORMAT.format(location_id)).json()

            if not appointments:
                return
            
            schedule = []
            for appointment in appointments:
                if appointment['active']:
                    schedule = self._evaluate_timestamp(schedule, appointment['startTimestamp'])

            if not schedule:
                return
            
            self.notification_handler.new_appointment(location_id, schedule)
            
        except OSError:
            return
        
    def monitor_location(self, location_id: int) -> None:
            if self.config.retrieval_interval == 0:
                self._get_schedule(location_id)
                return

            while True:
                time_before = datetime.utcnow()

                self._get_schedule(location_id)

                # Account for the time it takes to retrieve the location when
                # deciding how long to sleep
                time_after = datetime.utcnow()
                time_taken = (time_after - time_before).total_seconds()
                time.sleep(self.config.retrieval_interval - time_taken)