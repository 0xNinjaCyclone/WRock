
from core.config.base import Format
from core.output import *


class JsAnalyzerReportInText(TxtOutput):
    
    def __init__(self, fileName):
        TxtOutput.__init__(self, fileName)

    def write(self, results):
        line = "*" * 50


        for result in results.GetFilesHaveSensitives():
            TxtOutput.write(self, line)
            TxtOutput.write(self, f"JsLink:  {result.GetJsLink()}")

            for item in result.GetItems():
                TxtOutput.write(self, "") # Empty Line as a seperator between items

                TxtOutput.write(self, f"Platform :  {item.GetPlatform()}")
                TxtOutput.write(self, f"KeyType :  {item.GetKeyType()}")
                TxtOutput.write(self, f"Expression :  {item.GetExpression()}")

                TxtOutput.write(self, "Data :-")
                data = "\n\t->  ".join( item.GetData() )
                TxtOutput.write(self, f"\t-> {data}")
                

            TxtOutput.write(self, line)


class JsAnalyzerReportInJson(JsonOutput):

    def __init__(self, fileName):
        JsonOutput.__init__(self, fileName)

    def write(self, results):
        JsonOutput.write(self, results.Transform())


class JsAnalyzerReport(Report):

    def __init__(self, config: OutputConfig) -> None:
        Report.__init__(self, config)

    def _get_report(self):
        fmt = self.config.GetFormat()

        if fmt == Format.Text:
            return JsAnalyzerReportInText(self.fileName)

        elif fmt == Format.Json:
            return JsAnalyzerReportInJson(self.fileName)

        else:
            raise TypeError(f"Invalid report format")