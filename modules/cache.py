
import random, string
from core.scanner.module import *


class WebCachePoisoning( HeadersScanner ):

    def __init__(self, config: ModuleConfig, info = {
        "Authors": ["Abdallah Mohamed"],
        "Name": "Web cache poisoning",
        "Risk": Risk.High,
        "Description": "Web cache poisoning vulnerabilities arise when an application behind a cache processes input that is not included in the cache key. Attackers can exploit this by sending crafted input to trigger a harmful response that the cache will then save and serve to other users.",
        "Referances": [
            "https://portswigger.net/research/practical-web-cache-poisoning"
        ]
    }) -> None:
        HeadersScanner.__init__(self, config, info)

        self.__canary = self.__random_str__() + ".webrock.net"


    def GetPayloads(self) -> list:
        return [
            { "X-Forwarded-Host":   self.__canary },
            { "X-Host":             self.__canary },
            { "X-Forwarded-Server": self.__canary }
        ]

    def is_vulnerable(self, response) -> bool:
        if not self.__canary in response.text:
            return False

        req = self.GetRequester()
        res = req.Send()
        return self.__canary in res.text

    def __random_str__(self):
        return ''.join( random.choice(string.ascii_lowercase) for _ in range(8) )