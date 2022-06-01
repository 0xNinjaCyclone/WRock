
from core.config.base import Config
from core.config.module import *
from core.config.crawler import *
from core.config.enumerator import *


class ScannerConfig(Config):
    def __init__(self) -> None:
        self.__excluded_modules   = None
        self.__module_config      = None
        self.__crawler            = None
        Config.__init__(self)

    
    def SetTarget(self, target):
        if not target.startswith('http'):
            target = 'http://' + target

        if not target.endswith('/'):
            target += '/'

        Config.SetTarget(self, target)
    
    def SetExcludedModules(self, excluded: ExcludedModules):
        self.__excluded_modules = excluded

    def GetExcludedModules(self):
        return self.__excluded_modules

    def SetModuleConfig(self, module: ModuleConfig):
        self.__module_config = module

    def GetModuleConfig(self):
        return self.__module_config

    def SetCrawlerConfig(self, crawler: CrawlerConfig):
        self.__crawler = crawler

    def GetCrawlerConfig(self):
        return self.__crawler

