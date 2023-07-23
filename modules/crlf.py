
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

    def is_vulnerable(self, response) -> bool:
        return 'wrock' in response.headers
