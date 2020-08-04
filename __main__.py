from classes.DHT22 import DHT22
from classes.CCS811 import CCS811
from classes.OCTOPRINT import OCTOPRINT
from classes.MQTT import MQTT
from classes.LOG import LOG


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
    "filament1": None,
    "filament2": None,
    "job": None,
    "printer": None,
    "spools": None
}
LOG_file = "/home/pi/octoprint-mqtt-enclosure/logs/data.log"


# Get DHT22 sensor data
DHT22 = DHT22()
MQTT_message["enclosure"] = DHT22.read(4, 17)
MQTT_message["filament1"] = DHT22.read(10, 9) # gelb grün blau
MQTT_message["filament2"] = DHT22.read(27, 22) # braun rot orange
MQTT_message["filament3"] = DHT22.read(5, 6) # ASA
MQTT_message["filament4"] = DHT22.read(16, 26) # rot, braun, schwarz
MQTT_message["filament5"] = DHT22.read(20, 21) # orange gelb grün
DHT22.cleanup()

# Get CCS811 sensor data
CCS811 = CCS811()
MQTT_message["enclosure"].update(
    CCS811.read(
        MQTT_message["enclosure"]["temperature"],
        MQTT_message["enclosure"]["humidity"]
    )
)

# Get Octoprint data
# TODO check wheter printer is connected or not
OCTOPRINT = OCTOPRINT()
MQTT_message["job"] = OCTOPRINT.getJob()
MQTT_message["printer"] = OCTOPRINT.getPrinter()
MQTT_message["spools"] = OCTOPRINT.getSpools()

# Log data
LOG = LOG(LOG_file)
LOG.info(MQTT_message)

# Report data via MQTT to Home Assistant
MQTT = MQTT(MQTT_host, MQTT_port, MQTT_timeout, MQTT_username, MQTT_password, MQTT_qos, MQTT_retain)
MQTT.publish(MQTT_topic, MQTT_message)