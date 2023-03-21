"""Primary script entrypoint where arguments are processed and locations are set up."""

import sys
from typing import List
from .config import Config
from multiprocessing import Process
import apprise

__version__ = "v1.0"

__doc__ = """
Retrieve schedules from locations:
    python3 ttp.py LOCATION_ID LOCATION_ID ...

Options:
    --test-notifications Test the notification URLs configuration and exit
    -h, --help           Display this help and exit
    -v, --version        Display version information and exit

For more information, check out https://github.com/everettsouthwick/trusted-traveler-scheduler#readme"""

def send_notification(body: str, config) -> None:
    print(body)

    title = "Trusted Traveler Scheduler"

    apobj = apprise.Apprise(config.notification_urls)
    apobj.notify(title=title, body=body, body_format=apprise.NotifyFormat.TEXT)

def print_version():
    print("Trusted Traveler Scheduler " + __version__)


def print_usage():
    print_version()
    print(__doc__)


def check_flags(arguments: List[str]) -> None:
    """Checks for version and help flags and exits the script on success"""
    if "--version" in arguments or "-v" in arguments:
        print_version()
        sys.exit()
    elif "--help" in arguments or "-h" in arguments:
        print_usage()
        sys.exit()

def set_up_locations(config: Config) -> None:
    # pylint:disable=import-outside-toplevel
    from .schedule_retriever import ScheduleRetriever

    for location_id in config.location_ids:
        schedule_retriever = ScheduleRetriever(config)

        # Start each location in a separate process to run them in parallel
        process = Process(
            target=schedule_retriever.monitor_location,
            args=(location_id,),
        )
        process.start()

def set_up(arguments: List[str]):
    """Initialize a specific Schedule Retriever based on the arguments passed in"""

    # Imported here to avoid needing dependencies to retrieve the script's
    # version or usage
    # pylint:disable=import-outside-toplevel
    from .config import Config
    from .schedule_retriever import ScheduleRetriever

    config = Config()

    if "--test-notifications" in arguments:
        schedule_retriever = ScheduleRetriever(config)

        print("Sending test notifications...")
        schedule_retriever.notification_handler.send_notification("This is a test message")
        sys.exit()

    for argument in arguments:
        if argument not in config.location_ids:
            config.location_ids.append(argument)

    set_up_locations(config)

def main(arguments: List[str]) -> None:
    check_flags(arguments)
    set_up(arguments)