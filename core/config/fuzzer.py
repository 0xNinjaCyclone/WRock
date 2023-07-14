
from core.config.base import Config


class FuzzerConfig( Config ):

    def __init__(self) -> None:
        self.__wordlists = list()
        self.__recursion = False
        self.__recursionDepth = 2
        self.__timeout = 10
        self.__method = str()
        self.__data = str()
        self.__configFile = str()
        self.__inputMode = str()
        self.__inputCommands = list()
        self.__reqFile = str()
        self.__autoCalibrationStrategy = str()
        self.__recursionStrategy = str()
        self.__requestProto = str()
        self.__scrapers = str()
        self.__matcherMode = str()
        self.__matchers = dict()
        self.__filters = dict()
        Config.__init__(self)

    def SetWordLists(self, wordlists: list):
        self.__wordlists = wordlists

    def GetWordLists(self):
        return self.__wordlists

    def EnableRecursion(self):
        self.__recursion = True

    def IsRecursionEnabled(self):
        return self.__recursion

    def SetRecursionDepth(self, depth: int):
        self.__recursionDepth = depth

    def GetRecursionDepth(self):
        return self.__recursionDepth

    def SetTimeout(self, timeout: int):
        self.__timeout = timeout

    def GetTimeout(self):
        return self.__timeout

    def SetMethod(self, method: str):
        self.__method = method

    def GetMethod(self):
        return self.__method

    def SetData(self, data: str):
        self.__data = data

    def GetData(self):
        return self.__data

    def SetConfigFile(self, cfgfile: str):
        self.__configFile = cfgfile

    def GetConfigFile(self):
        return self.__configFile

    def SetInputMode(self, mode: str):
        self.__inputMode = mode

    def GetInputMode(self):
        return self.__inputMode

    def SetInputCommands(self, cmds: list):
        self.__inputCommands = cmds

    def GetInputCommands(self):
        return self.__inputCommands

    def SetRequestFile(self, file: str):
        self.__reqFile = file

    def GetRequestFile(self):
        return self.__reqFile

    def SetAutoCalibrationStrategy(self, strategy: str):
        self.__autoCalibrationStrategy = strategy

    def GetAutoCalibrationStrategy(self):
        return self.__autoCalibrationStrategy

    def SetRecursionStrategy(self, strategy: str):
        self.__recursionStrategy = strategy

    def GetRecursionStrategy(self):
        return self.__recursionStrategy

    def SetRequestProto(self, proto: str):
        self.__requestProto = proto

    def GetRequestProto(self):
        return self.__requestProto

    def SetScrapers(self, scrapers: str):
        self.__scrapers = scrapers

    def GetScrapers(self):
        return self.__scrapers

    def SetMatcherMode(self, mode: str):
        self.__matcherMode = mode

    def GetMatcherMode(self):
        return self.__matcherMode

    def SetMatchers(self, matchers: dict):
        self.__matchers = matchers

    def GetMatchers(self):
        return self.__matchers

    def SetFilters(self, filters: dict):
        self.__filters = filters

    def GetFilters(self):
        return self.__filters


class FuzzerProxy:

    def __init__(self) -> None:
        self.__fuzzer = None

    def SetFuzzerConfig(self, fuzzer: FuzzerConfig):
        self.__fuzzer = fuzzer

    def GetFuzzerConfig(self):
        return self.__fuzzer
