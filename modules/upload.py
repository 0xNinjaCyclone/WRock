
from core.scanner.module import *


class Upload(ParamsScanner):
    # This module will get all upload functions, without upload any thing

    def __init__(self, config, info = {
        "Authors": ["Abdallah Mohamed"],
        "Name": "Upload file",
        "Description": "The product allows the attacker to upload or transfer files of dangerous types that can be automatically processed within the product's environment.",
        "Risk": Risk.Critical,
        "Referances": [
            "https://cwe.mitre.org/data/definitions/434.html"
        ]
    }) -> None:
        ParamsScanner.__init__(self, config, info)

    def check(self) -> bool:
        endpoint = self.GetEndPoint()

        for pname in endpoint.GetAllParamNames():
            if endpoint.GetParamTypeByName(pname) == 'file':
                self.InsertParamToScan(pname)
                self.GetVulnInfo().register_maybe(pname)
                
        return self.HaveParamsToScan()

    def run(self):
        return self.GetModuleInfo()
