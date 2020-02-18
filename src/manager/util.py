import os
from datetime import datetime
import pytz
import hashlib


def md5_checksum(s) -> str:
    return hashlib.md5(s.encode('utf-8')).hexdigest()


def now_utc() -> datetime:
    return datetime.utcnow().replace(tzinfo=pytz.utc)


def dt_api_format(date: datetime):
    if date is None:
        return None

    return date.replace(microsecond=0).isoformat()


def assert_env_vars(*args):
    for a in args:
        if os.environ.get(a) is None:
            raise AssertionError('{} environment variable required'.format(a))
