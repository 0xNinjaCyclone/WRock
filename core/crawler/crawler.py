
from core.config.scanner import CrawlerConfig
from core.request import Headers
from rockrawler import Crawler
     

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
