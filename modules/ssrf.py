
import socket, struct
from core.scanner.module import *


# Great blog
# https://pravinponnusamy.medium.com/ssrf-payloads-f09b2a86a8b4


class SSRF(ParamsScanner):

    def __init__(self, config, info = {
        "Authors": ["Abdallah Mohamed"],
        "Name": "Server Side Request Forgery",
        "Description": 'The web server receives a URL or similar request from an upstream component and retrieves the contents of this URL, but it does not sufficiently ensure that the request is being sent to the expected destination.',
        "Risk": Risk.High,
        "Referances": [
            "https://cwe.mitre.org/data/definitions/918.html"
        ]
    }) -> None:
        ParamsScanner.__init__(self, config, info)
        self.ssrf_receiver_server = self.options.get('collaborator')


    def check(self):
        endpoint = self.GetEndPoint()
        params = endpoint.GetAllParams()

        if bool(params):
            for param , value in params.items():
                if value.startswith("http://") or value.startswith("https://") or endpoint.GetParamTypeByName(param) == "url":
                    self.InsertParamToScan(param)
        
        return self.HaveParamsToScan()


    def GetPayloads(self) :
        # ip receiver in decimal value for bypassing

        receiver_uri = urlparse(self.ssrf_receiver_server)
        return [ f"{receiver_uri.scheme or 'http'}://{self.ip2long(socket.gethostbyname(receiver_uri.netloc))}/" ]


    def ip2long(self, ip):
        packedIP = socket.inet_aton(ip)
        return struct.unpack("!L", packedIP)[0]


    def run(self):
        # this module will not return true because the receiver server responsible about checking

        if self.ssrf_receiver_server:
            GeneralScanner.run(self)
            
        self.vulnInfo.register_maybe(self.GetMayVulnerableParams())

        return self.GetModuleInfo()


    def is_vulnerable(self, response) -> bool:
        return False
    