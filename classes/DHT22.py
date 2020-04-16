import Adafruit_DHT
from time import sleep
from RPi import GPIO


class DHT22:

    def __init__(self):
        self.retries = 0
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(11, GPIO.OUT, initial=GPIO.HIGH)

    def read(self, pin):
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 4)

        if humidity is not None and temperature is not None:
            return {
                "temperature": float("{:.1f}".format(temperature)),
                "humidity": float("{:.1f}".format(humidity))
            }
        else:
            self.retries += 1

            # Up to 15 retry readings
            if self.retries < 15:
                print("Reading faild, retry " + str(self.retries))
                sleep(2)
                self.read(self, pin)

    @staticmethod
    def cleanup():
        GPIO.cleanup()
