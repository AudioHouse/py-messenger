from datetime import datetime, timedelta
import pytz


def get_time_now():
    now_utc = datetime.now(tz=pytz.utc)
    return now_utc.astimezone(pytz.timezone('US/Pacific'))


def add_hours(timestamp, hours):
    return timestamp + timedelta(hours=hours)


def get_empty_time():
    return get_time_now().replace(hour=0, minute=0, second=0, microsecond=0)


def check_active_range():
    now = get_time_now()
    today9am = now.replace(hour=9, minute=0, second=0, microsecond=0)
    today11pm = now.replace(hour=23, minute=30, second=0, microsecond=0)
    if (now > today9am) and (now < today11pm):
        print(get_empty_time())
        return True
    else:
        return False
