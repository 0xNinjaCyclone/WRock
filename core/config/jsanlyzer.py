
from core.config.base import Config
from core.config.crawler import *


class JsAnalyzerConfig(Config, CrawlerProxy):

    def __init__(self) -> None:
        self.__extractors = None
        Config.__init__(self)
        CrawlerProxy.__init__(self)

    def SetExtractors(self, extractors):
        self.__extractors = extractors

    def GetExtractors(self):
        return self.__extractors


class JsAnalyzerProxy:

    def __init__(self) -> None:
        self.__jsanalyzer = None

    def SetJsAnalyzerConfig(self, jsanalyzer: JsAnalyzerConfig):
        self.__jsanalyzer = jsanalyzer

    def GetJsAnalyzerConfig(self):
        return self.__jsanalyzer