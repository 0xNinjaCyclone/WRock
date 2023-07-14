
from core.config.fuzzer import FuzzerConfig
from gorock.ffuf import Fuzzer, FuzzerResult


class WebFuzzer( Fuzzer ):


    def __init__(self, config: FuzzerConfig) -> None:
        
        Fuzzer.__init__(
            self,
            config.GetTarget(),
            config.GetHeaders(),
            config.GetWordLists(),
            config.GetThreads(),
            config.IsRecursionEnabled(),
            config.GetRecursionDepth(),
            config.GetTimeout()
        )

        method = config.GetMethod()

        if bool( method ):
            self.SetMethod(method)

        data = config.GetData()

        if bool( data ):
            self.SetData(data)

        cfgfile = config.GetConfigFile()

        if bool( cfgfile ):
            self.SetConfigFile(cfgfile)

        inpmode = config.GetInputMode()

        if bool( inpmode ):
            self.SetInputMode(inpmode)

        cmds = config.GetInputCommands()

        if bool( cmds ):
            self.SetInputCommands(cmds)

        reqfile = config.GetRequestFile()

        if bool( reqfile ):
            self.SetRequestFile(reqfile)

        calibStrategy = config.GetAutoCalibrationStrategy()

        if bool( calibStrategy ):
            self.SetAutoCalibrationStrategy(calibStrategy)

        rStrategy = config.GetRecursionStrategy()

        if bool( rStrategy ):
            self.SetRecursionStrategy(rStrategy)

        reqproto = config.GetRequestProto()

        if bool( reqproto ):
            self.SetRequestProto(reqproto)

        scrapers = config.GetScrapers()

        if bool( scrapers ):
            self.SetScrapers(scrapers)

        mMode = config.GetMatcherMode()

        if bool( mMode ):
            self.SetMatcherMode(mMode)

        # Set All Matchers
        for name, value in config.GetMatchers().items():
            self.AddMatcher(name, value)

        # Set All Filters
        for name, value in config.GetFilters().items():
            self.AddFilter(filter)


    def Start(self) -> FuzzerResult:
        return Fuzzer.Start(self)