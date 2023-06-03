
from core.config.base import Format
from core.output import *


class SubdomainEnumeratorReportInText(TxtOutput):
    
    def __init__(self, fileName):
        TxtOutput.__init__(self, fileName)

    def write(self, subdomains):
        for domain in subdomains:
            TxtOutput.write(self, domain)


class EnumeratorReport(Report):

    def __init__(self, config: OutputConfig) -> None:
        Report.__init__(self, config)

    def _get_report(self):
        fmt = self.config.GetFormat()

        if fmt == Format.Text:
            return SubdomainEnumeratorReportInText(self.fileName)

        else:
            raise TypeError(f"Invalid report format")