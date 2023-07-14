
from core.config.base import Format
from core.output import *


class FuzzerReportInText(TxtOutput):

    def __init__(self, fileName):
        TxtOutput.__init__(self, fileName)

    def write(self, result):
        for item in result:
            TxtOutput.write(self, item.GetUrl())


class FuzzerReport(Report):

    def __init__(self, config: OutputConfig) -> None:
        Report.__init__(self, config)

    def _get_report(self):
        fmt = self.config.GetFormat()

        if fmt == Format.Text:
            return FuzzerReportInText(self.fileName)

        else:
            raise TypeError(f"Invalid report format")