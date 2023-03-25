"""Primary script entrypoint where arguments are processed and locations are set up."""

from .config import Config
from multiprocessing import Process

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
    set_up(config)