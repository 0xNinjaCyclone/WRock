
from core.config.base import Config
from core.config.module import *
from core.config.crawler import *
from core.config.enumerator import *


class ScannerConfig(Config, CrawlerProxy):
    def __init__(self) -> None:
        self.__excluder           = None
        self.__module_config      = None
        Config.__init__(self)
        CrawlerProxy.__init__(self)

    
    def SetTarget(self, target):
        if not target.startswith('http'):
            target = 'http://' + target


        Config.SetTarget(self, target)
    
    def SetExcluder(self, excluder):
        self.__excluder = excluder

    def GetExcluder(self):
        return self.__excluder

    def SetModuleConfig(self, module: ModuleConfig):
        self.__module_config = module

    def GetModuleConfig(self):
        return self.__module_config

    
class ScannerProxy:

    def __init__(self) -> None:
        self.__scanner = None

    def SetScannerConfig(self, scanner: ScannerConfig):
        self.__scanner = scanner

    def GetScannerConfig(self):
        return self.__scanner