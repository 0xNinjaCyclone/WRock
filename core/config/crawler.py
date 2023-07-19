
from core.config.base import Config


class CrawlerConfig(Config):
    def __init__(self) -> None:
        self.__depth            = 5
        self.__subsInScope      = False
        self.__insecure         = False
        self.__nocrawl          = False
        self.__getstatuscode    = False
        self.__noOutOfScope     = False
        self.__disallowed       = []
        Config.__init__(self)


    def SetTarget(self, target):
        if not target.startswith('http'):
            target = 'http://' + target

        if not target.endswith('/'):
            target += '/'

        Config.SetTarget(self, target)

    def SetDepth(self, depth):
        self.__depth = depth

    def GetDepth(self):
        return self.__depth

    def enableSubsInScope(self):
        self.__subsInScope = True

    def isSubsInScopeEnabled(self):
        return self.__subsInScope

    def enableInsecure(self):
        self.__insecure = True

    def isInsecureEnabled(self):
        return self.__insecure

    def disable(self):
        self.__nocrawl = True

    def isEnabled(self):
        return not self.__nocrawl

    def isGetStatusCodeEnabled(self):
        return self.__getstatuscode

    def enableGetStatusCode(self):
        self.__getstatuscode = True

    def isNoOutOfScopeEnabled(self):
        return self.__noOutOfScope

    def enableNoOutOfScope(self):
        self.__noOutOfScope = True

    def SetDisallowed(self, disallowed):
        self.__disallowed = disallowed

    def GetDisallowed(self):
        return self.__disallowed
    

class CrawlerProxy:

    def __init__(self) -> None:
        self.__crawler   = None

    def SetCrawlerConfig(self, crawler: CrawlerConfig):
        self.__crawler = crawler

    def GetCrawlerConfig(self):
        return self.__crawler
