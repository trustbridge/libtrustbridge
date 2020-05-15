import logging
from datetime import datetime
from io import BytesIO

from libtrustbridge.repos import elasticmqrepo
from libtrustbridge.repos.miniorepo import MinioRepo

from .domain import Id, Pattern, Subscription

logger = logging.getLogger(__name__)


class SubscriptionsRepo(MinioRepo):
    DEFAULT_BUCKET = 'subscriptions'

    def subscribe_by_id(self, id: Id, url, expiration_seconds=None):
        key = id.to_key(url)
        return self._subscribe_by_key(key, url, expiration_seconds)

    def subscribe_by_pattern(self, pattern: Pattern, url, expiration_seconds=None):
        key = pattern.to_key(url=url)
        return self._subscribe_by_key(key, url, expiration_seconds)

    def get_subscriptions_by_id(self, id: Id):
        return self._get_subscriptions_by_key(id.to_key(), datetime.utcnow())

    def get_subscriptions_by_pattern(self, pattern: Pattern):
        """
        predicate pattern parameter is the primary search filter
        technically aaaa.bbbb.cccc.* == aaaa.bbbb.cccc
        This can be used for verbosity

        search predicate: a.b.c.d
        1. a = files in A/
        2. a.b = files in A/B/
        3. a.b.c = files in A/B/C/
        4. a.b.c.d files in A/B/C/D/

        Important: subscription AA.BB.CCCC is not equal to AA.BB.CC but includes
        AA.BB.CCCC.EE, and doesn't include AA.BB.CC.GG
        """
        subscriptions = set()
        now = datetime.utcnow()
        layers = pattern.to_layers()
        for storage_key in layers:
            subscriptions |= self._get_subscriptions_by_key(storage_key, now)
        return subscriptions

    def bulk_delete(self, keys):
        if not keys:
            return

        self.client.delete_objects(
            Bucket=self.bucket,
            Delete={
                'Objects': [
                    {'Key': key} for key in keys
                ],
                'Quiet': True,
            },
        )

    def _subscribe_by_key(self, key, url, expiration):
        try:
            subscription = Subscription.encode_obj(url, expiration)
            self.client.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=BytesIO(subscription),
                ContentLength=len(subscription)
            )
        except Exception:
            raise
        else:
            return True

    def _get_subscriptions_by_key(self, key, now):
        subscriptions = set()

        found_objects = self._search_objects(key)
        for obj_key in found_objects:
            obj = self.client.get_object(
                Bucket=self.bucket,
                Key=obj_key,
            )
            payload = obj['Body'].read()
            subscription = Subscription(payload, obj_key, now)
            subscriptions.add(subscription)

        return subscriptions

    def _search_objects(self, storage_key):
        found_objects = set()

        listed_objects = self.client.list_objects(
            Bucket=self.bucket,
            Prefix=storage_key,
            Delimiter='/',  # to avoid recursive search
        )
        # Warning: this is very dumb way to iterate S3-like objects
        # works only on small datasets
        for obj in listed_objects.get('Contents', []):
            found_objects.add(obj['Key'])

        return found_objects


class DeliveryOutboxRepo(elasticmqrepo.ElasticMQRepo):
    def _get_queue_name(self):
        return 'delivery-outbox'


class NotificationsRepo(elasticmqrepo.ElasticMQRepo):
    def _get_queue_name(self):
        return 'notifications'

