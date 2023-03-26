import json
import re
import os
import sys
from typing import Any, Dict
from datetime import datetime

from .notification_level import NotificationLevel

CONFIG_FILE_NAME = "config.json"
LOCATION_FILE_NAME = "locations.json"

class Config:
    def __init__(self):
        # Default values are set
        self.current_appointment_date = None
        self.location_ids = []
        self.notification_level = NotificationLevel.INFO
        self.notification_urls = []
        self.retrieval_interval = 300
       
        # Read the config file
        config = self._get_config()
        self.locations = self._get_locations()

        # Set the configuration values if provided
        try:
            self._parse_config(config)
        except TypeError as err:
            print("Error in configuration file:")
            print(err)
            sys.exit()

    def _get_config(self) -> Dict[str, Any]:
        project_dir = os.path.dirname(os.path.dirname(__file__))
        config_file = project_dir + "/" + CONFIG_FILE_NAME

        config = {}
        try:
            with open(config_file) as file:
                config = json.load(file)
        except FileNotFoundError:
            pass

        return config
    
    def _get_locations(self):
        project_dir = os.path.dirname(os.path.dirname(__file__))
        locations_file = project_dir + "/utils/" + LOCATION_FILE_NAME

        locations = {}
        try:
            with open(locations_file, encoding="utf-8") as file:
                locations = json.load(file)
        except FileNotFoundError:
            pass

        return locations
    
    def convert_to_seconds(self, time: str) -> int:
        match = re.match(r'^(\d+)([smhd])$', time.lower())
        
        if not match:
            raise ValueError(f"'retrieval_interval' must be in the format of <integer><unit>. (e.g. 45s (seconds), 30m (minutes), 2h (hours), 1d (days))")
        
        value, unit = int(match.group(1)), match.group(2)

        if unit == "s":
            return value
        elif unit == "m":
            return value * 60
        elif unit == "h":
            return value * 3600
        elif unit == "d":
            return value * 86400
        else:
            raise ValueError(f"'retrieval_interval' invalid time unit: {unit}. Accepted units: s (seconds), m (minutes), h (hours), d (days).")

    # This method ensures the configuration values are correct and the right types.
    # Defaults are already set in the constructor to ensure a value is never null.
    def _parse_config(self, config: Dict[str, Any]) -> None:
        if "current_appointment_date" in config and config["current_appointment_date"] != "":
            self.current_appointment_date = config["current_appointment_date"]

            try:
                self.current_appointment_date = datetime.strptime(self.current_appointment_date, '%B %d, %Y')
            except:
                raise TypeError("'current_appointment_date' must be in the format of Month Day, Year (e.g. January 1, 2024)")
        
        if "location_ids" in config:
            self.location_ids = config["location_ids"]

            if not isinstance(self.location_ids, (list, int)):
                raise TypeError("'location_ids' must be a list or integer")
            
        if "notification_level" in config:
            self.notification_level = config["notification_level"]

            if not isinstance(self.notification_level, int):
                raise TypeError("'notification_level' must be an integer")

        if "notification_urls" in config:
            self.notification_urls = config["notification_urls"]

            if not isinstance(self.notification_urls, (list, str)):
                raise TypeError("'notification_urls' must be a list or string")

        if "retrieval_interval" in config:
            self.retrieval_interval = config["retrieval_interval"]

            if not isinstance(self.retrieval_interval, str):
                raise TypeError("'retrieval_interval' must be a string")
            
            try:
                self.retrieval_interval = self.convert_to_seconds(self.retrieval_interval)
            except ValueError as err:
                raise TypeError(err)
                
                
