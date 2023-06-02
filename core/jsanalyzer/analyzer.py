# Author    => Abdallah Mohamed
# Date      => 29-5-2023/02:07AM

from core.jsanalyzer.anlysis import *
from core.config.jsanlyzer import JsAnalyzerConfig


def do_analysis(config: JsAnalyzerConfig):
    return Analyzer(config).Start()
    