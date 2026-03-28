
from enum import Enum, auto
from core.http.headers import Headers


class Verbosity:

    def __init__(self) -> None:
        self.__verbose = False
        self.__level   = None

    def Enable(self):
        self.__verbose = True

    def IsEnabled(self):
        return self.__verbose

    def SetLevel(self, level):
        self.__level = level

    def GetLevel(self):
        return self.__level
    

class WRockProxy( dict ):

    def __init__(self, proxy):
        self.__proto  = None
        self.__server = None
        self.__port   = None
        self.__user   = None
        self.__pass   = None

        if '://' not in proxy:
            proxy = "http://" + proxy

        self.__proto, info = proxy.split( '://' )

        if '@' in info:
            auth_info, info = info.split( '@', 1 )
            if ':' not in auth_info:
                raise ValueError("Invalid proxy")

            self.__user, self.__pass = auth_info.split( ':', 1 ) 

        if ':' not in info:
            self.__port = {
                "http": 80,
                "https": 443,
                "socks5": 1080
            }[ self.__proto ]

        else:
            self.__server, self.__port = ( lambda x: (x[0], int(x[1])) )( info.split( ':' ) )

        proxy = self.prepare()
        self[ "http" ] = proxy
        self[ "https" ] = proxy

    def get_auth_user(self):
        return self.__user

    def get_auth_pass(self):
        return self.__pass
    
    def auth_required(self):
        return self.__user and self.__pass
    
    def get_server(self):
        return self.__server
    
    def get_port(self):
        return self.__port
    
    def get_proto(self):
        return self.__proto
    
    def prepare(self):
        return f"{self.get_proto()}://" + \
        ( f"{self.get_auth_user()}:{self.get_auth_pass()}@" if self.auth_required() else "" ) + \
        f"{self.get_server()}:{self.get_port()}"

    

class Config:
    def __init__(self) -> None:
        self.__target  = None
        self.__threads = 1
        self.__headers = None
        self.__verbose = None
        self.__proxy   = None
        

    def SetTarget(self, target):
        self.__target = target

    def GetTarget(self):
        return self.__target
    
    def SetThreads(self, threads):
        self.__threads = threads

    def GetThreads(self):
        return self.__threads

    def SetHeaders(self, headers: Headers):
        self.__headers = headers

    def GetHeaders(self):
        return self.__headers

    def SetVerbosity(self, v: Verbosity):
        self.__verbose = v

    def GetVerbosity(self):
        return self.__verbose
    
    def SetProxy(self, proxy: WRockProxy):
        self.__proxy = proxy

    def GetProxy(self):
        return self.__proxy


class Format(Enum):
    Text    = auto()
    Json    = auto()
    Html    = auto()

class OutputConfig:

    def __init__(self) -> None:
        self.__filename   = None
        self.__format     = None
        self.__enable     = False

    def SetFileName(self, fileName):
        self.__filename = fileName

    def GetFileName(self):
        return self.__filename

    def SetFormat(self, format):
        self.__format = format

    def GetFormat(self):
        return self.__format

    def isEnable(self):
        return self.__enable

    def enableOutput(self):
        self.__enable = True

    def disableOutput(self):
        self.__enable = False


class Mode(Enum):
    Both      = auto()
    Scan      = auto()
    Recon     = auto()
    Crawl     = auto()
    JsAnalyze = auto()
    Fuzz      = auto()

class RockMode:

    def __init__(self) -> None:
        self.__mode = None

    def SetModeToBoth(self):
        self.__mode = Mode.Both

    def SetModeToScan(self):
        self.__mode = Mode.Scan

    def SetModeToRecon(self):
        self.__mode = Mode.Recon

    def SetModeToCrawl(self):
        self.__mode = Mode.Crawl

    def SetModeToJsAnalyze(self):
        self.__mode = Mode.JsAnalyze

    def SetModeToFuzz(self):
        self.__mode = Mode.Fuzz

    def GetMode(self):
        return self.__mode



