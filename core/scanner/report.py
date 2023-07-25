
from core.config.base import Format
from core.output import *
from core.scanner.result import *


class ScannerReportInText(TxtOutput):

    def __init__(self, fileName):
        TxtOutput.__init__(self, fileName)

    def write(self, results):
        resultsList = [ results ] if isinstance(results, ScanResults) else results

        for results in resultsList:
            self.writeResult(results)
            TxtOutput.write(self, '-' * 50)

    def writeResult(self, results: ScanResults):
        for vulnName in results.GetAllVulnNames():
            for vulnInfo in results.GetResultByVuln(vulnName):
                if vulnInfo.status == Status.Vulnerable or vulnInfo.status == Status.Maybe:
                    TxtOutput.write(self, f"{vulnInfo.vulnName} - {vulnInfo.url}")


class ScannerReportInJson(JsonOutput):

    def __init__(self, fileName):
        JsonOutput.__init__(self, fileName)

    def write(self, results):
        if isinstance(results, ScanResults):
            return JsonOutput.write(self, results.Transform())

        dResult = dict()
        ctr = 1

        for result in results:
            dResult[ str(ctr) ] = result.Transform()
            ctr += 1

        return JsonOutput.write(self, dResult)


class ScannerReport(Report):

    def __init__(self, config: OutputConfig):
        Report.__init__(self, config)

    def _get_report(self):
        fmt = self.config.GetFormat()

        if fmt == Format.Text:
            return ScannerReportInText(self.fileName)

        if fmt == Format.Json:
            return ScannerReportInJson(self.fileName)

        else:
            raise TypeError(f"Invalid report format")
