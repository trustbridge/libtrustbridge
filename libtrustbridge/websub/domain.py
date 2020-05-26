import json
import logging
from datetime import datetime

import dateutil

from .utils import url_to_filename, expiration_datetime
from .exceptions import SubscriptionExpired, InvalidSubscriptionFormat, SubscriptionMissingExpiration

logger = logging.getLogger(__name__)


class Id:
    def __init__(self, id):
        self.id = id

    def to_key(self, url=''):
        key = self.id
        if url:
            key += '/%s' % url_to_filename(url)
        return key


class Pattern:
    def __init__(self, topic):
        self.topic = topic

    def to_key(self, url=''):
        self._validate()
        if self.topic.endswith('.'):
            self.topic = self.topic[:-1]
        if self.topic.endswith('*'):
            self.topic = self.topic[:-1]

        parts = self.topic.upper().split('.')
        key = '/'.join([p for p in parts if p]) + '/'
        if url:
            key += url_to_filename(url)
        return key

    def _validate(self):
        if not self.topic:
            raise ValueError("non-empty topic is required")
        if '/' in self.topic:
            raise ValueError("topic should contain dots, not slashes")
        if self.topic.endswith('*') and self.topic[-2] != '.':
            raise ValueError("* character is supported only after a dot")

    def to_layers(self):
        layers = []
        key = self.to_key()
        split_layers = [layer for layer in key.split("/") if layer]
        for i in range(0, len(split_layers)):
            layers.append("/".join(split_layers[0:i + 1]) + "/")
        return layers


class Subscription:
    CALLBACK_KEY = 'c'
    EXPIRATION_KEY = 'e'

    def __init__(self, payload, key, now: datetime):
        self.payload = payload
        self.key = key
        self.now = now
        try:
            self.data = self._decode(payload)
            self.is_valid = True
        except (InvalidSubscriptionFormat, SubscriptionExpired) as e:
            self.is_valid = False
            self.error = str(e)

    def _decode(self, payload):
        try:
            data = json.loads(payload.decode('utf-8'))
        except UnicodeError as e:
            raise InvalidSubscriptionFormat("data is not UTF-8") from e
        except ValueError as e:
            logger.warning("Tried to decode JSON data %s but failed", payload)
            raise InvalidSubscriptionFormat("data is not a valid JSON") from e

        try:
            callback = data[self.CALLBACK_KEY]
            expiration = data.get(self.EXPIRATION_KEY)
            if expiration:
                data[self.EXPIRATION_KEY] = dateutil.parser.parse(expiration)
                self.is_expired = data[self.EXPIRATION_KEY] < self.now
                if self.is_expired:
                    raise SubscriptionExpired()
        except KeyError as e:
            raise InvalidSubscriptionFormat(f"data missing required key:{str(e)}") from e
        except (TypeError, ValueError) as e:
            raise InvalidSubscriptionFormat(f"expiration invalid format:{str(data[self.EXPIRATION_KEY])}") from e

        return data

    @property
    def callback_url(self):
        return self.data[self.CALLBACK_KEY]

    @classmethod
    def encode_obj(cls, callback, expiration_seconds: int):
        if not expiration_seconds:
            raise SubscriptionMissingExpiration()

        expiration = expiration_datetime(expiration_seconds).isoformat()

        data = {
            cls.CALLBACK_KEY: callback,
            cls.EXPIRATION_KEY: expiration
        }
        return json.dumps(data).encode('utf-8')

    def __hash__(self):
        return hash(self.callback_url)

    def __eq__(self, other):
        return self.callback_url == other.callback_url
