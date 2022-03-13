
import socket, struct
from core.scan.module import *


# Great blog
# https://pravinponnusamy.medium.com/ssrf-payloads-f09b2a86a8b4


class SSRF(GeneralScanner):

    def __init__(self, config) -> None:
        GeneralScanner.__init__(self, config)
        self.ssrf_receiver_server = self.options.get('collaborator')


    def check(self):
        params = self.request.GetParams()

        if bool(params):
            for param , values in params.items():
                value = values.__getitem__(0)
                if value.startswith("http://") or value.startswith("https://"):
                    self.vulnerable_params.append(param)
                    return True

        
        return False


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
            
        self.vulnInfo.status = Status.Maybe

        return self.GetVulnInfo()


    def is_vulnerable(self, response) -> bool:
        return False
    