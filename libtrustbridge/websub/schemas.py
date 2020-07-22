from marshmallow import Schema, fields, validate, EXCLUDE

from libtrustbridge.websub.constants import (
    TOPIC_ATTR_KEY,
    CALLBACK_ATTR_KEY,
    MODE_ATTR_KEY,
    SECRET_ATTR_KEY,
    LEASE_SECONDS_ATTR_KEY,
    LEASE_SECONDS_DEFAULT_VALUE,
    SUPPORTED_CALLBACK_URL_SCHEMES,
    SUPPORTED_MODES,
)


class SubscriptionForm(Schema):
    """
    Based on https://www.w3.org/TR/websub/#subscriber-sends-subscription-request
    """
    topic = fields.Str(data_key=TOPIC_ATTR_KEY, required=True)
    callback = fields.Str(data_key=CALLBACK_ATTR_KEY, required=True,
                          validate=validate.URL(schemes=SUPPORTED_CALLBACK_URL_SCHEMES, require_tld=False))
    mode = fields.Str(data_key=MODE_ATTR_KEY, required=True,
                      validate=validate.OneOf(choices=SUPPORTED_MODES))
    lease_seconds = fields.Integer(data_key=LEASE_SECONDS_ATTR_KEY,
                                   missing=LEASE_SECONDS_DEFAULT_VALUE)
    secret = fields.Str(data_key=SECRET_ATTR_KEY,
                        validate=validate.Length(max=200))

    class Meta:
        unknown = EXCLUDE
