import sys
import time

from src.notifcation_handler import NotificationHandler
import requests
import apprise
from datetime import datetime
from typing import Any, Dict, List

from .config import Config

GOES_URL_FORMAT = 'https://ttp.cbp.dhs.gov/schedulerapi/slots?orderBy=soonest&limit=3&locationId={0}&minimum=1'

class ScheduleRetriever:
    """
    Retrieve schedule based on the location id provided.
    """

    def __init__(self, config: Config) -> None:
        self.config = config
        self.notification_handler = NotificationHandler(self)
        # self.checkin_scheduler = CheckInScheduler(self)

    def get_schedule(self, location_id: str) -> None:
        try:
            # obtain the json from the web url
            data = requests.get(GOES_URL_FORMAT.format(location_id)).json()

            # parse the json
            if not data:
                return

            current_apt = datetime.strptime('December 31, 2023', '%B %d, %Y')
            dates = []
            for o in data:
                if o['active']:
                    dt = o['startTimestamp'] #2017-12-22T15:15
                    dtp = datetime.strptime(dt, '%Y-%m-%dT%H:%M')
                    if current_apt > dtp:
                        dates.append(dtp.strftime('%A, %B %d @ %I:%M%p').encode('utf-8'))

            if not dates:
                return
        
        except OSError:
            return
        
        self.notification_handler.new_appointment(location_id, dates)
