
import os
from core.data import rockPATH


class Excluder:
    
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
        files = os.listdir(path)
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
