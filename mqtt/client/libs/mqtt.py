
import logging
import os
import socket
import time
import threading

import paho.mqtt.client as mqttc


class Client():

    """MQTT

    sync
        connect
        disconnect
    async
        subscribe?
        publish
        (message)

    """

    def __init__(self, clean=True, keepalive=5, retain=False, logger=None):

        self.brokers = []

        self.clean = clean
        self.keepalive = keepalive
        self.retain = retain

        self.state = 0
        self.state_connecting = 1
        self.state_connected = 2
        self.state_disconnecting = 3
        self.state_disconnected = 4

        if logger:
            self.log = logger.getChild("MQTT")
        else:
            logging.basicConfig()
            self.log = logging.getLogger("MQTT")
            self.log.setLevel(logging.DEBUG)

        host = socket.gethostname()
        if self.clean:
            self.client_id = host + "-" + str(os.getpid())
        else:
            self.client_id = host

        self.client = mqttc.Client(self.client_id, self.clean)

        self.client.on_connect    = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_subscribe  = self._on_subscribe
        self.client.on_message    = self._on_message

        # TODO add type info
        # {'foo': [cb1, cb2], 'bar': [cb3]}
        self.topics = {}


    def add_broker(self, host, port):

        self.brokers.append({"host": host, "port": port})


    def connect(self):

        self.log.info("connecting")
        self.state = self.state_connecting
        ok = False
        while not ok:
            ok = self._connect()
            if ok:
                break
            else:
                time.sleep(5)

    def _connect(self):

        self.client.loop_start()

        ok = False
        for broker in self.brokers:
            try:
                self.log.info("trying {}:{}".format(broker["host"], broker["port"]))
                self.client.connect(broker["host"], broker["port"], self.keepalive)

                ok = True
                break
            except ConnectionRefusedError:
                self.log.info("failed")
                continue

        # TODO add timeout
        if ok:
            while self.state != self.state_connected:
                time.sleep(0.1)

        return ok


    def _on_connect(self, client, userdata, flags, rc):

        if rc == mqttc.MQTT_ERR_SUCCESS:
            self.log.info("connected")
            self.state = self.state_connected
            # TODO deliver saved msgs
        else:
            self.log.error(mqttc.connack_string(rc))


    def disconnect(self):

        self.log.info("disconnecting")
        self.state = self.state_disconnecting
        self.client.disconnect()

        # TODO add timeout
        while self.state != self.state_disconnected:
            time.sleep(0.1)


    def _on_disconnect(self, client, userdata, rc):

        self.state = self.state_disconnected
        if rc == mqttc.MQTT_ERR_SUCCESS:
            self.log.info("disconnected")
        else:
            self.log.error("unexpected disconnect")

            thread = threading.Thread(target=self._reconnect)
            thread.daemon = True
            thread.start()

    def _reconnect(self):
        time.sleep(3)
        self.connect()
        # resubscribe on connect to other broker
        # TODO if unclean session on new broker
        for topic in self.topics.keys():
            self.client.subscribe(topic, 0)

    def subscribe(self, cb, topic, qos=0):

        self.log.info("subscribing to {}".format(topic))
        self.client.subscribe(topic, qos)

        if topic in self.topics:
            self.topics[topic].append(cb)
        else:
            self.topics[topic] = [cb]


    def _on_subscribe(self, client, userdata, mid, qos_list):

        self.log.info("subscribed")


    def _on_message(self, client, userdata, msg):

        self.log.debug('message {!s}: {} {} QoS {!s} retain {!s}'.format(
                       msg.mid, msg.topic, msg.payload, msg.qos, msg.retain))

        cbs = self.topics[msg.topic]
        for cb in cbs:
            cb(msg.topic, str(msg.payload))

    def publish(self, topic, payload, qos=0, retain=None):
        # TODO
        # check connected
        # save if not connected

        if retain == None:
            retain = self.retain

        self.log.info("publishing {} to {}".format(payload, topic))
        (rc, mid) = self.client.publish(topic, payload, qos, retain)

        if rc != mqttc.MQTT_ERR_SUCCESS:
            self.log.info("could not publish")

