
import json
from json2html import json2html
from typing import Type
from core.config.base import OutputConfig


class Report:
    def __init__(self, config: OutputConfig) -> None:
        self.config = config
        self.fileName = self.config.GetFileName()
        self.report = self._get_report()

    def write(self, data):
        self.report.write(data)

    def _get_report(self):
        pass

    def save(self):
        self.report.save()

    def __enter__(self):
        return self

    def __exit__(self, type, value, trace_back):
        self.save()


class ReportWriter:

    def __init__(self, config: OutputConfig) -> None:
        self.__config = config

    def write(self, Report: Type[Report], data) -> None:
        if self.__config.isEnable():
            self.__write__(Report, data)

    def __write__(self, Report: Type[Report], data):
        with Report(self.__config) as report:
            report.write(data)


class Output:

    def __init__(self, fileName) -> None:
        self.data = None
        self.fileName = fileName
        self.file = open(self.fileName, 'w+')

    def write(self, data, newline = True) -> None:
        pass

    def save(self):
        self.file.write(self.data)
        self.file.close()

    def repeated_data(self, data) -> bool:
        pass

    def __enter__(self):
        return self

    def __exit__(self, type, value, trace_back):
        self.save()

        
class TxtOutput(Output):

    def __init__(self, fileName):
        Output.__init__(self, fileName)
        self.data = str()

    def write(self, data, newline = True):
        self.data += data
        if newline : self.data += "\n"

    def repeated_data(self, data):
        return (data in open(self.fileName, 'r').read() or data in self.data)


class JsonOutput(Output):

    def __init__(self, fileName):
        Output.__init__(self, fileName)

    def write(self, data: dict):
        self.data = data

    def save(self):
        json.dump(self.data, self.file)
        self.file.close()
        

class HtmlOutput(Output):

    def __init__(self, fileName):
        Output.__init__(self, fileName)

    def write(self, data):
        self.data = "<!DOCTYPE html>"
        self.data += "<html>"
        self.data += "<body>"
        self.data += json2html.convert(data)
        self.data += "</body>"
        self.data += "</html>"