import json
import os
import sys
from typing import Any, Dict

from .notification_level import NotificationLevel

CONFIG_FILE_NAME = "config.json"
LOCATION_FILE_NAME = "locations.json"

class Config:
    def __init__(self):
        # Default values are set
        self.location_ids = []
        self.notification_urls = []
        self.notification_level = NotificationLevel.INFO
        self.retrieval_interval = 24
        self.locations = []
       
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
        locations_file = project_dir + "/util/" + LOCATION_FILE_NAME

        locations = {}
        try:
            with open(locations_file, encoding="utf-8") as file:
                locations = json.load(file)
        except FileNotFoundError:
            pass

        return locations

    # This method ensures the configuration values are correct and the right types.
    # Defaults are already set in the constructor to ensure a value is never null.
    def _parse_config(self, config: Dict[str, Any]) -> None:
        if "location_ids" in config:
            self.location_ids = config["location_ids"]

            if not isinstance(self.location_ids, (list, str)):
                raise TypeError("'location_ids' must be a list or string")

        if "notification_urls" in config:
            self.notification_urls = config["notification_urls"]

            if not isinstance(self.notification_urls, (list, str)):
                raise TypeError("'notification_urls' must be a list or string")
            
        if "notification_level" in config:
            self.notification_level = config["notification_level"]

            if not isinstance(self.notification_level, int):
                raise TypeError("'notification_level' must be an integer")

        if "retrieval_interval" in config:
            self.retrieval_interval = config["retrieval_interval"]

            if not isinstance(self.retrieval_interval, int):
                raise TypeError("'retrieval_interval' must be an integer")

            if self.retrieval_interval < 1:
                print(
                    f"Setting 'retrieval_interval' to one as {self.retrieval_interval} hours is too low"
                )
                self.retrieval_interval = 1
