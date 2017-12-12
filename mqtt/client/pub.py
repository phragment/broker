#!/usr/bin/env python3

import time

from libs import mqtt


client = mqtt.Client()
client.add_broker("127.0.0.1", 1337)
client.add_broker("127.0.0.1", 1338)

client.connect()

try:
    i = 0
    while True:
        client.publish("foo", str(i))
        i += 1
        time.sleep(5)
except KeyboardInterrupt:
    pass

client.disconnect()

