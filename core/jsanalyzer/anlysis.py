
import csv, requests, re
import os.path
from core.data import rockPATH
from core.crawler.crawl import crawl
from core.config.jsanlyzer import *
from concurrent.futures import ThreadPoolExecutor


# src => https://github.com/odomojuli/RegExAPI/blob/master/regex.csv
EXTRACTORS = os.path.join(rockPATH(), "core/jsanalyzer/regex.csv")


class Extractor:

    def __init__(self, platform, key_type, expression, source) -> None:
        self.__platform   = platform
        self.__key_type   = key_type
        self.__expression = expression
        self.__source     = source

    def GetPlatform(self):
        return self.__platform

    def GetKeyType(self):
        return self.__key_type

    def GetExpression(self):
        return self.__expression

    def GetSource(self):
        return self.__source


class ExtractorsLoader:
    
    def __init__(self) -> None:
        self.__extractors = list()

    def LoadAll(self):
        with open(EXTRACTORS, 'r') as f:
            reader = csv.reader(f)
            self.__extractors = [ Extractor(row[0], row[1], row[2], row[3]) for row in reader ]

    def LoadByPlatforms(self, platforms: list):
        self.__loadby__(platforms, 0)

    def LoadByKeys(self, keys):
        self.__loadby__(keys, 1)

    def GetAll(self):
        return self.__extractors

    def GetByKeyType(self, keyType):
        return [ extractor for extractor in self.__extractors if extractor.GetKeyType() == keyType ]

    def GetByPlatform(self, platform):
        return [ extractor for extractor in self.__extractors if extractor.GetPlatform() == platform ]

    def __loadby__(self, data: list, i):
        with open(EXTRACTORS, 'r') as f:
            reader = csv.reader(f)
            self.__extractors = [ Extractor(row[0], row[1], row[2], row[3]) for row in reader if row[i] in data ]


class SensitiveDataItem:

    def __init__(self, data, extractor) -> None:
        self.__data      = data
        self.__extractor = extractor

    def GetData(self) -> list:
        return self.__data

    def GetExtractor(self) -> Extractor:
        return self.__extractor


class AnalysisResult:
    def __init__(self, jslink) -> None:
        self.__jslink = jslink
        self.__items  = list()

    def GetJsLink(self):
        return self.__jslink

    def GetItems(self):
        return self.__items

    def AppendItem(self, item: SensitiveDataItem):
        self.__items.append(item)


class Analyzer:

    def __init__(self, config: JsAnalyzerConfig) -> None:
        self.__config     = config

    def Analyze(self, jsLink) -> AnalysisResult:
        result  = AnalysisResult(jsLink)
        content = self.__getjscontent__(jsLink)

        for extractor in self.__config.GetExtractors():
            prog = re.compile(extractor.GetExpression(), re.X | re.I)
            all_matches = list( dict.fromkeys( [ match.group(0) for match in re.finditer(prog, content) ] ) )

            for match in all_matches:
                results = re.findall(f".+?{match}.+?", content, re.I)

                if bool(results):
                    result.AppendItem( SensitiveDataItem(results, extractor) )

        return result

    def Start(self) -> list:
        with ThreadPoolExecutor(max_workers=self.__config.GetThreads()) as executor:
            features = [ executor.submit(self.Analyze, jsLink) for jsLink in crawl( self.__config.GetCrawlerConfig() ).GetJsFiles() ]


        return [ feature.result() for feature in features ]

    def __getjscontent__(self, jsLink):
        try:
            response = requests.get(jsLink, headers=self.__config.GetHeaders().GetAll(), timeout=30)
            retval   = response.text if response.ok else str()
        except:
            retval = str()

        return retval