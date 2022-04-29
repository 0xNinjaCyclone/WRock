

from gorock.subfinder import SubFinder
from core.config.enumerator import FinderConfig
from core.recon.subenum.enumerator import IDomainEnumerator

class Finder(SubFinder, IDomainEnumerator):
    """
        from core.recon.subenum.subfinder.finder import Finder

        # create an instance
        f = Finder("example.com")
        
        # version
        print(f.Version())
        
        # list of AllSources
        pList = f.GetAllSources()

        f.SetSources([Finder.Property.Virustotal])
        f.SetAPI(Finder.Property.Virustotal, ["54822c1a98e95c06f.........................."])
        
        # run and get list of results
        subdomains = f.Start()
        
        for subdomain in subdomains:
            print(subdomain)
    """

    class Property:
        # Finder property names
        Resolvers       = "Resolvers"
        Sources         = "Sources"
        AllSources      = "AllSources"
        Recursive       = "Recursive"
        ExcludeSources  = "ExcludeSources"
        Binaryedge      = "Binaryedge"
        Censys          = "Censys"
        Certspotter     = "Certspotter"
        Chaos           = "Chaos"
        Chinaz          = "Chinaz"
        DNSDB           = "DNSDB"
        GitHub          = "GitHub"
        IntelX          = "IntelX"
        PassiveTotal    = "PassiveTotal"
        Recon           = "Recon"
        Robtex          = "Robtex"
        SecurityTrails  = "SecurityTrails"
        Shodan          = "Shodan"
        Spyse           = "Spyse"
        ThreatBook      = "ThreatBook"
        URLScan         = "URLScan"
        Virustotal      = "Virustotal"
        ZoomEye         = "ZoomEye"
        Fofa            = "Fofa"


    def __init__(self, config: FinderConfig) -> None:
        
        SubFinder.__init__(
            self, 
            config.GetTarget(), 
            config.GetThreads(), 
            config.GetTimeout(), 
            config.GetMaxEnumerationTime(),
            config.isRecursiveEnabled(),
            False # Do not use all subfinder sources, We can enable via 'self.UseAll()' API
        )

        IDomainEnumerator.__init__(self, config)

        self.__load_apis__(config.GetAPIs())

                
    def isEnumerator(self, obj):
        pass

    def GetAllEnumerators(self):
        return { 
            enumerator.lower() : enumerator.lower() for enumerator in self.GetAllSources() 
        }

    def SetProperty(self, propname: str, propval):
        # Set list of properties if user passed a list contain properties
        # Else set default values 

        if isinstance(propval, list):
            SubFinder.SetProperty(self, propname, propval)

        elif isinstance(propval, str):
            self.SetProperty(propname, self.GetProperty(propname))

        else:
            raise TypeError

    def SetSources(self, sources):
        # Set list of sources if user passed a list contain sources
        # Else set default values like AllSources depending on the value passed by the user

        if isinstance(sources, list):
            self.SetProperty(Finder.Property.Sources, [source.lower() for source in sources])
        
        elif isinstance(sources, str):
            self.SetProperty(Finder.Property.Sources, self.GetProperty(sources))

        else:
            raise TypeError

    def GetSources(self):
        return self.GetProperty(Finder.Property.Sources)

    def GetAllSources(self):
        return self.GetProperty(Finder.Property.AllSources)

    def SetAPI(self, source, APIs: list):
        self.SetProperty(source, APIs)

    def SetExcludeSources(self, sources: list):
        self.SetProperty(Finder.Property.ExcludeSources, sources)

    def GetExcludedSources(self):
        return self.GetProperty(Finder.Property.ExcludeSources)

    def __load_apis__(self, apis):
        if apis:
            for source, api in apis.items():
                self.SetAPI(source, api)
