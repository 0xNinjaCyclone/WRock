
from core.scanner.module import *


class SSTI( ParamsScanner ):

    def __init__(self, config, info = {
        "Authors": ["Abdallah Mohamed"],
        "Name": "Server Side Template Injection",
        "Description": "The product uses a template engine to insert or process externally-influenced input, but it does not neutralize or incorrectly neutralizes special elements or syntax that can be interpreted as template expressions or other code directives when processed by the engine.",
        "Risk": Risk.Critical,
        "Referances": [
            "https://cwe.mitre.org/data/definitions/1336.html"
        ]
    }) -> None:
        ParamsScanner.__init__(self, config, info)

        self.__n = random.randint( 11, 19 )
        self.__r = self.__n * self.__n
        self.__baseline_resp = self.GetRequester().Send()

    def GetPayloads(self):
        return [
            "{{%d*%d}}" % ( self.__n, self.__n ),
            "${%d*%d}" % ( self.__n, self.__n ),
            "#{%d*%d}" % ( self.__n, self.__n ),
            "<%%= %d*%d %%>" % ( self.__n, self.__n ),
            "#set($x=%d*%d)$x" % ( self.__n, self.__n )
        ]
    
    def is_vulnerable(self, response):
        if str(self.__r) in response.text and str(self.__r) not in self.__baseline_resp.text:
            return Status.Vulnerable
        
        return Status.NotVulnerable
    

class BlindSSTI( ParamsScanner ):

    TIMING_THRESHOLD = 3

    def __init__(self, config, info = {
        "Authors": ["Abdallah Mohamed"],
        "Name": "Server Side Template Injection",
        "Description": "The product uses a template engine to insert or process externally-influenced input, but it does not neutralize or incorrectly neutralizes special elements or syntax that can be interpreted as template expressions or other code directives when processed by the engine.",
        "Risk": Risk.Critical,
        "Referances": [
            "https://cwe.mitre.org/data/definitions/1336.html"
        ]
    }) -> None:
        ParamsScanner.__init__(self, config, info)

        self.__baseline_resp = self.GetRequester().Send()


    def GetPayloads(self):
        return [
            "{{range(5000000)|list}}",
            "{{range(1,5000000)}}",
            "<#assign x=7?repeat(5000000)>",
            "<%= (1..5_000_000).to_a.size %>",
            "<%%= sleep %d %%>" % ( self.TIMING_THRESHOLD*2 ),
            "#set($i = 0)\n#foreach($x in [1..5000000])\n#set($i = $i + 1)\n#end\n$i"
        ]
    
    def is_vulnerable(self, response):
        if response.elapsed.total_seconds() - self.__baseline_resp.elapsed.total_seconds() >= self.TIMING_THRESHOLD:
            return Status.Vulnerable
        
        return Status.NotVulnerable