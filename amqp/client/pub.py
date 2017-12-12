#!/usr/bin/env python3

import time

from libs import amqp 


client = amqp.Client()
client.add_broker("127.0.0.1", 5672)
client.add_broker("127.0.0.1", 5673)

client.connect()

try:
    i = 0
    while True:
        client.publish("foo", str(i))
        i += 1
        time.sleep(3)
except KeyboardInterrupt:
    pass

client.disconnect()

