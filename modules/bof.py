
import random, string
from core.scanner.module import *


class BufferOverFlow( ParamsScanner ):

    def __init__(self, config, info = {
        "Authors": ["Abdallah Mohamed"],
        "Name": "Buffer overflow",
        "Description": "The product copies an input buffer to an output buffer without verifying that the size of the input buffer is less than the size of the output buffer, leading to a buffer overflow.",
        "Risk": Risk.Medium,
        "Referances": [
            "https://cwe.mitre.org/data/definitions/120.html"
        ]
    }) -> None:
        ParamsScanner.__init__(self, config, info)


    def GetPayloads(self) -> list:
        return [ self.__random_str__( 4096 ) ]

    def is_vulnerable(self, response) -> Status:
        return Status.Vulnerable if response.status_code >= 500 and \
                response.headers.get("Connection") == "close" \
            else \
                Status.NotVulnerable


    def __random_str__(self, n):
        return ''.join( random.choice(string.ascii_letters) for _ in range(n) )
