

from core.fuzzer.fuzz import WebFuzzer


def fuzz(config):
    return WebFuzzer(config).Start()