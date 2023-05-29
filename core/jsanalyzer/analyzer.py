# Author    => Abdallah Mohamed
# Date      => 29-5-2023/02:07AM

from core.jsanalyzer.anlysis import *


def do_analysis(jsLinks, threads):
    extLdr = ExtractorsLoader()
    extLdr.Load()
    return Analyzer(extLdr.GetAll(), jsLinks, threads).Start()