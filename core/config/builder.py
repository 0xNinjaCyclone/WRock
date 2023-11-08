
from core.config.base import *
from core.config.rock import *

class ConfigBuilder:

    def __init__(self, data) -> None:
        self.data = data

    def buildSharedData(self, cfghandler: Config):
        pass

    def buildSharedEnumerationData(self, cfghandler: EnumerationConfig):
        pass

    def buildVerbosity(self):
        pass

    def buildMode(self):
        pass

    def buildHeaders(self):
        pass

    def buildExcluder(self):
        pass

    def buildOutput(self):
        pass

    def buildCrawler(self):
        pass

    def buildJsAnalyzer(self):
        pass

    def buildFuzzer(self):
        pass

    def buildScanner(self):
        scanner = ScannerConfig()
        self.buildSharedData(scanner)
        scanner.SetModuleConfig(self.buildModule())
        scanner.SetExcluder(self.buildExcluder())
        scanner.SetCrawlerConfig(self.buildCrawler())
        return scanner

    def buildModulesOptions(self):
        pass

    def buildModule(self):
        module = ModuleConfig()
        self.buildSharedData(module)
        module.SetModulesOptions(self.buildModulesOptions())
        return module

    def buildList3rConfig(self):
        pass

    def buildFinderConfig(self):
        pass

    def buildReverseIPConfig(self):
        pass

    def buildEnumerator(self):
        enumerator = EnumeratorConfig()
        self.buildSharedEnumerationData(enumerator)
        enumerator.SetList3rConfig(self.buildList3rConfig())
        enumerator.SetFinderConfig(self.buildFinderConfig())
        enumerator.SetReverseIPConfig(self.buildReverseIPConfig())
        return enumerator

    def buildProxy(self):
        return ProxyConfig()

    def buildRock(self):
        rock = RockConfig()
        rock.SetMode(self.buildMode())
        rock.SetVerbosity(self.buildVerbosity())
        rock.SetProxyConfig(self.buildProxy())
        mode = rock.GetMode()
        output = self.buildOutput()
        
        if output:
            rock.SetOutputConfig(output)

        if mode == Mode.Scan:
            rock.SetScannerConfig(self.buildScanner())
        
        elif mode == Mode.Recon:
            rock.SetEnumeratorConfig(self.buildEnumerator())

        elif mode == Mode.Crawl:
            rock.SetCrawlerConfig(self.buildCrawler())

        elif mode == Mode.JsAnalyze:
            rock.SetJsAnalyzerConfig(self.buildJsAnalyzer())

        elif mode == Mode.Fuzz:
            rock.SetFuzzerConfig(self.buildFuzzer())

        elif mode == Mode.Both:
            rock.SetScannerConfig(self.buildScanner())
            rock.SetEnumeratorConfig(self.buildEnumerator())

        return rock