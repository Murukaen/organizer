from datetime import datetime

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
DATE_TIME_FROMAT_2 = "%Y-%m-%dT%H:%M:%SZ"
DATE_FORMAT = "%Y-%m-%d"

def extract_date(date_str: str) -> datetime:
    try:
        return datetime.strptime(date_str, DATETIME_FORMAT)
    except ValueError:
        pass
    try:
        return datetime.strptime(date_str, DATE_TIME_FROMAT_2)
    except ValueError:
        pass
    try:
        return datetime.strptime(date_str, DATE_FORMAT)
    except ValueError:
        raise Exception(f'Could not parse date {date_str}')