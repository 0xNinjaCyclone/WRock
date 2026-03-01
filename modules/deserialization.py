
import base64
from core.scanner.module import *


class IOD( ParamsScanner ):

    def __init__(self, config, info = {
        "Authors": ["Abdallah Mohamed"],
        "Name": "Insecure Object Deserialization",
        "Description": "The product deserializes untrusted data without sufficiently ensuring that the resulting data will be valid.",
        "Risk": Risk.Critical,
        "Referances": [
            "https://cwe.mitre.org/data/definitions/502.html"
        ]
    }) -> None:
        ParamsScanner.__init__(self, config, info)

    def check(self):
        e = self.GetEndPoint()
        for pname in e.GetAllParamNames():
            if e.GetParamTypeByName( pname ) in ( '', "text", "hidden" ):
                v = e.GetParamValueByName( pname )
                if pname.upper() in ( "__VIEWSTATE", "__EVENTVALIDATION" ) or not v or \
                    any( i in v for i in ["rO0AB", "O:", "gAS", "BAh", "dDw"] ):
                    self.InsertParamToScan( pname )

        return self.HaveParamsToScan()
    
    def GetPayloads(self):
        return [
            'O:8:"StdClass":1:{s:4:"test";s:5:"WRock";}BROKEN', # Broken PHP serialized object
            base64.b64encode( b"\xac\xed\x00\x05\x00\x00\x00" ).decode(), # Corrupted Java serialization header
            base64.b64encode( b"\x80\x04\x95\x00\x00" ).decode(), # Corrupted pickle stream
            base64.b64encode( b"\x04\x08\x00\x00" ).decode(), # Corrupted Ruby Marshal stream
            base64.b64encode( b"WRockTestViewState" ).decode()[:-2] # .Net ViewState
        ]
    
    def is_vulnerable(self, response):
        for signature in [
            # Java
            "java.io.InvalidClassException",
            "java.io.StreamCorruptedException",
            "Invalid stream header",
            "ObjectInputStream",

            # PHP
            "unserialize():",
            "Unexpected end of serialized data",

            # Python
            "pickle.UnpicklingError",
            "invalid load key",

            # Ruby
            "marshal data too short",

            # .NET
            "ViewStateException",
            "LosFormatter"
        ]:
            if signature in response.text:
                return Status.Vulnerable

        return Status.NotVulnerable
