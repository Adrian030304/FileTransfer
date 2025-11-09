import uuid
from datetime import datetime, timedelta


def generate_random_string():
    return uuid.uuid4()


def get_current_time():
    #to format .strftime("%Y-%m-%d %H:%M:%S")
    return datetime.now()