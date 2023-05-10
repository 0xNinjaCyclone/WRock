
from core.config.module import *
from core.request import *
from core.scan.result import *
from core.data import *


class BaseScanner:

    def __init__(self, config: ModuleConfig) -> None:
        self.config                 = config
        self.endpoint               = config.GetTarget()
        self.options                = self.config.GetModulesOptions()
        scannerName                 = self.__class__.__name__
        self.may_vulnerable_params  = []
        self.request_args           = {}
        self.vulnInfo               = VulnerabilityInfo(self.endpoint.GetFullUrl(), scannerName)
        self.options.setKey(scannerName.lower())

        
    def GetPayloads(self) -> list:
        # should override
        pass

    def check(self) -> bool:
        # should override
        pass

    def is_vulnerable(self, response) -> bool:
        # should override
        pass

    def GetEndPoint(self):
        return self.endpoint

    def GetRequester(self):
        return self.endpoint.GetRequester(self.config.GetHeaders())

    def GetVulnInfo(self):
        return self.vulnInfo

    def SetRequestArgs(self, **args):
        self.request_args = args

    def InsertAllParamsToScan(self) -> dict:
        
        for pname in self.endpoint.GetAllParamNames():
            if self.endpoint.GetParmTypeByName(pname) != 'submit':
                self.may_vulnerable_params.append(pname)

    def run(self):
        for payload in self.GetPayloads():
            for pname, pvalue in self.endpoint.GetAllParams().items():
                if pname not in self.may_vulnerable_params: continue

                # Set payload in param
                self.endpoint.SetParam(pname, payload)

                try:
                    request = self.GetRequester()
                    res = request.Send(**self.request_args)
                except KeyboardInterrupt:
                    # Stop activities because user want that
                    raise KeyboardInterrupt("Stop !!!")

                except:
                    # Because http requests for scanning activities often get weird
                    # in this case we should continue in our scanning activities 
                    continue
                
                # Reset param to its value after scan
                self.endpoint.SetParam(pname, pvalue)

                if self.is_vulnerable(res):
                    self.vulnInfo.register_vuln(pname, payload)

                    # remove param from may_vulnerable_params
                    self.may_vulnerable_params.remove(pname)
            
            
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