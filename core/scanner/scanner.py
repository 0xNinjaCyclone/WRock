
from core.scanner.factory import executorFactory


def scan(config):
    executor = executorFactory(config)
    return executor.Start()