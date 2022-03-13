
from core.scan.factory import executorFactory


def scan(config):
    executor = executorFactory(config)
    return executor.Start()