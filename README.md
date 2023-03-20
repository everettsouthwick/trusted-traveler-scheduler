# Trusted Traveler Scheduler

Running this script will automatically check configured location(s) for new appointments for Global Entry, NEXUS, SENTRI, and FAST.

## Table of Contents
- [Installation](#installation)
    * [Pre-requisites](#pre-requisites)
- [Using the Script](#using-the-script)
- [Credits](#credits)

## Installation

### Pre-requisities

- [Python 3.7+][0]
- [Pip][1]

First, download the script onto your computer
```shell
git clone https://github.com/everettsouthwick/trusted-traveler-scheduler.git
cd trusted-traveler-scheduler
```
Then, install the needed packages for the script
```shell
pip install -r requirements.txt
```

## Using the Script
To monitor a location, run the following command:
```shell
python3 ttp.py LOCATION_ID LOCATION_ID ...
```

For the complete help documentation, run:
```shell
python ttp.py --help
```

## Locations

For information on how to set up the configuration for locations, see [LOCATIONS.md](LOCATIONS.md)

## Credits

- [Drewster727][2] for their work on [goes-notify][3] which served as a starting point for the logic of pulling the schedule from the Trusted Traveler Program API.
- [jdholtz][4] for their work on [auto-southwest-check-in][5] which greatly influenced the layout and structure of the project.

[0]: https://www.python.org/downloads/
[1]: https://pip.pypa.io/en/stable/installation/
[2]: https://github.com/Drewster727
[3]: https://github.com/Drewster727/goes-notify
[4]: https://github.com/jdholtz
[5]: https://github.com/jdholtz/auto-southwest-check-in