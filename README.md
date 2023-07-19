# Trusted Traveler Scheduler

![image](https://github.com/everettsouthwick/trusted-traveler-scheduler/assets/8216991/242646d9-6343-4919-a214-75b5b512d65a)

This script will automatically fetch new appointment dates/times for the configured location(s) from the Trusted Traveler Program API. You can use this to schedule Global Entry, NEXUS, SENTRI, or FAST appointments, provided the enrollment center you have configured offers the service.

## Table of Contents
* [Installation](#installation)
    * [Prerequisites](#prerequisites)
* [Usage](#usage)
    * [Docker](#docker)
        * [Pulling the image](#pulling-the-image)
        * [Running the Container](#running-the-container)
* [Configuration](#configuration)
    * [Locations](#locations)
* [Credits](#credits)

## Installation

### Prerequisites

- [Python 3.7+][0]
- [Pip][1]

1. First download the script to your machine and enter into the resulting directory:

```shell
git clone https://github.com/everettsouthwick/trusted-traveler-scheduler.git
cd trusted-traveler-scheduler
```
2. Then install the required packages to run the script:

```shell
pip install -r requirements.txt
```

## Usage
To use the script, run the following command:
```shell
python ttp.py [-d CURRENT_APPOINTMENT_DATE] [-l LOCATION_IDS] [-n NOTIFICATION_LEVEL] 
    [-u NOTIFICATION_URLS] [-r RETRIEVAL_INTERVAL] [-s START_APPOINTMENT_TIME] 
    [-e END_APPOINTMENT_TIME]
```
All of the arguments are optional, and will take precedence over the values supplied in `config.json`, with the exception of `location_ids` and `notification_urls` which will merge the values into a single list.

For example, the following command would retrieve appointments before December 31, 2023 for locations 5004 and 5140 and send notifications to the two Discord URLs every 5 minutes if the appointment time is between 8:00 AM and 8:00 PM:
```shell
python ttp.py -d "December 31, 2023" -l 5004,5140 -n 1 
    -u discord://id/token,discord://id/token -r 5m -s 08:00
    -e 20:00
```

For complete documentation, you can use the following command:
```shell
python ttp.py -h
```

### Docker

#### Pulling the image

The script can be configured to run in [Docker][2]. You can pull the latest container image from the [Docker repository][3] by running the following command:

```shell
docker pull ecsouthwick/trusted-traveler-scheduler
```
To pull the develop branch from the Docker repository, add the `:develop` tag to the above command:

```shell
docker pull ecsouthwick/trusted-traveler-scheduler:develop
```

#### Running the Container

Once you have pulled the image from docker, you may use the following command to run the container:

```shell
docker run -d ecsouthwick/trusted-traveler-scheduler [-d CURRENT_APPOINTMENT_DATE] [-l LOCATION_IDS] 
    [-n NOTIFICATION_LEVEL] [-u NOTIFICATION_URLS] [-r RETRIEVAL_INTERVAL] [-s START_APPOINTMENT_TIME] 
    [-e END_APPOINTMENT_TIME]
```
Optionally, you may attach your `config.json` file to the container to utilize your configuration settings.

```shell
docker run -d --name ttp --volume /path/to/config.json:/app/config.json ecsouthwick/trusted-traveler-scheduler
```

**Note**: The recommended restart policy for the container is `on-failed` or `no`.

## Configuration

1. Copy `config.example.json` to `config.json`. 
2. See [CONFIGURATION.md](CONFIGURATION.md) for detailed instructions on setting up `config.json`.

### Locations

For information on the list of applicable locations, see [LOCATIONS.md](LOCATIONS.md).

## Credits

- [Drewster727][4] for their `goes-notify` repository which was used for initial testing of the Trusted Traveler Program API.
- [jdholtz][5] for their work on `auto-southwest-check-in` which in part influenced the logic and overall structure of this project.

[0]: https://www.python.org/downloads/ "Python 3.7+"
[1]: https://pip.pypa.io/en/stable/installation/	"Pip"
[2]: https://www.docker.com/	"Docker"
[3]: https://hub.docker.com/r/ecsouthwick/trusted-traveler-scheduler	"Docker repository"
[4]: https://github.com/Drewster727	"Drewster727"
[5]: https://github.com/jdholtz	"jdholtz"
