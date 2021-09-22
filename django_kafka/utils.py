from datetime import datetime

''' datetime_str = '2016-10-03T19:00:00.999Z' '''


def str_to_timestamp(datetime_str):
    datetime_object = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    timestamp = datetime_object.timestamp()
    return int(timestamp * 1000)
