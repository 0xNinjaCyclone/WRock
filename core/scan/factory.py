
from core.scan.executor import *

def executorFactory(config: ScannerConfig):
    return GeneralScanExecutor(config)