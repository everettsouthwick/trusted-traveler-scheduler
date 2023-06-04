"""Primary script entrypoint where arguments are processed and locations are set up."""

import sqlite3
from .config import Config
from multiprocessing import Process

def create_database(filename: str) -> None:
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
    create_database('ttp.db')
    set_up(config)