
from core.config.base import Format
from core.output import *
from core.scan.result import *


def writeResults(report, results: ScanResults):
    for vulnName in results.GetAllVulnNames():
        for vulnInfo in results.GetResultByVuln(vulnName):
            if vulnInfo.status == Status.Vulnerable or vulnInfo.status == Status.Maybe:
                report.write(vulnInfo)

def writeScanReport(output: OutputConfig, results: ScanResults):
    if output.isEnable():
        with ScannerReport(output) as report:
            writeResults(report, results)

def writeListScansReport(output: OutputConfig, resultsList: list):
    if output.isEnable():
        with ScannerReport(output) as report:
            for results in resultsList:
                writeResults(report, results)

class ScannerReportInText(TxtOutput):

    def __init__(self, fileName):
        TxtOutput.__init__(self, fileName)

    def write(self, data: VulnerabilityInfo):
        data = f"{data.vulnName} - {data.url}"
        return TxtOutput.write(self, data)


class ScannerReport(Report):

    def __init__(self, config: OutputConfig):
        Report.__init__(self, config)

    def _get_report(self):
        fmt = self.config.GetFormat()

        if fmt == Format.Text:
            return ScannerReportInText(self.fileName)

        else:
            raise TypeError(f"Invalid report format")
