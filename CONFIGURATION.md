# Configuration
This guide contains all the information you need to configure `trusted-traveler-scheduler` to your specifications. An example file of the configuration can be found at [config.example.json](config.example.json).

## Current Appointment Date

Default: None

Type: String

This represents the date of your current appointment if you have one. If you do not have one, leave it as an empty string. This value is used to determine whether to notify you if a new appointment is found. If it is later than your current appointment date, it will not notify you.

```json
{
	"current_appointment_date": "January 1, 2024"
}
```

This above configuration will notify you if a new appointment is found for December 1, 2023, but will not notify you if an appointment is found for January 2, 2024.

**Note:** This must be in the format of Month Day, Year (e.g. January 1, 2024).

## Locations

Default: []

Type: List or Integer

This represents the IDs of the enrollment centers you wish to monitor. This can either be a list of locations, or a singular location represented by an integer. This list is used in addition to whatever arguments you pass in at run-time of the script. For more information on locations, please see [LOCATIONS.md](LOCATIONS.MD).

```json
{
  "location_ids": [ 5140 ]
}
```

or

```json
{  
    "location_ids": 5140
}
```

## Notifications

### Notification Level
Default: 1

Type: Integer

This indicates the notification sensitivity you wish to receive. 
```json
{
  "notification_level": 1
}
```
Level 1 means you receive notifications when new appointments are found.

Level 2 means you receive notifications only when errors occur.

### Notification URLs

Default: []

Type: List or String

This uses the [Apprise Library][0] to generate notifications that are pushed to you based on the notification level you have elected to receive. You can find more information about notifications through the [Apprise README.md][1]

```json
{
  "notification_urls": "service://my_service_url"
}
```

or

```json
{
  "notification_urls": [
    "service://my_first_service_url",
    "service://my_second_service_url"
  ]
}
```

### Test Notifications
To test your notification configuration, run the following command:
```shell
python tty.py --test-notifications
```

## Retrieval Interval
Default: 5 minutes

Type: String

This indicates how often the script will fetch new appointments from the monitored locations. To disable automatic retrieval, set this to "0m".

```json
{
    "retrieval_interval": "5m"
}
```

## Appointment Times

### Start Appointment Time
Default: 00:00

Type: String

This indicates the earliest appointment you would like to be notified for. To be notified for all appointments, set this to "00:00".

```json
{
    "start_appointment_time": "06:00"
}
```

### End Appointment Time
Default: 23:59

Type: String

This indicates the latest appointment you would like to be notified for. To be notified for all appointments, set this to "23:59".

```json
{
    "end_appointment_time": "20:00"
}
```



[0]: https://github.com/caronc/apprise
[1]: https://github.com/caronc/apprise#supported-notifications