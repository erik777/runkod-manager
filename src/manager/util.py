import os
from datetime import datetime, timedelta
import pytz
import hashlib


def md5_checksum(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()


def now_utc() -> datetime:
    return datetime.utcnow().replace(tzinfo=pytz.utc)


def in_1_min() -> datetime:
    return now_utc() + timedelta(minutes=1)


def in_15_min() -> datetime:
    return now_utc() + timedelta(minutes=15)


def in_30_min() -> datetime:
    return now_utc() + timedelta(minutes=30)


def in_1_hour() -> datetime:
    return now_utc() + timedelta(hours=1)


def in_1_day() -> datetime:
    return now_utc() + timedelta(days=1)


def assert_env_vars(*args):
    for a in args:
        if os.environ.get(a) is None:
            raise AssertionError('{} environment variable required'.format(a))
