import hashlib
from datetime import datetime, timedelta


def url_to_filename(url):
    return hashlib.md5(url.encode('utf-8')).hexdigest()


def expiration_datetime(seconds):
    return datetime.utcnow() + timedelta(seconds=seconds)
