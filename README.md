Trustbridge library
===================

https://github.com/trustbridge/libtrustbridge

SubscriptionsRepo
 - subscribe by id (id_type, id): /subscriptions_by_id/{id_type}/{id}/*
 - subscribe by pattern (pattern_type, pattern): /subscriptions_by_pattern/{pattern_type}/{pattern/as/chunks/}/*
 - get subscriptions by id
 - get subscriptions by pattern

https://github.com/trustbridge/intergov/intergov/repos/subscriptions/minio/miniorepo.py
 - subscribe_by_id(id_type, id), e.g. ("sender_ref": {sender_ref}), "channel_id", "channel_txn_id"
   - (regulated community -> Node)
     subscribe to message after posting to the node (by sender_ref)
     `GET https://{node}/send_messages/{sender_ref}
     EFFERENT (Exit, Eject, Etched into the blockchain)

   - (node operator -> Channel Endpoint)
     subscribe to message (by channel_txn_id)                            EFFERENT
     `GET https://{channel_endpoint}/sent_messages/{channel_txn_id}`

   - (regulator: channel manager -> Node)
     subscribe to all messages on a channel (by channel_id) that the node can see
     `GET https://{node}/channels/{channel_id}/messages`                 AFFERENT+EFFERENT

   - (node operator -> Channel Endpoint)
     subscribe to all messages for a jurisdiction
     AFFERENT (Arrive, listened on the blockchain Airwaves)
     `GET https://{channel_endpoint}/{jurisdiction}/received_messages`

 - subscribe_by_pattern(pattern_type, pattern) , e.g. ("predicate", "UN.CEFACT.Trade.CoO.*")
   - (regulator: operational area)
     subscribe to all messages on a node, by predicate pattern
     `GET https://{node}/sent_messages/predicate_pattern`                EFFERENT
     `GET https://{node}/received_messages/predicate_pattern`            AFFERENT
