
from core.config.scanner import CrawlerConfig
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
            Headers.Parser.toRaw(config.GetHeaders().GetAll())
        )

    def Start(self) -> CrawlerResult:
        '''
            CrawlerResult methods:
                GetJsFiles()    -> a list of js urls files
                GetEmails()     -> a list of crawled emails
                GetEndPoints()  -> a list of dict that contains all endpoints
                            [
                                {
                                    "url": "http://target/path/to/endpoint",
                                    "m_type": "METHOD" # Get or Post ?
                                    "params": {
                                        "name": "param name",
                                        "value": "param value",
                                        "p_type": "param type" file or text or submit or what ?
                                    }
                                },
                                {

                                }
                            ]
        '''

        return Crawler.Start(self)
