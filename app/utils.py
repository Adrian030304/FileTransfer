import uuid
from datetime import datetime, timedelta


def generate_random_string():
    return uuid.uuid4()


def get_current_time():
    #to format .strftime("%Y-%m-%d %H:%M:%S")
    return datetime.now()

def get_time_increment(datetime: datetime, expiration_date_unit):
                unit = float((expiration_date_unit.split(' ')[0]).strip())
                if "minutes" in expiration_date_unit:
                    delta = timedelta(minutes=unit)
                elif "hours":
                    delta = timedelta(hours=unit)
                else:
                    delta = timedelta(days=unit)
                return datetime + delta