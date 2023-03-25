# Trusted Traveler Scheduler

This script will automatically fetch new appointment dates/times for the configured location(s) from the Trusted Traveler Program API. You can use this to schedule Global Entry, NEXUS, SENTRI, or FAST appointments, provided the enrollment center you have configured offers the service.

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
    [-u NOTIFICATION_URLS] [-r RETRIEVAL_INTERVAL]
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
    [-n NOTIFICATION_LEVEL] [-u NOTIFICATION_URLS] [-r RETRIEVAL_INTERVAL]
```
Optionally, you may attach your `config.json` file to the container to utilize your configuration settings.

```shell
docker run -d ecsouthwick/trusted-traveler-scheduler --volume /path/to/config.json:/app/config.json
```

**Note**: The recommended restart policy for the container is `on-failed` or `no`.

## Configuration

1. Copy `config.example.json` to `config.json`. 
2. See [CONFIGURATION.md](CONFIGURATION.md) for detailed instructions on setting up `config.json`.



**Note**: If you are using Docker and make changes to your `config.json`, you *must* re-build the container to use the updated `config.json`.

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
