
from core.config.base import *
from core.config.scanner import *
from core.config.enumerator import *

class RockConfig:

    def __init__(self) -> None:
        self.__mode       = None
        self.__output     = None
        self.__scanner    = None
        self.__crawler    = None
        self.__enumerator = None

    def SetMode(self, mode: RockMode):
        self.__mode = mode

    def GetMode(self):
        return self.__mode.GetMode()

    def SetOutputConfig(self, output: OutputConfig):
        self.__output = output

    def GetOutputConfig(self):
        return self.__output

    def SetScannerConfig(self, scanner: ScannerConfig):
        self.__scanner = scanner

    def GetScannerConfig(self):
        return self.__scanner

    def SetCrawlerConfig(self, crawler: CrawlerConfig):
        self.__crawler = crawler

    def GetCrawlerConfig(self):
        return self.__crawler

    def SetEnumeratorConfig(self, enumerator: EnumeratorConfig):
        self.__enumerator = enumerator

    def GetEnumeratorConfig(self):
        return self.__enumerator
