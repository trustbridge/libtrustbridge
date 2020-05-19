import pytest
from marshmallow import ValidationError

from libtrustbridge.websub.schemas import SubscriptionForm


def test_form__when_valid__should_return_loaded_data():
    loaded = SubscriptionForm().load({
        "hub.callback": "http://callback.com",
        "hub.topic": "topic",
        "hub.mode": "subscribe",
        "hub.lease_seconds": 3600,
    })

    assert loaded == {
        'callback': 'http://callback.com',
        'lease_seconds': 3600,
        'mode': 'subscribe',
        'topic': 'topic'
    }


def test_form__when_callback_missing__should_return_error():
    with pytest.raises(ValidationError) as exc:
        SubscriptionForm().load({
            "hub.topic": "topic",
            "hub.mode": "subscribe",
        })
    assert exc.value.messages == {'hub.callback': ['Missing data for required field.']}


@pytest.mark.parametrize("url", [
    "invalid_url",
    "ftp://somehost.com/",
])
def test_form__when_callback_invalid_url__should_return_error(url):
    with pytest.raises(ValidationError) as exc:
        SubscriptionForm().load({
            "hub.callback": url,
            "hub.topic": "topic",
            "hub.mode": "subscribe",
        })
    assert exc.value.messages == {'hub.callback': ['Not a valid URL.']}


def test_form__when_invalid_mode__should_return_error():
    with pytest.raises(ValidationError) as exc:
        SubscriptionForm().load({
            "hub.callback": "https://callback.com",
            "hub.topic": "topic",
            "hub.mode": "please subscribe me",
        })
    assert exc.value.messages == {'hub.mode': ['Must be one of: subscribe, unsubscribe.']}


def test_form__when_too_big_secret__should_return_error():
    with pytest.raises(ValidationError) as exc:
        SubscriptionForm().load({
            "hub.callback": "https://callback.com",
            "hub.topic": "topic",
            "hub.mode": "subscribe",
            "hub.secret": "x" * 201,
        })
    assert exc.value.messages == {'hub.secret': ['Longer than maximum length 200.']}


def test_form__when_additional_params__should_ignore():
    loaded = SubscriptionForm().load({
        "hub.callback": "http://callback.com",
        "hub.topic": "topic",
        "hub.mode": "unsubscribe",
        "ignore": "me",

    })

    assert "ignore" not in loaded


def test_form_lease_seconds__when_missing__should_be_5_days():
    loaded = SubscriptionForm().load({
        "hub.callback": "http://callback.com",
        "hub.topic": "topic",
        "hub.mode": "subscribe",
    })
    assert loaded['lease_seconds'] == 5 * 24 * 3600
