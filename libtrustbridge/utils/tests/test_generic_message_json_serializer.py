import json
import uuid

from libtrustbridge.domain.country import Country
from libtrustbridge.domain.uri import URI
from libtrustbridge.domain.wire_protocols.generic_discrete import Message
from libtrustbridge.utils.serializers import MessageJSONEncoder


def test_serialise_message():
    tx = "AU"
    rx = "CN"
    s = str(uuid.uuid4())
    t = str(uuid.uuid4())
    p = str(uuid.uuid4())

    msg = Message(
        sender=Country(tx),
        receiver=Country(rx),
        subject=URI(s),
        obj=URI(t),
        predicate=URI(p))

    expected_json = """
       {{
            "sender": "{}",
            "receiver": "{}",
            "subject": "{}",
            "obj": "{}",
            "predicate": "{}"
       }}
    """.format(tx, rx, s, t, p)

    msg_json = json.dumps(msg, cls=MessageJSONEncoder)

    assert json.loads(msg_json) == json.loads(expected_json)
