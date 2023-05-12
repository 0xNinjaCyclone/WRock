

import sys, inspect
from core.config.enumerator import EnumerationConfig
from core.recon.subenum.reverser.revip import *
from core.recon.subenum.sublist3r.sublist3r import *

class IDomainEnumerator:
    def __init__(self, config: EnumerationConfig) -> None:
        self.config = config
        self.domain = self.config.GetTarget()
        self.__enumerators = self.GetAllEnumerators()
        self.__sources = list()

        self.handleSources()

    def isEnumerator(self, obj):
        pass

    def GetAllEnumerators(self):
        pass

    def SetSources(self, enumerators):
        if isinstance(enumerators, list):
            # Clear sources from its values 
            self.__sources.clear()

            # Check enumerators one by one before push it to the list
            for enumerator in enumerators:
                if self.isEnumerator(enumerator):
                    self.__sources.append(enumerator)

        else:
            raise TypeError("Enumerators must be in a list")

    def GetSources(self):
        return self.__sources

    def GetAllSources(self):
        enumerators = []
        callers_module = sys._getframe(1).f_globals['__name__']
        classes = inspect.getmembers(sys.modules[callers_module], inspect.isclass)
        for _, obj in classes:
            if self.isEnumerator(obj):
                enumerators.append(obj)

        return enumerators

    def handleSources(self):
        sources = self.config.GetSources()
        
        exclude_case = False
        excluded_src = []

        if sources:
            for src in sources:
                if src.startswith('-'):
                    exclude_case = True
                    excluded_src.append(src[1:])


        if exclude_case:
            self.SetSources([src for src in self.GetAllSources() if src not in [self.__enumerators[key] for key in self.__enumerators.keys() if key in excluded_src]])

        elif sources:
            self.SetSources([self.__enumerators[src] for src in sources if src in self.__enumerators.keys()])

        else:
            self.SetSources(self.GetAllSources())


    def Start(self):
        pass
        
    