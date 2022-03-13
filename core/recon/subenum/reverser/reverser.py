
from core.recon.subenum.reverser.revip import *
from core.recon.subenum.enumerator import *


class Reverser(IDomainEnumerator):

    def __init__(self, config: ReverseIPBase) -> None:
        IDomainEnumerator.__init__(self, config)

    def isEnumerator(self, obj):
        return obj is not ReverseIPBase and (ReverseIPBase in inspect.getmro(obj))

    def GetAllEnumerators(self):
        return {
            'sonarsearch': Sonar
        }

    def Start(self):
        results = []

        for src in self.GetSources():
            domains = src(self.config).enumerate()

            for domain in domains:
                if domain not in results:
                    results.append(domain)


        return results