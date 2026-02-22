
import csv, requests, re, os.path, urllib.parse
from core.data import rockPATH
from core.crawler.crawl import crawl
from core.config.jsanlyzer import *
from concurrent.futures import ThreadPoolExecutor


# src => https://github.com/odomojuli/RegExAPI/blob/master/regex.csv
EXTRACTORS = os.path.join(rockPATH(), "core/jsanalyzer/regex.csv")

# src => https://github.com/GerbenJavado/LinkFinder/blob/1debac5dace4724fd6187c06f133578dae51c86f/linkfinder.py#L28
LINK_EXTRACTOR = r"""

  (?:"|')                               # Start newline delimiter

  (
    ((?:[a-zA-Z]{1,10}://|//)           # Match a scheme [a-Z]*1-10 or //
    [^"'/]{1,}\.                        # Match a domainname (any character + dot)
    [a-zA-Z]{2,}[^"']{0,})              # The domainextension and/or path

    |

    ((?:/|\.\./|\./)                    # Start with /,../,./
    [^"'><,;| *()(%%$^/\\\[\]]          # Next character can't be...
    [^"'><,;|()]{1,})                   # Rest of the characters can't be

    |

    ([a-zA-Z0-9_\-/]{1,}/               # Relative endpoint with /
    [a-zA-Z0-9_\-/.]{1,}                # Resource name
    \.(?:[a-zA-Z]{1,4}|action)          # Rest + extension (length 1-4 or action)
    (?:[\?|#][^"|']{0,}|))              # ? or # mark with parameters

    |

    ([a-zA-Z0-9_\-/]{1,}/               # REST API (no extension) with /
    [a-zA-Z0-9_\-/]{3,}                 # Proper REST endpoints usually have 3+ chars
    (?:[\?|#][^"|']{0,}|))              # ? or # mark with parameters

    |

    ([a-zA-Z0-9_\-]{1,}                 # filename
    \.(?:php|asp|aspx|jsp|json|
         action|html|js|txt|xml)        # . + extension
    (?:[\?|#][^"|']{0,}|))              # ? or # mark with parameters

  )

  (?:"|')                               # End newline delimiter

"""


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
    PLATFORM = 0
    KEYTYPE  = 1
    
    def __init__(self) -> None:
        self.__extractors = list()

    def LoadAll(self):
        self.__loadby__(all=True)

    def LoadByPlatforms(self, platforms: list):
        self.__loadby__(platforms, ExtractorsLoader.PLATFORM)

    def LoadByKeys(self, keys):
        self.__loadby__(keys, ExtractorsLoader.KEYTYPE)

    def GetAll(self) -> list[ Extractor ]:
        return self.__extractors

    def GetByKeyType(self, keyType) -> list[ Extractor ]:
        return [ extractor for extractor in self.__extractors if extractor.GetKeyType() == keyType ]

    def GetByPlatform(self, platform) -> list[ Extractor ]:
        return [ extractor for extractor in self.__extractors if extractor.GetPlatform() == platform ]

    def __loadby__(self, data: list = [], index = 0, all = False):
        with open(EXTRACTORS, 'r') as f:
            reader = csv.reader(f)
            self.__extractors = [ Extractor(row[0], row[1], row[2], row[3]) for row in reader if all or row[index] in data ]


class SensitiveDataItem:

    def __init__(self, data, extractor) -> None:
        self.__data      = data
        self.__extractor = extractor

    def GetData(self) -> list[ str ]:
        return self.__data

    def GetExtractor(self) -> Extractor:
        return self.__extractor


