# Octoprint MQTT Enclosure

Run every minute as cron job


## Install the adafruit dht library and how the sensor ist connected:
via Github repository:
https://tutorials-raspberrypi.de/raspberry-pi-luftfeuchtigkeit-temperatur-messen-dht11-dht22/

via pip3:
https://pimylifeup.com/raspberry-pi-humidity-sensor-dht22/

## Connect all DHT22 sensors to 
- a single GND
- all VCC to GPIO 17 (pin number 11) as this is referenced in `DHT22.py` in order to conduct a hard reset if timing fails
- for the data pins you are free to choose, see `__main__.py` i.e. ``DHT22.read(4)``
