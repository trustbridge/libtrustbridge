from marshmallow import Schema, fields, validate, EXCLUDE

from libtrustbridge.websub import constants


class SubscriptionForm(Schema):
    """
    Based on https://www.w3.org/TR/websub/#subscriber-sends-subscription-request
    """
    topic = fields.Str(data_key='hub.topic', required=True)
    callback = fields.Str(data_key='hub.callback', required=True, validate=validate.URL(schemes=["http", "https"]))
    mode = fields.Str(data_key='hub.mode', required=True, validate=validate.OneOf(choices=["subscribe", "unsubscribe"]))
    lease_seconds = fields.Integer(data_key='hub.lease_seconds', missing=constants.LEASE_SECONDS_DEFAULT_VALUE)
    secret = fields.Str(data_key='hub.secret', validate=validate.Length(max=200))

    class Meta:
        unknown = EXCLUDE
