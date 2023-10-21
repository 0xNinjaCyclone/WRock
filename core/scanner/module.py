
from core.config.module import *
from core.request import *
from core.scanner.endpoint import EndPoint
from core.scanner.result import *
from core.data import *


class BaseScanner:

    def __init__(self, config: ModuleConfig, info = {}) -> None:
        self.config                 = config
        self.endpoint               = config.GetTarget()
        self.options                = self.config.GetModulesOptions()
        self.request_args           = {}
        self.moduleInfo             = ModuleInfo.Load(info)
        self.vulnInfo               = self.InitVulnInfo()
        self.moduleInfo.SetVulnInfo(self.GetVulnInfo())
        self.options.setKey(self.__class__.__name__.lower())

        # flags
        self.__stoponsuccess = False

        
    def GetPayloads(self) -> list:
        # should override
        pass

    def check(self) -> bool:
        # should override
        pass

    def is_vulnerable(self, response) -> Status:
        # should override
        pass

    def StopOnSuccess(self):
        self.__stoponsuccess = True

    def ShouldStop(self):
        return self.__stoponsuccess

    def GetEndPoint(self):
        return self.endpoint

    def DeepCloneEndpoint(self, url = '', method = '', params = {}):
        return EndPoint(
            url if url else self.endpoint.GetFullUrl(),
            method if method else self.endpoint.GetMethodType(),
            params if params else self.endpoint.GetRawParams()
        )

    def GetRequester(self, endpoint=None):
        e = endpoint if endpoint else self.endpoint
        return e.GetRequester(self.config.GetHeaders())

    def InitVulnInfo(self) -> VulnerabilityInfo:
        pass

    def GetVulnInfo(self):
        return self.vulnInfo

    def GetModuleInfo(self):
        return self.moduleInfo

    def GetHeaders(self):
        return self.config.GetHeaders().copy()

    def SetRequestArgs(self, **args):
        self.request_args = args

    def run(self) -> ModuleInfo:
        return self.GetModuleInfo()


class GeneralScanner(BaseScanner):

    def __init__(self, config: ModuleConfig, info = {}) -> None:
        BaseScanner.__init__(self, config, info)


class ParamsScanner(GeneralScanner):

    def __init__(self, config: ModuleConfig, info={}) -> None:
        GeneralScanner.__init__(self, config, info) 
        self.__may_vulnerable_params  = []

    def InitVulnInfo(self):
        return ParamsVulnInfo(self.endpoint, self.__class__.__name__)

    def InsertParamToScan(self, pname):
        if self.endpoint.GetParamTypeByName(pname) != 'submit':
            self.__may_vulnerable_params.append(pname)

    def InsertAllParamsToScan(self):
        for pname in self.endpoint.GetAllParamNames():
            self.InsertParamToScan(pname)

    def GetMayVulnerableParams(self) -> list:
        return self.__may_vulnerable_params

    def HaveParamsToScan(self) -> bool:
        return bool( self.GetMayVulnerableParams() )

    def check(self):
        # check if url has parameters
        # we cannot scan Params based urls without parameters
        # put all prameters to __may_vulnerable_params for scan it with payloads
        
        self.InsertAllParamsToScan()
        return self.HaveParamsToScan()

    def run(self):
        for payload in self.GetPayloads():
            for pname in self.GetMayVulnerableParams():

                # Get a new endpoint object copied from self.endpoint
                endpoint = self.DeepCloneEndpoint()

                # Set payload in param
                endpoint.SetParam(pname, payload)

                try:
                    request = self.GetRequester(endpoint)
                    res = request.Send(**self.request_args)
                except KeyboardInterrupt:
                    # Stop activities because user want that
                    raise KeyboardInterrupt("Stop !!!")

                except:
                    # Because http requests for scanning activities often get weird
                    # in this case we should continue in our scanning activities 
                    continue

                status = self.is_vulnerable(res)

                if status != Status.NotVulnerable:
                    if status == Status.Vulnerable:
                        self.vulnInfo.register_vuln(pname, payload)

                    else:
                        self.vulnInfo.register_maybe(pname, payload)

                    # remove param from __may_vulnerable_params
                    self.__may_vulnerable_params.remove(pname)

                    # stop scanning activities against this endpoint if required
                    if self.ShouldStop():
                        return self.GetModuleInfo()

        return self.GetModuleInfo()


class UriScanner(GeneralScanner):

    def __init__(self, config: ModuleConfig, info={}) -> None:
        GeneralScanner.__init__(self, config, info)
        self.__manipulate_path = False

    def AllowPathManipulation(self):
        self.__manipulate_path = True

    def InitVulnInfo(self):
        return UriVulnInfo(self.endpoint, self.__class__.__name__)

    def GetPath(self):
        return self.endpoint.GetPath()

    def check(self) -> bool:
        # Check if there is no query
        return not bool(self.endpoint.GetParams())

    def run(self):
        for payload in self.GetPayloads():
            endpoint = self.GetEndPoint()

            try:
                # Prepared requester with current targeted endpoint
                req = self.GetRequester()

                if self.__manipulate_path:
                    # In this case the scanner will manipulate the path 
                    req.SetUrl( endpoint.GetUrlWithoutPath() + payload )

                else:
                    # Set our payload at the end of url
                    req.SetUrl( endpoint.GetUrl() + payload )

                # Send HTTP Request ( request_args for user if need to set any additional request option )
                res = req.Send( **self.request_args )

            except KeyboardInterrupt:
                    # Stop activities because user want that
                    raise KeyboardInterrupt("Stop !!!")

            except:
                # Because http requests for scanning activities often get weird
                # in this case we should continue in our scanning activities 
                continue

            status = self.is_vulnerable(res)

            if status != Status.NotVulnerable:
                path = endpoint.GetUri().path

                if status == Status.Vulnerable:
                    self.vulnInfo.register_vuln(path, payload)

                else:
                    self.vulnInfo.register_maybe(path, payload)

                # stop scanning activities against this endpoint if required
                if self.ShouldStop():
                    break

        return self.GetModuleInfo()


class HeadersScanner(GeneralScanner):

    def __init__(self, config: ModuleConfig, info={}) -> None:
        GeneralScanner.__init__(self, config, info)
        
    def InitVulnInfo(self):
        return HeadersVulnInfo(self.endpoint, self.__class__.__name__)

    def check(self) -> bool:
        return True

    def run(self):
        for payload in self.GetPayloads():
            headers = self.GetHeaders()
            headers.update( payload )

            try:
                req = self.GetRequester()
                req.SetHeaders( headers )
                res = req.Send( **self.request_args )

            except KeyboardInterrupt:
                    # Stop activities because user want that
                    raise KeyboardInterrupt("Stop !!!")

            except:
                # Because http requests for scanning activities often get weird
                # in this case we should continue in our scanning activities 
                continue

            status = self.is_vulnerable(res)

            if status != Status.NotVulnerable:
                for hname, value in payload.items():
                    if status == Status.Vulnerable:
                        self.vulnInfo.register_vuln(hname, value)

                    else:
                        self.vulnInfo.register_maybe(hname, value)

                # stop scanning activities against this endpoint if required
                if self.ShouldStop():
                    break

        return self.GetModuleInfo()