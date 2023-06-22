
from core.config.crawler import CrawlerConfig
from core.request import Headers
from gorock.rockrawler import Crawler, CrawlerResult
     

class WebCrawler(Crawler):

    def __init__(self, config: CrawlerConfig) -> None:
        Crawler.__init__(
            self, 
            config.GetTarget(), 
            config.GetThreads(),
            config.GetDepth(),
            config.isSubsInScopeEnabled(),
            config.isInsecureEnabled(),
            Headers.Parser.toRaw(config.GetHeaders()),
            config.isGetStatusCodeEnabled(),
            config.isNoOutOfScopeEnabled()
        )

    def Start(self) -> CrawlerResult:
        '''
            CrawlerResult methods:
                Transform()     -> Transform the result to a dictionary
                GetJsFiles()    -> a list of js urls files
                GetEmails()     -> a list of crawled emails
                GetEndPoints()  -> a list of dict that contains all endpoints
                            [
                                {
                                    "url": "http://target/path/to/endpoint",
                                    "status_code": 200 
                                    "in_scope: True # indicates if the url in scope or not
                                    "m_type": "METHOD" # Get or Post ?
                                    "params": [
                                        {
                                        "name": "param name",
                                        "value": "param value",
                                        "p_type": "param type" file or text or submit or what ?
                                        },
                                        {
                                            
                                        }
                                    ]
                                },
                                {

                                }
                            ]
        '''

        return Crawler.Start(self)
