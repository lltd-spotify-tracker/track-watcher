from datetime import datetime
import pytz


def convert_to_unix(utc_string):
    utc_datetime = datetime.strptime(utc_string, "%Y-%m-%dT%H:%M:%S.%fZ")

    # Make the datetime object timezone aware
    utc_datetime = utc_datetime.replace(tzinfo=pytz.UTC)

    # Convert the datetime object to a Unix timestamp in milliseconds
    return int(utc_datetime.timestamp() * 1000)


def convert_to_aus_tz(unix_timestamp):
    timestamp_datetime = datetime.fromtimestamp(unix_timestamp / 1000)

    # Make the datetime object timezone aware
    timestamp_datetime = timestamp_datetime.replace(tzinfo=pytz.UTC)

    # Convert the datetime object to your current timezone
    timestamp_datetime = timestamp_datetime.astimezone(pytz.timezone('Australia/Sydney')) # replace 'Asia/Kolkata' with your timezone

    # Convert the datetime object to a string
    return timestamp_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")