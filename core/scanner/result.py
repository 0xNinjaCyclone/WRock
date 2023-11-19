
from enum import Enum, auto

class Status(Enum):
    Vulnerable      = auto()
    Maybe           = auto()
    NotVulnerable   = auto()

class Risk(Enum):
    Critical = auto()
    High     = auto()
    Medium   = auto()
    Low      = auto()
    Unknown  = auto()

class VulnerabilityInfo:

    def __init__(self, endpoint, vulnName) -> None:
        self.endpoint           = endpoint
        self.vulnName           = vulnName
        self.status             = Status.NotVulnerable
        self.vulnerables        = []

    def register_vuln(self, position, payload):
        self.status = Status.Vulnerable
        self._add_vuln_(position, payload)

    def register_maybe(self, position, payload = ''):
        self.status = Status.Maybe
        self._add_vuln_(position, payload)

    def GetAllVulnerables(self):
        return self.vulnerables

    def _add_vuln_(self, position, payload):
        pass

class ParamsVulnInfo(VulnerabilityInfo):

    def __init__(self, url, vulnName) -> None:
        VulnerabilityInfo.__init__(self, url, vulnName)

    def _add_vuln_(self, position, payload):
        if isinstance(position, list):
            for pname in position:
                self.vulnerables.append({"param": pname, "payload": payload})
        
        else:
            self.vulnerables.append({"param": position, "payload": payload})

class UriVulnInfo(VulnerabilityInfo):

    def __init__(self, url, vulnName) -> None:
        VulnerabilityInfo.__init__(self, url, vulnName)

    def _add_vuln_(self, position, payload):
        if isinstance(position, list):
            for uripath in position:
                self.vulnerables.append({"uripath": uripath, "payload": payload})
        
        else:
            self.vulnerables.append({"uripath": position, "payload": payload})

class HeadersVulnInfo(VulnerabilityInfo):

    def __init__(self, url, vulnName) -> None:
        VulnerabilityInfo.__init__(self, url, vulnName)

    def _add_vuln_(self, position, payload):
        if isinstance(position, list):
            for hname in position:
                self.vulnerables.append({"headername": hname, "payload": payload})
        
        else:
            self.vulnerables.append({"headername": position, "payload": payload})

class DataExposureInfo(VulnerabilityInfo):

    def __init__(self, endpoint, vulnName) -> None:
        VulnerabilityInfo.__init__(self, endpoint, vulnName)

    def _add_vuln_(self, position, payload):
        if isinstance(position, list):
            for place in position:
                self.vulnerables.append({"place": place, "data": payload})
        
        else:
            self.vulnerables.append({"place": position, "data": payload})


class ModuleInfo:

    @classmethod
    def Load(cls, info = {}):
        return ModuleInfo(
            authors=info['Authors'] if 'Authors' in info else [],
            name = info['Name'] if 'Name' in info else "'blank'",
            description=info['Description'] if 'Description' in info else "Description not provided !!",
            risk=info['Risk'] if 'Risk' in info else Risk.Unknown,
            referances=info['Referances'] if 'Referances' in info else []
        )

    def __init__(self, authors: list, name: str, description:str, risk: Risk, referances: list) -> None:
        self.__authors     = authors
        self.__name        = name
        self.__description = description
        self.__risk        = risk
        self.__referances  = referances
        self.__vuln        = None

    def SetVulnInfo(self, vuln):
        self.__vuln = vuln

    def GetAuthors(self):
        return self.__authors

    def GetName(self):
        return self.__name

    def GetDescription(self):
        return self.__description

    def GetRisk(self):
        return self.__risk

    def GetReferances(self):
        return self.__referances

    def GetVulnInfo(self) -> VulnerabilityInfo:
        return self.__vuln

    def Transform(self):
        return {
            "Authors": self.__authors,
            "Module Name": self.__name,
            "Description": self.__description,
            "Risk": "Critical" if self.__risk == Risk.Critical else "High" if self.__risk == Risk.High else "Medium" if self.__risk == Risk.Medium else "Low" if self.__risk == Risk.Low else "Unknown",
            "Referances": self.__referances
        }


class ScanResults:

    def __init__(self) -> None:
        self.__results = {}

    def Add(self, modInfo: ModuleInfo):
        vulnName = modInfo.GetVulnInfo().vulnName

        if vulnName not in self.__results:
            self.__results[vulnName] = list()

        self.__results[vulnName].append(modInfo)

    def GetResultByVuln(self, vulnName):
        if vulnName in self.__results:
            return self.__results[vulnName]

    def GetAllVulnNames(self):
        return self.__results.keys()

    def Transform(self) -> dict:
        dResult = dict()

        for vulnName in self.GetAllVulnNames():
            for modInfo in self.GetResultByVuln(vulnName):
                vulnInfo = modInfo.GetVulnInfo()

                # Skip not vulnerable endpoints
                if vulnInfo.status == Status.NotVulnerable:
                    continue

                if not vulnName in dResult:
                    dResult[ vulnName ] = []

                dResult[ vulnName ].append({
                    "Module info":  modInfo.Transform(),
                    "Method":       vulnInfo.endpoint.GetMethodType(),
                    "Url":          vulnInfo.endpoint.GetFullUrl(),
                    "Get params":   vulnInfo.endpoint.GetParams(),
                    "Post params":  vulnInfo.endpoint.GetData(),
                    "Vulnerables":  vulnInfo.vulnerables
                })

        return dResult

    def merge(self, o):
        for vulnName in o.GetAllVulnNames():
            if vulnName in self.__results:
                self.__results[vulnName] += o.GetResultByVuln(vulnName)

            else:
                self.__results[vulnName] = o.GetResultByVuln(vulnName)

    def __add__(self, o):
        self.merge(o)
        return self
