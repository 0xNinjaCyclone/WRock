
from core.scan.module import *


class Upload(GeneralScanner):
    # This module will get all upload functions, without upload any thing

    def __init__(self, config) -> None:
        GeneralScanner.__init__(self, config)

    def check(self) -> bool:
        endpoint = self.GetEndPoint()

        for pname in endpoint.GetAllParamNames():
            if endpoint.GetParmTypeByName(pname) == 'file':
                self.may_vulnerable_params.append(pname)
                self.GetVulnInfo().register_maybe(self.may_vulnerable_params)
                return True

    def run(self):
        return self.GetVulnInfo()
