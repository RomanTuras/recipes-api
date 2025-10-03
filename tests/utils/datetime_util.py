from datetime import datetime


def get_datetime_from_str(date_str: str) -> datetime:
    format_string = "%Y-%m-%d %H:%M:%S"
    return datetime.strptime(date_str, format_string)
