
from core.scan.module import *


class CRLF(CommonScanner):

    def __init__(self, config) -> None:
        CommonScanner.__init__(self, config)
        
    def check(self) -> bool:
        return True

    def GetPayloads(self) -> list:
        payloads = list()
        ESCAPE_CHARS = ['%0d','%0a', '%0d%0a', '%23%0d', '%23%0a', '%23%0d%0a']
        INJECTED_HEADERS = [f"wrock: {rockVERSION()}"] #, f"Set-Cookie:wrock={rockVERSION()}"] 
        
        for header in INJECTED_HEADERS:
            for char in ESCAPE_CHARS:
                payloads.append(f"{unquote(char)}{header}")

        return payloads

    def is_vulnerable(self, response) -> bool:
        return 'wrock' in response.headers

    def SetPayloadInParams(self, payload) -> dict:
        # reinit request to add the payloads at the end of the url
        # and we don't encode the payload when the url has params because 
        # GetUrl() method will encode params and the payload.

        self.request = Get(self.url + (payload if self.request.GetUrlParams() else quote(payload)), headers = self.config.GetHeaders())
