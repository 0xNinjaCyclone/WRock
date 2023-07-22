
from core.scanner.executor import *

def executorFactory(config: ScannerConfig):
    return GeneralScanExecutor(config)