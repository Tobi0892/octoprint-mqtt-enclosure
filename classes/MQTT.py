import paho.mqtt.client as mqtt
import json


class MQTT:

    def __init__(self, host, port, timeout, username, password, qos, retain):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.username = username
        self.password = password
        self.qos = qos
        self.retain = retain
        self.connect()

    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

    def connect(self):
        self.client = mqtt.Client()
        self.client.username_pw_set(self.username, self.password)
        self.client.on_connect = self.on_connect
        self.client.connect(self.host, self.port, self.timeout)
        self.client.loop_start()

    def publish(self, topic, message):
        self.client.publish(topic, json.dumps(message), qos=self.qos, retain=self.retain)
        print(json.dumps(message))
