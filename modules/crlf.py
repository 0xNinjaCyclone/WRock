
from core.scanner.module import *


class CRLF(UriScanner):

    def __init__(self, config, info = {
        "Authors": ["Abdallah Mohamed"],
        "Name": "Carriage Return Line Feed Injection",
        "Description": 'The product uses CRLF (carriage return line feeds) as a special element, e.g. to separate lines or records, but it does not neutralize or incorrectly neutralizes CRLF sequences from inputs.',
        "Risk": Risk.Medium,
        "Referances": [
            "https://cwe.mitre.org/data/definitions/93.html"
        ]
    }) -> None:
        UriScanner.__init__(self, config, info)

        # Stop attacking when find a valid way to control the response
        self.StopOnSuccess()
        

    def GetPayloads(self) -> list:
        payloads = list()
        ESCAPE_CHARS = ['%0d','%0a', '%0d%0a', '%23%0d', '%23%0a', '%23%0d%0a']
        INJECTED_HEADERS = [f"wrock: {rockVERSION()}"] #, f"Set-Cookie:wrock={rockVERSION()}"] 
        
        for header in INJECTED_HEADERS:
            for char in ESCAPE_CHARS:
                payloads.append(f"{char}{header}")

        return payloads

    def is_vulnerable(self, response) -> Status:
        return Status.Vulnerable if 'wrock' in response.headers else Status.NotVulnerable


class CRLFParamsBased( ParamsScanner ):

    DEFAULT_PARAM_VALUE = "WRock"

    def __init__(self, config, info = {
        "Authors": ["Abdallah Mohamed"],
        "Name": "Carriage Return Line Feed Injection",
        "Description": 'The product uses CRLF (carriage return line feeds) as a special element, e.g. to separate lines or records, but it does not neutralize or incorrectly neutralizes CRLF sequences from inputs.',
        "Risk": Risk.Medium,
        "Referances": [
            "https://cwe.mitre.org/data/definitions/93.html"
        ]
    }) -> None:
        UriScanner.__init__(self, config, info)

        # Stop attacking when find a valid way to control the response
        self.StopOnSuccess()

    def check(self):
        endpoint = self.DeepCloneEndpoint()

        if not endpoint.GetAllParams():
            return False
        
        self.set_defaults(endpoint)
        res = self.send_request(endpoint)
        ret = False

        if not res or not res.ok:
            return False

        for _, value in res.headers.items():
            if CRLFParamsBased.DEFAULT_PARAM_VALUE in value:
                reflected_value_idx = value.index( CRLFParamsBased.DEFAULT_PARAM_VALUE )
                reflected_value = value[ reflected_value_idx : reflected_value_idx + len(CRLFParamsBased.DEFAULT_PARAM_VALUE) + 1 ]
                vulnerable_param = endpoint.GetParamNameByValue( reflected_value )
                self.InsertParamToScan( vulnerable_param )
                ret = True

        return ret

    def GetPayloads(self) -> list:
        payloads = list()
        ESCAPE_CHARS = ['%0d','%0a', '%0d%0a', '%23%0d', '%23%0a', '%23%0d%0a']
        INJECTED_HEADERS = [f"wrock: {rockVERSION()}"] #, f"Set-Cookie:wrock={rockVERSION()}"] 
        
        for header in INJECTED_HEADERS:
            for char in ESCAPE_CHARS:
                payloads.append(f"{char}{header}")

        return payloads

    def is_vulnerable(self, response) -> Status:
        return Status.Vulnerable if 'wrock' in response.headers else Status.NotVulnerable

    def set_defaults(self, endpoint):
        ctr = 0

        for param in endpoint.GetAllParamNames():
            endpoint.SetParam( param, CRLFParamsBased.DEFAULT_PARAM_VALUE + str(ctr) )
            ctr += 1

    def send_request(self, endpoint, **args):
        try:
            requester = self.GetRequester( endpoint )
            return requester.Send( **args )
        except:
            return None