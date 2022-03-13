
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

    def Add(self, vulnName, vulnInfo: VulnerabilityInfo):
        if vulnName not in self.results:
            self.results[vulnName] = list()

        self.results[vulnName].append(vulnInfo)

    def GetResultByVuln(self, vulnName):
        if vulnName in self.results:
            return self.results[vulnName]

    def GetAllVulnNames(self):
        return self.results.keys()
