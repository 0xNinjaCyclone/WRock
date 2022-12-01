
from core.config.base import Format
from core.output import *


def writeCrawlReport(config: OutputConfig, crawler_result):
    if config.isEnable():
        with CrawlerReport(config) as report:
            for endpoint in crawler_result.GetEndPoints():
                report.write(endpoint['url'])


class CrawlerReportInText(TxtOutput):
    
    def __init__(self, fileName):
        TxtOutput.__init__(self, fileName)

    def write(self, domain):
        TxtOutput.write(self, domain)


class CrawlerReport(Report):

    def __init__(self, config: OutputConfig) -> None:
        Report.__init__(self, config)

    def _get_report(self):
        fmt = self.config.GetFormat()

        if fmt == Format.Text:
            return CrawlerReportInText(self.fileName)

        else:
            raise TypeError(f"Invalid report format")