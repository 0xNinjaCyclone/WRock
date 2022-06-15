
import sys, os, inspect, requests
from concurrent.futures import ThreadPoolExecutor
from core.config.scanner import ScannerConfig
from core.scan.module import *
from core.scan.result import ScanResults
from core.utils import rduplicate
from core.crawler.crawl import crawl
from core.data import rockPATH


class ScanExecutor:

    def __init__(self, config: ScannerConfig, scantype) -> None:
        self.results    = ScanResults()
        self.config     = config
        self.url        = self.config.GetTarget()
        self.headers    = self.config.GetHeaders()
        self.threads    = self.config.GetThreads()
        self.excludedM  = self.config.GetExcludedModules()
        self.rock_path  = rockPATH()
        self.scantype   = scantype
        self.LoadAllModules()


    def GetAllModules(self):
        subclasses = []
        callers_module = sys._getframe(1).f_globals['__name__']
        classes = inspect.getmembers(sys.modules[callers_module], inspect.isclass)
        for _ , obj in classes: # return (className , class_object)
            if not self.__isabstractscanner__(obj) and issubclass(obj, BaseScanner):
                subclasses.append(obj)
            
        return subclasses
        

    def LoadAllModules(self):
        self.__loadmodules__(os.path.join(self.rock_path, 'modules', self.scantype.MODPATH))
            
        # Common modules
        self.__loadmodules__(os.path.join(self.rock_path, 'modules', CommonScanner.MODPATH))

    
    def run(self, url, MODULE):
        config = self.config.GetModuleConfig()
        config.SetTarget(url)
        obj = MODULE(config)

        if obj.check():
            self.results.Add(obj.run())
            

    def reachable(self):
        try:
            requests.get(self.url, timeout=30)
            return True
        except:
            return False
            

    def Start(self) -> ScanResults:
        if not self.reachable():
            raise Exception(f"This server is unreachable !!")

        return self.start()

        
    def start(self) -> ScanResults:
        """ chlid class should override this function """
        pass

    def __loadmodules__(self, path):
        for py in [f[:-3] for f in os.listdir(path) if f.endswith('.py') and self.excludedM.included(f)]:
            mod = __import__('.'.join(['modules', path.split('/')[-1], py]), fromlist=[py])
            classes = [getattr(mod, x) for x in dir(mod) if isinstance(getattr(mod, x), type)]
            for cls in classes:
                setattr(sys.modules[__name__], cls.__name__, cls)

    def __isabstractscanner__(self, cls):
        return 'core/scan' in inspect.getfile(cls)

class GeneralScanExecutor(ScanExecutor):

    def __init__(self, config: ScannerConfig) -> None:
        ScanExecutor.__init__(self, config, GeneralScanner)


    def start(self):
        crawler_cfg = self.config.GetCrawlerConfig()
        urls = rduplicate(crawl(crawler_cfg)) if crawler_cfg.isEnabled() else [self.config.GetTarget()]

        for MODULE in self.GetAllModules():
            with ThreadPoolExecutor(max_workers=self.threads) as executor:
                for url in urls:
                    executor.submit(self.run, url, MODULE)


        return self.results

