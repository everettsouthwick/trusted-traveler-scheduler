"""Primary script entrypoint where arguments are processed and locations are set up."""

import sqlite3
from .config import Config
from multiprocessing import Process

def create_database(filename: str) -> None:
    """
    Creates a new SQLite database file with the given filename if it does not already exist,
    and creates a table named 'appointments' with columns 'id', 'location_id', and 'start_time'.
    """
    conn = sqlite3.connect(filename)

    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS appointments
                      (id INTEGER PRIMARY KEY,
                       location_id INTEGER,
                       start_time TEXT)'''
                       )

    conn.commit()
    conn.close()

def set_up(config: Config) -> None:
    """
    Sets up the scheduler by creating a ScheduleRetriever for each location ID in the given config,
    and starting a separate process to monitor each location in parallel.
    """
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

def main(config: Config) -> None:
    """
    Entry point for the Trusted Traveler Scheduler application. Creates a new SQLite database file
    named 'ttp.db' if it does not already exist, and sets up the scheduler by creating a ScheduleRetriever
    for each location ID in the given config, and starting a separate process to monitor each location in parallel.

    :param config: A Config object containing the configuration for the scheduler.
    """
    create_database('ttp.db')
    set_up(config)