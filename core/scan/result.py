
from enum import Enum, auto


class Status(Enum):
    Vulnerable      = auto()
    Maybe           = auto()
    NotVulnerable   = auto()


class VulnerabilityInfo:

    def __init__(self, url, vulnName) -> None:
        self.url                = url
        self.vulnName           = vulnName
        self.status             = Status.NotVulnerable
        self.vulnerable_params  = []

    def register_vuln(self, paramName, payload):
        self.status = Status.Vulnerable
        self.__add_vuln__(paramName, payload)

    def register_maybe(self, paramName, payload = ''):
        self.status = Status.Maybe
        self.__add_vuln__(paramName, payload)

    def __add_vuln__(self, paramName, payload):
        if isinstance(paramName, list):
            for pname in paramName:
                self.vulnerable_params.append({"param": pname, "payload": payload})
        
        else:
            self.vulnerable_params.append({"param": paramName, "payload": payload})


class ScanResults:

    def __init__(self) -> None:
        self.results = {}

    def Add(self, vulnInfo: VulnerabilityInfo):
        if vulnInfo.vulnName not in self.results:
            self.results[vulnInfo.vulnName] = list()

        self.results[vulnInfo.vulnName].append(vulnInfo)

    def GetResultByVuln(self, vulnName):
        if vulnName in self.results:
            return self.results[vulnName]

    def GetAllVulnNames(self):
        return self.results.keys()

    def merge(self, o):
        for vulnName in o.GetAllVulnNames():
            if vulnName in self.results:
                self.results[vulnName] += o.GetResultByVuln(vulnName)

            else:
                self.results[vulnName] = o.GetResultByVuln(vulnName)

    def __add__(self, o):
        self.merge(o)
        return self
