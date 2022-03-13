
import os
from core.data import rockPATH
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


class ExcludedModules:
    def __init__(self) -> None:
        self.__excluded_modules = []

    def excludeA(self, moduleName):
        # Exclude only one module
        if moduleName not in self.__excluded_modules:
            moduleName += '.py' if not moduleName.endswith('.py') else str()
            self.__excluded_modules.append(moduleName)


    def excludeL(self, modules):
        # Exclude list of modules
        if not isinstance(modules, list):
            raise TypeError("excludeL takes a list")
        
        for module in modules:
            self.excludeA(module)

    def excludeAll(self):
        # Exclude all of modules
        modules = list()
        path = os.path.join(rockPATH(), "modules")
        dirs = os.listdir(path)
        for dir in dirs:
            modules_path = os.path.join(path, dir)
            if os.path.isdir(modules_path):
                files = os.listdir(modules_path)
                for file in files:
                    if file.endswith('.py'):
                        modules.append(file)

        self.excludeL(modules)
        
    def include(self, moduleName):
        # Include one module
        moduleName += '.py' if not moduleName.endswith('.py') else str()
        self.__excluded_modules.remove(moduleName)

    def includeA(self, moduleName):
        # Include one module, with excluding all modules
        self.excludeAll()
        self.include(moduleName)

    def includeL(self, modules):
        # Include list of modules, with excluding all another modules
        if not isinstance(modules, list):
            raise TypeError("includeL takes a list")
        
        self.excludeAll()

        for module in modules:
            self.include(module)

    def excluded(self, moduleName):
        # check if module excluded 
        return moduleName in self.__excluded_modules

    def included(self, moduleName):
        # check if module included
        return not self.excluded(moduleName)
