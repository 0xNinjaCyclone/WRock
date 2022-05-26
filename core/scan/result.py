
from enum import Enum, auto


class Status(Enum):
    Vulnerable      = auto()
    Maybe           = auto()
    NotVulnerable   = auto()


class VulnerabilityInfo:

    def __init__(self) -> None:
        self.url        = None
        self.vulnName   = None
        self.status     = Status.NotVulnerable


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
