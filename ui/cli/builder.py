
import yaml, os.path
from core.config.fuzzer import FuzzerConfig
from core.config.jsanlyzer import JsAnalyzerConfig
from core.scanner.excluder import Excluder
from core.jsanalyzer.anlysis import ExtractorsLoader
from core.logger import Level
from core.utils import *
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
        cfghandler.SetVerbosity(self.buildVerbosity())

    def buildSharedEnumerationData(self, cfg: EnumerationConfig):
        self.buildSharedData(cfg)
        cfg.SetTimeout(self.data.timeout)
        cfg.SetSources(self.buildSources())
        sources = self.buildSources()

        if sources:
            cfg.SetSources(sources)

        if self.data.recursive:
            cfg.enableRecursive()

    def buildVerbosity(self):
        v = Verbosity()

        if self.data.verbose:
            v.Enable()

        level = self.data.level

        if level == 1:
            v.SetLevel(Level.CRITICAL)
        elif level == 2:
            v.SetLevel(Level.INFO)
        elif level == 3:
            v.SetLevel(Level.DEBUG)
        else:
            raise ValueError("Invalid verbosity level")

        return v

    def buildSources(self):
        if self.data.sources:
            if ',' in self.data.sources:
                return self.data.sources.split(',')

            else:
                return [self.data.sources]

    def buildModule(self):
        module              = ConfigBuilder.buildModule(self)
        endpoint            = dict()
        url                 = module.GetTarget() # buildSharedData() had set url as a target here
        endpoint['url']     = url
        endpoint['params']  = list()

        if self.data.post:
            endpoint['m_type'] = "POST"

            for i in self.data.post.split('&'):
                param           = dict()
                pname, temp     = i.split('=')
                pvalue, p_type  = temp.split('|') if '|' in temp else [temp, '']
                param['name']   = pname
                param['value']  = pvalue
                param['p_type'] = p_type
                endpoint['params'].append(param)

        else:
            endpoint['m_type'] = "GET"

        module.SetTarget(endpoint)
                
        return module

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
        return parse_headers_from_file(self.data.headers) if self.data.headers and os.path.isfile(self.data.headers) else Headers(Headers.Parser.toDict(self.data.headers) if self.data.headers else dict())

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

        elif mode in ('a', 'jsanalyze'):
            modecfg.SetModeToJsAnalyze()

        elif mode in ('f', 'fuzz'):
            modecfg.SetModeToFuzz()

        return modecfg

    def buildExcluder(self):
        excluder = Excluder()

        if self.data.included_modules:
            included     = self.data.included_modules.split(',') if ',' in self.data.included_modules else [self.data.included_modules]
            exclude_case = False
            excluded     = []

            for module in included:
                if module.startswith('-'):
                    exclude_case = True
                    excluded.append(module[1:])

            if exclude_case:
                excluder.excludeL(excluded)

            else:
                excluder.includeL(included)

        return excluder

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

            elif self.data.format == "json":
                output.SetFormat(Format.Json)

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

        if self.data.sc:
            crawler.enableGetStatusCode()

        if self.data.noOutOfScope:
            crawler.enableNoOutOfScope()

        if self.data.disallowed:
            crawler.SetDisallowed( self.data.disallowed.split(',') )

        return crawler

    def buildJsAnalyzer(self):
        jsAnalyzer = JsAnalyzerConfig()
        self.buildSharedData(jsAnalyzer)
        jsAnalyzer.SetCrawlerConfig( self.buildCrawler() )

        # Load extractors
        extLoader = ExtractorsLoader()

        if self.data.by_platforms:
            extLoader.LoadByPlatforms( self.data.by_platforms.split(',') )

        elif self.data.by_keys:
            extLoader.LoadByKeys( self.data.by_keys.split(',') )

        else:
            extLoader.LoadAll()

        # Pass the Extractors list to the config
        jsAnalyzer.SetExtractors( extLoader.GetAll() )

        return jsAnalyzer

    def buildFuzzer(self):
        if not self.data.wordlists:
            raise Exception("You must pass wordlists using '--wordlists' option")

        fuzzer = FuzzerConfig()
        self.buildSharedData(fuzzer)
        fuzzer.SetWordLists( self.data.wordlists.split(',') )

        # Set post params
        if self.data.post:
            if '|' in self.data.post:
                raise ValueError("parameter type not required in the fuzz mode")

            fuzzer.SetData( self.data.post )

        if self.data.method:
            fuzzer.SetMethod( self.data.method.upper() )

        if self.data.matchers:
            matchers = {}

            for matcher in self.data.matchers.split('-'):
                matcher = matcher.split(':') if ':' in matcher else [ matcher, '' ]
                matchers[ matcher[0] ] = matcher[1]

            fuzzer.SetMatchers( matchers )

        if self.data.filters:
            filters = {}

            for filter in self.data.filters.split('-'):
                filter = filter.split(':') if ':' in filter else [ filter, '' ]
                filters[ filter[0] ] = filter[1]

            fuzzer.SetFilters( filters )
        
        if self.data.inputMode:
            fuzzer.SetInputMode( self.data.inputMode )

        if self.data.matcherMode:
            fuzzer.SetMatcherMode( self.data.matcherMode )

        if self.data.filterMode:
            fuzzer.SetFilterMode( self.data.filterMode )

        if self.data.strategy:
            fuzzer.SetAutoCalibrationStrategy( self.data.strategy )

        if self.data.frecursion:
            fuzzer.EnableRecursion()

        if bool( self.data.fdepth ):
            fuzzer.SetRecursionDepth( self.data.fdepth )

        if self.data.fstrategy:
            fuzzer.SetRecursionStrategy( self.data.fstrategy )

        return fuzzer

        