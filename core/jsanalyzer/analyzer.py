# Author    => Abdallah Mohamed
# Date      => 29-5-2023/02:07AM

from core.jsanalyzer.anlysis import *
from core.jsanalyzer.miner import EndpointsMiner
from core.config.jsanlyzer import JsAnalyzerConfig


def do_analysis(config: JsAnalyzerConfig):
    return Analyzer(config).Start()
    
def mine(config: Config, crawler_result):
    return EndpointsMiner( config, crawler_result ).Start()