
from core.scanner.module import *

class CORS( HeadersScanner, GlobalLevelScanner ):

    def __init__(self, config: ModuleConfig, info = {
        "Authors": ["Abdallah Mohamed"],
        "Name": "Cross Origin Resource Sharing",
        "Description": "The product uses a web-client protection mechanism such as a Content Security Policy (CSP) or cross-domain policy file, but the policy includes untrusted domains with which the web client is allowed to communicate.",
        "Risk": Risk.High,
        "Referances": [
            "https://cwe.mitre.org/data/definitions/942.html",
            "https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/11-Client-side_Testing/07-Testing_Cross_Origin_Resource_Sharing"
        ]
    }) -> None:
        HeadersScanner.__init__(self, config, info)
        GlobalLevelScanner.__init__(self, config, info)
        self.StopOnSuccess()
        self.__rand_origin = 'https://' + ''.join(random.choices(string.ascii_lowercase, k=8)) + '.wrock.com'

    def GetPayloads(self):
        return [ 
            { 'Origin': self.__rand_origin },
            { 'Origin': 'null' }
        ]
    
    def is_vulnerable(self, response):
        if response.headers.get("Access-Control-Allow-Origin") in ( "*", self.__rand_origin, "null" ):
            return Status.Vulnerable

        if response.headers.get("Access-Control-Allow-Credentials") == "true":
            return Status.Maybe
        
        return Status.NotVulnerable