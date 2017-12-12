#!/usr/bin/env python3

import time

from libs import amqp


def msg(topic, payload):
    print(topic, payload)

client = amqp.Client("ha-sub1")
client.add_broker("127.0.0.1", 5673)
client.add_broker("127.0.0.1", 5672)

client.connect()

client.subscribe(msg, "foo")

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    pass

client.disconnect()

