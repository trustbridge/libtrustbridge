from datetime import datetime
from unittest import TestCase

import pytest
from freezegun import freeze_time

from libtrustbridge.websub.domain import Pattern, Subscription


class PatternTest(TestCase):
    def test_to_key__when_empty__should_return_error(self):
        with pytest.raises(ValueError):
            Pattern(topic='').to_key()

    def test_to_key__when_contains_slashes__should_return_error(self):
        with pytest.raises(ValueError):
            Pattern(topic='aa/bb').to_key()

    def test_to_key__when_wildcard_without_dot__should_return_error(self):
        with pytest.raises(ValueError):
            Pattern(topic='aa.bb*').to_key()

    def test_to_key__when_predicate_valid__should_return_key(self):
        assert Pattern('aaaa.bbbb.cccc').to_key() == "AAAA/BBBB/CCCC/"

    def test_to_key__with_wildcard_in_predicate__should_be_handled(self):
        assert Pattern('aaaa.bbbb.cccc.*').to_key() == "AAAA/BBBB/CCCC/"
        assert Pattern('aaaa.bbbb.cccc.').to_key() == "AAAA/BBBB/CCCC/"

    def test_to_key__with_url__should_add_url_hashed_as_suffix(self):
        expected = "AAAA/BBBB/CCCC/8710bd9f92a413cbcaa13aa0e00953ba"
        assert Pattern('aaaa.bbbb.cccc.*').to_key(url='http://callback.com/1') == expected

    def test_to_layers__should_return_list_of_layers(self):
        assert Pattern('aaaa.bbbb.cccc.*').to_layers() == [
            'AAAA/',
            'AAAA/BBBB/',
            'AAAA/BBBB/CCCC/'
        ]


@freeze_time("2020-05-12 12:00:01")
class SubscriptionTest(TestCase):
    def setUp(self):
        self.payload = b'{"e": "2020-05-12 14:00:01", "c": "http://callback.com/1"}'

    def test_subscription_for_valid_object__should_have_callback_url(self):
        subscription = Subscription(self.payload, 'some_name', now=datetime.utcnow())
        assert subscription.is_valid
        assert not subscription.is_expired
        assert subscription.callback_url == 'http://callback.com/1'

    @freeze_time("2020-05-12 15:00:01")
    def test_subscription_for_expired_object__should_be_not_valid(self):
        subscription = Subscription(self.payload, 'some_name', now=datetime.utcnow())
        assert not subscription.is_valid
        assert subscription.is_expired

    def test_subscription__when_missing_callback__should_be_not_valid(self):
        subscription = Subscription(b'{}', 'some_name', now=datetime.utcnow())
        assert not subscription.is_valid
        assert subscription.error == "data missing required key:'c'"

    def test_subscription__when_missing_expiration__should_be_valid(self):
        subscription = Subscription(b'{"c": "http://callback.com/1"}', 'some_name', now=datetime.utcnow())
        assert subscription.is_valid
