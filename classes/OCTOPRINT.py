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
            "file": job["job"]["file"]["name"],
            "percent": float("{:.1f}".format(job["progress"]["completion"])),
            "elapsed": self.formatSeconds(job["progress"]["printTime"]),
            "remaining": self.formatSeconds(job["progress"]["printTimeLeft"]),
            "completion": self.calculateCompletion(job["progress"]["printTimeLeft"]),
            "state": job["state"]
        }

    def getPrinter(self):
        printer = self.request("printer")

        return {
            "hotendActual": float("{:.1f}".format(printer["temperature"]["tool0"]["actual"])),
            "hotendTarget": float("{:.1f}".format(printer["temperature"]["tool0"]["target"])),
            "bedActual": float("{:.1f}".format(printer["temperature"]["bed"]["actual"])),
            "bedTarget": float("{:.1f}".format(printer["temperature"]["bed"]["target"])),
        }

    @staticmethod
    def formatSeconds(seconds):
        h = seconds // 3600
        m = (seconds % 3600) // 60

        return "%02d:%02d" % (h, m)

    @staticmethod
    def calculateCompletion(remaining):
        if remaining != 0:
            return (datetime.now() + timedelta(seconds=remaining)).strftime('%H:%M')
        else:
            return "00:00"

