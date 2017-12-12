#!/usr/bin/env python3

import time

from libs import mqtt


def msg(topic, payload):
    print(topic, payload)

client = mqtt.Client()
client.add_broker("127.0.0.1", 1338)
client.add_broker("127.0.0.1", 1337)

client.connect()

client.subscribe(msg, "foo")

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    pass

client.disconnect()

