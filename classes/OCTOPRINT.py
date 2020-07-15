import requests
import json
from datetime import datetime, timedelta


class OCTOPRINT:

    def __init__(self):
        self.apikey = "935B41090E1842E1B3DC33D32918AE46"
        self.host = "localhost"

    def request(self, path):
        response = requests.request("GET", "http://" + self.host + path,
                                    headers={'X-Api-Key': self.apikey}
                                    )

        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return False

    def getJob(self):
        job = self.request("/api/job")

        if job:
            return {
                "file": self.formatText(job["job"]["file"]["name"]),
                "percent": self.formatNumber(job["progress"]["completion"]),
                "elapsed": self.formatSeconds(job["progress"]["printTime"]),
                "remaining": self.formatSeconds(job["progress"]["printTimeLeft"]),
                "completion": self.calculateCompletion(job["progress"]["printTimeLeft"]),
                "state": self.formatStatus(job["state"])
            }
        else:
            return ""

    def getPrinter(self):
        printer = self.request("/api/printer")

        if printer:
            return {
                "hotendActual": self.formatNumber(printer["temperature"]["tool0"]["actual"]),
                "hotendTarget": self.formatNumber(printer["temperature"]["tool0"]["target"]),
                "bedActual": self.formatNumber(printer["temperature"]["bed"]["actual"]),
                "bedTarget": self.formatNumber(printer["temperature"]["bed"]["target"]),
            }
        else:
            return ""

    def getSpools(self):
        spools = self.request("/plugin/filamentmanager/spools")

        if spools:
            materials = {}
            for spool in spools["spools"]:
                if spool["profile"]["material"] not in materials:
                    materials[spool["profile"]["material"]] = {}
                materials[spool["profile"]["material"]][spool["name"]] = round(spool["weight"] - spool["used"])

            return materials
        else:
            return ""

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
    def formatStatus(status):
        if status[:7] == "Offline":
            return "Offline"
        else:
            return status

    @staticmethod
    def calculateCompletion(remaining):
        if remaining != 0 and remaining is not None:
            return (datetime.now() + timedelta(seconds=remaining)).strftime('%H:%M')
        else:
            return "00:00"
