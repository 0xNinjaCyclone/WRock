

from core.config.base import Config


class ModulesOptionsError(Exception):
    def __init__(self, *args: object) -> None:
        Exception.__init__(self, *args)
            

class ModulesOptions:
    def __init__(self) -> None:
        self.__options = {}

        # intialize common 
        self.__options['common'] = {}

        # module name
        self.__key = None

    def register_common(self, optname, optval):
        # Store data which used in more than module
        self.__options['common'][optname] = optval

    def register(self, modname, optname, optval):
        # Store data which used at the module level

        # initialze module_name hash
        if not modname in self.__options:
            self.__options[modname] = {}

        self.__options[modname][optname] = optval

    def setKey(self, keyVal):
        self.__key = keyVal

    def get(self, optname):
        # return option's value whatever its data type

        if not self.__key:
            raise ModulesOptionsError("module name not supplied")

        if optname in self.__options['common']:
            return self.__options['common'][optname]

        if self.__key in self.__options:
            if optname in self.__options[self.__key]:
                return self.__options[self.__key][optname]


class ModuleConfig(Config):
    def __init__(self) -> None:
        self.__modules_options = None
        Config.__init__(self)

    def SetModulesOptions(self, modules_options: ModulesOptions):
        self.__modules_options = modules_options

    def GetModulesOptions(self):
        return self.__modules_options


