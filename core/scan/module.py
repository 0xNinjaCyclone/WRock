
from core.config.module import *
from core.request import *
from core.scan.result import *
from core.data import *


class BaseScanner:

    def __init__(self, config: ModuleConfig) -> None:
        self.config             = config
        self.url                = config.GetTarget()
        self.options            = self.config.GetModulesOptions()
        scannerName             = self.__class__.__name__
        self.options.setKey(scannerName.lower())
        self.request            = Get(self.url, headers = self.config.GetHeaders())
        self.vulnerable_params  = []
        self.vulnInfo           = VulnerabilityInfo()
        self.vulnInfo.vulnName  = scannerName
        self.vulnInfo.url       = self.url

        
    def GetPayloads(self) -> list:
        # should override
        pass

    def check(self) -> bool:
        # should override
        pass

    def is_vulnerable(self, response) -> bool:
        # should override
        pass

    def GetVulnInfo(self):
        return self.vulnInfo

    def PutPayloadInParams(self, payload):
        params = self.request.GetParams()

        for param in params:
            if param in self.vulnerable_params:
                params[param] = payload
                continue
            
            # Set the normal parameter value if this param is not vulnerable 
            params[param] = params.get(param).__getitem__(0)

        return params

    def SetPayloadInParams(self, payload) -> dict:
        # Put payload in vulnerable params
        params = self.PutPayloadInParams(payload)

        # Pass injected params to request handler
        self.request.SetParams(params)

    def run(self):
        for payload in self.GetPayloads():
            self.SetPayloadInParams(payload)

            try:
                res = self.request.Send()
            except KeyboardInterrupt:
                # Stop activities because user want that
                raise KeyboardInterrupt("Stop !!!")

            except:
                # Because http requests for scanning activities often get weird
                # in this case we should continue in our scanning activities 
                continue
            

            if self.is_vulnerable(res):
                self.vulnInfo.status = Status.Vulnerable
            
            
        return self.GetVulnInfo()


class CommonScanner(BaseScanner):

    # Modules folder that will use this
    MODPATH = "common"

    def __init__(self, config: ModuleConfig) -> None:
        BaseScanner.__init__(self, config)


class GeneralScanner(BaseScanner):

    # Modules folder that will use this
    MODPATH = "general"

    def __init__(self, config: ModuleConfig) -> None:
        BaseScanner.__init__(self, config)