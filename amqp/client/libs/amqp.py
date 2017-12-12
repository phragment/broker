
import logging
import threading
import time

import pika

class Client():

    def __init__(self, cn=None, xchg="testexchange", logger=None):
        self.brokers = []

        self.cn = cn
        self.xchg = xchg

        self.disconnected = True
        self.recon = False

        if logger:
            self.log = logger.getChild("AMQP")
        else:
            logging.basicConfig()
            self.log = logging.getLogger("AMQP")
            self.log.setLevel(logging.DEBUG)

        # TODO add type info
        # {'foo': [cb1, cb2], 'bar': [cb3]}
        self.topics = {}


    def add_broker(self, host, port):

        self.brokers.append({"host": host, "port": port})


    def connect(self):

        ok = False
        for broker in self.brokers:
            ok = self._connect(broker["host"], broker["port"])
            if ok:
                return ok
        return ok


    def _connect(self, host, port):

        self.log.info("trying {}:{}".format(host, port))
        try:
            self.conn = pika.BlockingConnection(pika.ConnectionParameters(host, port, heartbeat=True))
        except pika.exceptions.ConnectionClosed:
            return False
        self.chan = self.conn.channel()
        self.log.info("connected")

        self.chan.add_on_cancel_callback(self._on_cancel)

        self.fred = threading.Thread(target=self._consume)
        self.fred.daemon = True
        #self.fred.start()

        self.fred2 = threading.Thread(target=self._check)
        self.fred2.daemon = True
        self.fred2.start()

        return True

    def _on_cancel(self):

        print("asd")

    def _consume(self):
        self.log.info("commencing consumption")
        try:
            self.chan.start_consuming()
        except pika.exceptions.ConnectionClosed:
            return

    def disconnect(self):

        self.log.info("disconnecting")
        self.chan.stop_consuming()
        self.chan.close()

        #if self.recon:
        #    self.connect()


    def subscribe(self, cb, topic):

        self.log.info("subscribing to {}".format(topic))

        self.chan.exchange_declare(exchange=self.xchg, exchange_type="fanout")

        if self.cn:
            #self.chan.queue_declare(self.cn, durable=True, arguments={"x-ha-policy": "all"})
            # pika.exceptions.ChannelClosed: (404, "NOT_FOUND - home node 'rabbit2@localhost'
            # of durable queue 'sub1' in vhost '/' is down or inaccessible")
            self.chan.queue_declare(self.cn, arguments={"x-ha-policy": "all"})
            queue_name = self.cn
        else:
            result = self.chan.queue_declare(exclusive=True)
            queue_name = result.method.queue

        self.chan.queue_bind(exchange=self.xchg, queue=queue_name)
        self.chan.basic_consume(self._on_message, queue=queue_name)
        #self.chan.basic_consume(self._on_message, queue=queue_name, no_ack=True)
        self.queue_name = queue_name

        if topic in self.topics:
            self.topics[topic].append(cb)
        else:
            self.topics[topic] = [cb]

        self.fred.start()

    def _check(self):

        while True:
            if not self.conn.is_open:
                print("DOWN")
                time.sleep(1)
                self.connect()
                # TODO resubscribe!
                self.chan.queue_bind(exchange=self.xchg, queue=self.queue_name)
                self.chan.basic_consume(self._on_message, queue=self.queue_name)
                self.fred.start()
            time.sleep(1)


    def _on_message(self, chan, method, prop, msg):

        #self.log.info("{}".format(method))
        self.log.info("received {} from {}".format(msg.decode(), method.routing_key))

        cbs = self.topics[method.routing_key]
        for cb in cbs:
            cb(method.routing_key, msg.decode())


    def publish(self, topic, msg):

        self.log.info("publishing {} to {}".format(msg, topic))
        try:
            self.chan.exchange_declare(exchange=self.xchg, exchange_type="fanout")
            self.chan.basic_publish(exchange=self.xchg, routing_key=topic, body=msg)
        except pika.exceptions.ConnectionClosed:
            # TODO save msg
            self.connect()

