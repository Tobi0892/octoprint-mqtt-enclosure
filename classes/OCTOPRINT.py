import requests
import json
from datetime import datetime, timedelta


class OCTOPRINT:

    def __init__(self):
        self.apikey = "935B41090E1842E1B3DC33D32918AE46"
        self.host = "localhost"

    def request(self, api):
        response = requests.request("GET", "http://" + self.host + "/api/" + api,
                                    headers={'X-Api-Key': self.apikey}
                                    )
        return json.loads(response.text)

    def getJob(self):
        job = self.request("job")

        return {
            "file": self.formatText(job["job"]["file"]["name"]),
            "percent": self.formatNumber(job["progress"]["completion"]),
            "elapsed": self.formatSeconds(job["progress"]["printTime"]),
            "remaining": self.formatSeconds(job["progress"]["printTimeLeft"]),
            "completion": self.calculateCompletion(job["progress"]["printTimeLeft"]),
            "state": self.formatText(job["state"])
        }

    def getPrinter(self):
        printer = self.request("printer")

        return {
            "hotendActual": self.formatNumber(printer["temperature"]["tool0"]["actual"]),
            "hotendTarget": self.formatNumber(printer["temperature"]["tool0"]["target"]),
            "bedActual": self.formatNumber(printer["temperature"]["bed"]["actual"]),
            "bedTarget": self.formatNumber(printer["temperature"]["bed"]["target"]),
        }

    @staticmethod
    def formatSeconds(seconds):
        if seconds is not None:
            h = seconds // 3600
            m = (seconds % 3600) // 60

            return "%02d:%02d" % (h, m)
        else:
            return "00:00"

    @staticmethod
    def formatNumber(number):
        if number is not None:
            return float("{:.1f}".format(number))
        else:
            return "0.0"

    @staticmethod
    def formatText(text):
        if text is not None:
            return text
        else:
            return ""

    @staticmethod
    def calculateCompletion(remaining):
        if remaining != 0 and remaining is not None:
            return (datetime.now() + timedelta(seconds=remaining)).strftime('%H:%M')
        else:
            return "00:00"
