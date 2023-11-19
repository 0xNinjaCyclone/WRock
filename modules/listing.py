
import re
from core.scanner.module import BodyBasedDataExposure, Risk, Status


class DirListing( BodyBasedDataExposure ):

    def __init__(self, config, info = {
        "Authors": ["Abdallah Mohamed"],
        "Name": "Directory Listing",
        "Description": 'A directory listing is inappropriately exposed, yielding potentially sensitive information to attackers.',
        "Risk": Risk.Low,
        "Referances": [
            "https://cwe.mitre.org/data/definitions/548.html"
        ]
    }) -> None:
        BodyBasedDataExposure.__init__(self, config, info)

    def Check(self, data) -> Status:
        v = re.search(r"\bDirectory Listing\b.*(Tomcat|Apache)", data, re.DOTALL) != None or \
            re.search(r"[\s<]+IMG\s*=", data) != None or \
            ("Parent directory" or "Parent Directory") in data


        return Status.Vulnerable if v else Status.NotVulnerable
            
