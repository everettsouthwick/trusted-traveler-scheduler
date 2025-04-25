# Trusted Traveler Scheduler

![image](https://github.com/everettsouthwick/trusted-traveler-scheduler/assets/8216991/242646d9-6343-4919-a214-75b5b512d65a)

## Cloud-Hosted Option

A hosted version of this tool is available at [GoGlobalEntry.com](https://www.goglobalentry.com) if you prefer not to set up the script yourself.

## Self-Hosted Option

You can run this script locally to automatically fetch new appointment dates/times for the configured location(s) from the Trusted Traveler Program API. This works for Global Entry, NEXUS, SENTRI, or FAST appointments, provided the enrollment center you select offers the service.

## Table of Contents
* [Cloud-Hosted Option](#cloud-hosted-option)
* [Self-Hosted Option](#self-hosted-option)
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
