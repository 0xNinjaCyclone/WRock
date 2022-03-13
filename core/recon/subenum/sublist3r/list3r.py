
from core.recon.subenum.enumerator import *
from core.config.enumerator import List3rConfig


class List3r(IDomainEnumerator):

    def __init__(self, config: List3rConfig) -> None:
        IDomainEnumerator.__init__(self, config)

    def isEnumerator(self, obj):
        return obj is not enumratorBase and (enumratorBase in inspect.getmro(obj)) and obj is not SearchEngineEnumerator

    def GetAllEnumerators(self):
        return { 
            'baidu': BaiduEnum,
            'yahoo': YahooEnum,
            'google': GoogleEnum,
            'bing': BingEnum,
            'ask': AskEnum,
            'netcraft': NetcraftEnum,
            'dnsdumpster': DNSdumpster,
            'threatcrowd': ThreatCrowd,
            'crtsh': CrtSearch,
            'passivedns': PassiveDNS
        }

    def Start(self):
        # features container
        features = []

        # subdomains
        subdomains = []
        
        # Start the engines enumeration
        enums = [enum(self.config) for enum in self.GetSources()]
        
        with ThreadPoolExecutor(max_workers=self.config.GetThreads()) as e:
            [features.append(e.submit(enum.enumerate)) for enum in enums]          

        # extract subdomains from threads features
        for feature in features:
            subdomains.extend(feature.result())

        if subdomains:
            subdomains = sorted(subdomains, key=subdomain_sorting_key)

        
        return subdomains
