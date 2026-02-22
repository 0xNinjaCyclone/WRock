
from core.config.base import Format
from core.output import *


class SubdomainEnumeratorReportInText(TxtOutput):
    
    def __init__(self, fileName):
        TxtOutput.__init__(self, fileName)

    def write(self, subdomains):
        for domain in subdomains:
            TxtOutput.write(self, domain)


class SubdomainEnumeratorReportInJson(JsonOutput):

    def __init__(self, fileName):
        JsonOutput.__init__(self, fileName)

    def write(self, subdomains):
        JsonOutput.write(self, subdomains)

class SubdomainEnumeratorReportInHtml(HtmlOutput):

    def __init__(self, fileName):
        HtmlOutput.__init__(self, fileName)


class EnumeratorReport(Report):

    def __init__(self, config: OutputConfig) -> None:
        Report.__init__(self, config)

    def _get_report(self):
        fmt = self.config.GetFormat()

        if fmt == Format.Text:
            return SubdomainEnumeratorReportInText(self.fileName)

        elif fmt== Format.Json:
            return SubdomainEnumeratorReportInJson(self.fileName)
        
        elif fmt == Format.Html:
            return SubdomainEnumeratorReportInHtml(self.fileName)

        else:
            raise TypeError(f"Invalid report format")
            