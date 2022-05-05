
import yaml, os.path
from core.config.builder import ConfigBuilder
from core.request import Headers
from core.config.module import *
from core.config.rock import *

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

class OptionsBuilder(ConfigBuilder):

    def __init__(self, data) -> None:
        ConfigBuilder.__init__(self, data)

    def buildSharedData(self, cfghandler: Config):
        cfghandler.SetTarget(self.data.target)
        cfghandler.SetThreads(self.data.threads)
        cfghandler.SetHeaders(self.buildHeaders())
        
        if self.data.verbose:
            cfghandler.enableVerbose()

    def buildSharedEnumerationData(self, cfg: EnumeratationConfig):
        self.buildSharedData(cfg)
        cfg.SetTimeout(self.data.timeout)
        cfg.SetSources(self.buildSources())
        sources = self.buildSources()

        if sources:
            cfg.SetSources(sources)

        if self.data.recursive:
            cfg.enableRecursive()

    def buildSources(self):
        if self.data.sources:
            if ',' in self.data.sources:
                return self.data.sources.split(',')

            else:
                return [self.data.sources]

    def buildList3rConfig(self):
        if self.data.sublist3r:
            list3r = List3rConfig()
            self.buildSharedEnumerationData(list3r)
            return list3r

    def buildFinderConfig(self):
        finder  = FinderConfig()
        apisfmt = self.data.subfinder_apis

        self.buildSharedEnumerationData(finder)
        finder.SetMaxEnumerationTime(self.data.maxEnumerationTime)

        if self.data.subfinder_all:
            finder.UseAll()

        if apisfmt:
            apis    = {}

            if os.path.isfile(apisfmt):
                try:
                    with open(apisfmt, 'r') as stream:
                        data = yaml.load(stream, Loader=Loader)

                    for key in data.keys():
                        apis[key.capitalize()] = data[key]
                except:
                    raise ValueError("Invalid yaml")

            elif ',' in apisfmt:
                for fmt in apisfmt.split(','):
                    if ':' in fmt:
                        key, value = fmt.split(':')
                        apis[key.capitalize()]  = value.split('+') if '+' in value else [value]
                    else:
                        raise ValueError("Invalid subfinder APIs format")

            else:
                if ':' in apisfmt:
                    key, value = apisfmt.split(':')
                    apis[key.capitalize()]  = value.split('+') if '+' in value else [value]
                else:
                    raise ValueError("Invalid subfinder APIs format")


            finder.SetAPIs(apis)


        return finder

    def buildReverseIPConfig(self):
        if self.data.revip:
            revip = ReverseIPConfig()
            self.buildSharedEnumerationData(revip)
            return revip
    
    def buildHeaders(self):
        return Headers(Headers.Parser.toDict(self.data.headers) if self.data.headers else dict())

    def buildMode(self):
        mode = self.data.mode.lower()
        modecfg = RockMode()

        if '+' in mode and ('s', 'scan') and ('r', 'recon'):
            modecfg.SetModeToBoth()

        elif mode in ('s', 'scan'):
            modecfg.SetModeToScan()

        elif mode in ('r', 'recon'):
            modecfg.SetModeToRecon()

        elif mode in ('c', 'crawl'):
            modecfg.SetModeToCrawl()

        return modecfg

    def buildExcludedModules(self):
        excluded_modules = ExcludedModules()

        if self.data.included_modules:
            included     = self.data.included_modules.split(',') if ',' in self.data.included_modules else [self.data.included_modules]
            exclude_case = False
            excluded     = []

            for module in included:
                if module.startswith('-'):
                    exclude_case = True
                    excluded.append(module[1:])

            if exclude_case:
                excluded_modules.excludeL(excluded)

            else:
                excluded_modules.includeL(included)

        return excluded_modules

    def buildModulesOptions(self):
        options = ModulesOptions()

        if self.data.collaborator: # It's shared between modules
            options.register_common('collaborator', self.data.collaborator)

        if self.data.sqlmap:
            options.register('sqli', 'sqlmap', self.data.sqlmap)

        if self.data.xsshunter:
            options.register('xss', 'xsshunter', self.data.xsshunter)

        return options

    def buildOutput(self):
        if self.data.output:
            output = OutputConfig()
            output.SetFileName(self.data.output)
            output.enableOutput()

            if self.data.format == "text":
                output.SetFormat(Format.Text)

            else:
                return None
            
            return output

    def buildCrawler(self):
        crawler = CrawlerConfig()
        self.buildSharedData(crawler)
        crawler.SetDepth(self.data.depth)

        if self.data.subsInScope:
            crawler.enableSubsInScope()

        if self.data.insecure:
            crawler.enableInsecure()

        if self.data.nocrawl:
            crawler.disable()

        return crawler
