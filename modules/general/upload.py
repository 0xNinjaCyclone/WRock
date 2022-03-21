
from core.scan.module import *
from bs4 import BeautifulSoup

# Disable bs4 warnings
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')


class Upload(GeneralScanner):
    # This module will get all upload functions, without upload any thing

    def __init__(self, config) -> None:
        GeneralScanner.__init__(self, config)

    def check(self) -> bool:
        return True

    def run(self):
        res = self.request.Send()

        try:
            forms = BeautifulSoup(res.text, 'html.parser').find("form")
 
            if forms:        
                for tag in forms.findAll("input"):
                    itype = tag.get("type") # input type

                    if itype:
                        if itype == "file":
                            self.vulnInfo.status = Status.Maybe

        except:
            pass

        return self.GetVulnInfo()