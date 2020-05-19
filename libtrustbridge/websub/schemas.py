from marshmallow import Schema, fields, validate, EXCLUDE

from libtrustbridge.websub.constants import (
    TOPIC_ATTR_KEY,
    CALLBACK_ATTR_KEY,
    SUPPORTED_CALLBACK_URL_SCHEMES,
    MODE_ATTR_KEY,
    LEASE_SECONDS_DEFAULT_VALUE,
    SECRET_ATTR_KEY,
)


class SubscriptionForm(Schema):
    """
    Based on https://www.w3.org/TR/websub/#subscriber-sends-subscription-request
    """
    topic = fields.Str(data_key=TOPIC_ATTR_KEY, required=True)
    callback = fields.Str(data_key=CALLBACK_ATTR_KEY, required=True,
                          validate=validate.URL(schemes=SUPPORTED_CALLBACK_URL_SCHEMES))
    mode = fields.Str(data_key=MODE_ATTR_KEY, required=True,
                      validate=validate.OneOf(choices=["subscribe", "unsubscribe"]))
    lease_seconds = fields.Integer(data_key='hub.lease_seconds',
                                   missing=LEASE_SECONDS_DEFAULT_VALUE)
    secret = fields.Str(data_key=SECRET_ATTR_KEY,
                        validate=validate.Length(max=200))

    class Meta:
        unknown = EXCLUDE
