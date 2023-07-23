from core.scanner.module import *

class OpenRedirect(ParamsScanner):

    def __init__(self, config, info={
        "Authors": ["Hossam Ehab"],
        "Name": "Open Redirect Vulnerability",
        "Description": 'Open redirect vulnerability is a security flaw that allows attackers to redirect users to malicious websites via trusted, but improperly validated, redirects.',
        "Risk": Risk.Medium,
        "References": [
            "https://cwe.mitre.org/data/definitions/601"
        ]
    }) -> None:
        ParamsScanner.__init__(self, config, info)
        self.__malicious_loc = "http://malicious.webrock.com/"
        self.SetRequestArgs(allow_redirects=False)

    def check(self):
        endpoint = self.GetEndPoint()
        params = endpoint.GetAllParams()

        if bool(params):
            for param, value in params.items():
                if value.startswith("http://") or value.startswith("https://") or endpoint.GetParamTypeByName(param) == "url":
                    self.InsertParamToScan(param)
                    return True

        return False

    def GetPayloads(self):
        return [
            self.__malicious_loc,
            self.__malicious_loc[5:],
            "/\\/" + self.__malicious_loc[7:]
        ]

    def is_vulnerable(self, response) -> bool:

        return (

            response.status_code >= 300 and
            response.status_code < 400 and
            "Location" in response.headers and
            response.headers["Location"] in self.__malicious_loc
            
        )
