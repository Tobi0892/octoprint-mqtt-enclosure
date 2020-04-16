from classes.DHT22 import DHT22
from classes.MQTT import MQTT
from classes.LOG import LOG
from classes.OCTOPRINT import OCTOPRINT


# CONFIG
MQTT_host = "192.168.178.38"
MQTT_port = 1883
MQTT_timeout = 60
MQTT_username = "octoprint"
MQTT_password = "eTnoGGir19POazSiNNml"
MQTT_topic = "octoprint"
MQTT_retain = True
MQTT_qos = 1
MQTT_message = {
    "enclosure": None,
    "job": None,
    "printer": None
}
LOG_file = "/home/pi/octoprint-mqtt-enclosure/logs/data.log"


# Get DHT22 sensor data
DHT22 = DHT22()
MQTT_message["enclosure"] = DHT22.read(4)
DHT22.cleanup()

# Get Octoprint data
OCTOPRINT = OCTOPRINT()
MQTT_message["job"] = OCTOPRINT.getJob()
MQTT_message["printer"] = OCTOPRINT.getPrinter()

# Log data
LOG = LOG(LOG_file)
LOG.info(MQTT_message)

# Report data via MQTT to Home Assistant
MQTT = MQTT(MQTT_host, MQTT_port, MQTT_timeout, MQTT_username, MQTT_password, MQTT_qos, MQTT_retain)
MQTT.publish(MQTT_topic, MQTT_message)