class AnalysisResult:
    def __init__(self, jslink: str) -> None:
        self.__jslink    = jslink
        self.__items     = list()
        self.__endpoints = list() # Had better be compatible with Crawler.endpoints

    def GetJsLink(self) -> str:
        return self.__jslink

    def GetItems(self) -> list[ SensitiveDataItem ]:
        return self.__items

    def AppendItem(self, item: SensitiveDataItem):
        self.__items.append(item)

    def GetEndPoints(self) -> list[ dict ]:
        return self.__endpoints
    
    def AppendEndPoint(self, url, in_scope=False):
        self.__endpoints.append(
            {
                "url": url,
                "status_code": 0,
                "in_scope": in_scope,
                "m_type": "GET",
                "params": []
            }
        )


class AnalysisResults( list ):
    def __init__(self, iterable):
        list.__init__(self, iterable)

    def GetFilesHaveSensitives(self) -> list[ AnalysisResult ]:
        return [ sensitive for sensitive in self if bool( sensitive.GetItems() ) ]
    
    def GetAllEndPoints(self) -> list[ dict ]:
        return [ endpoint for result in self for endpoint in result.GetEndPoints() ]

    def GetNumberOfJsLinks(self) -> int:
        return len( self )
    
    def GetNumberOfEndpoints(self) -> int:
        ctr = 0

        for result in self:
            ctr += len( result.GetEndPoints() )

        return ctr

    def GetNumberOfFilesHaveSensitives(self) -> int:
        ctr = 0

        for result in self:
            ctr += bool( len(result.GetItems()) )

        return ctr

    def GetNumberOfSensitives(self) -> int:
        sensitives = 0

        for result in self:
            for item in result.GetItems():
                sensitives += len( item.GetData() )

        return sensitives

    def Transform(self) -> list:
        analyzer_result = []
        key = "Items"

        for result in self:
            dResult = dict()
            dResult["JsLink"] = result.GetJsLink()
            dResult["EndPoints"] = result.GetEndPoints()
            
            if not key in dResult:
                dResult[key] = list()

            for i in result.GetItems():
                x = i.GetExtractor()

                dResult[key].append({
                    "Extractor": {
                        "Platform":   x.GetPlatform(),
                        "KeyType":    x.GetKeyType(),
                        "Expression": x.GetExpression(),
                        "Source":     x.GetSource()
                    },
                    "Data":      i.GetData()
                })

            analyzer_result.append( dResult )

        return analyzer_result


class Analyzer:

    def __init__(self, config: JsAnalyzerConfig) -> None:
        self.__config     = config

    def Analyze(self, jsLink) -> AnalysisResult:
        result  = AnalysisResult(jsLink)
        content = self.__getjscontent__(jsLink)

        target_host = urllib.parse.urlparse(self.__config.GetTarget()).hostname
        prog = re.compile(LINK_EXTRACTOR, re.VERBOSE)
        all_matches = list( dict.fromkeys( [ match.group(1) for match in re.finditer(prog, content) ] ) )
        for match in all_matches:
            result.AppendEndPoint(match, urllib.parse.urlparse(match).hostname == target_host)

        for extractor in self.__config.GetExtractors():
            prog = re.compile(extractor.GetExpression(), re.X | re.I)
            all_matches = list( dict.fromkeys( [ match.group(0) for match in re.finditer(prog, content) ] ) )

            for match in all_matches:
                results = list( dict.fromkeys(re.findall(match, content, re.I)) )

                if bool(results):
                    result.AppendItem( SensitiveDataItem(results, extractor) )

        return result

    def Start(self) -> AnalysisResults:
        crawler_cfg = self.__config.GetCrawlerConfig()

        with ThreadPoolExecutor(max_workers=self.__config.GetThreads()) as executor:
            features = [ 
                executor.submit(self.Analyze, jsLink) for jsLink in ( crawl( crawler_cfg ).GetJsFiles() if crawler_cfg.isEnabled() else [ self.__config.GetTarget() ] )
            ]


        return AnalysisResults( feature.result() for feature in features )

    def __getjscontent__(self, jsLink) -> str:
        try:
            response = requests.get(jsLink, headers=self.__config.GetHeaders(), timeout=30)
            retval   = response.text if response.ok else str()
        except:
            retval = str()

        return retval