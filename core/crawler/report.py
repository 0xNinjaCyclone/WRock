
from core.config.base import Format
from core.output import *


class CrawlerReportInText(TxtOutput):
    
    def __init__(self, fileName):
        TxtOutput.__init__(self, fileName)

    def write(self, crawler_result):
        for endpoint in crawler_result.GetEndPoints():
            TxtOutput.write(self, endpoint['url'])


class CrawlerReportInJson(JsonOutput):
    def __init__(self, fileName):
        JsonOutput.__init__(self, fileName)

    def write(self, crawler_result):
        JsonOutput.write(self, crawler_result.Transform())


class CrawlerReport(Report):

    def __init__(self, config: OutputConfig) -> None:
        Report.__init__(self, config)

    def _get_report(self):
        fmt = self.config.GetFormat()

        if fmt == Format.Text:
            return CrawlerReportInText(self.fileName)

        elif fmt == Format.Json:
            return CrawlerReportInJson(self.fileName)

        else:
            raise TypeError(f"Invalid report format")
            