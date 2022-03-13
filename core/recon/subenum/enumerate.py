
from core.utils import GetAddrsFromHosts
from core.recon.subenum.subfinder.finder import Finder
from core.recon.subenum.sublist3r.list3r import List3r
from core.recon.subenum.reverser.reverser import Reverser
from core.config.enumerator import *
from concurrent.futures import ThreadPoolExecutor


def runFind3r(config: FinderConfig):
    return Finder(config).Start()

def runList3r(config: List3rConfig):
   return List3r(config).Start()

def runThreadedRevIP(config, ip):
    config.SetTarget(ip)
    return Reverser(config).Start()

def runRevIP(config: ReverseIPConfig, addrs):
    results = list()
    features = list()

    with ThreadPoolExecutor(max_workers=config.GetThreads()) as e:
        for ip in addrs:
            features.append(e.submit(runThreadedRevIP, config, ip))
        
    # Extract results from features
    for feature in features:
        results.extend(feature.result())

    return results

def runEnumeration(config: EnumeratorConfig):
    results      = list()
    finderconfig = config.GetFinderConfig()
    list3rconfig = config.GetList3rConfig()
    revconfig    = config.GetReverseIPConfig()
    target       = finderconfig.GetTarget()

    results.extend(runFind3r(finderconfig))

    if target not in results:
        results.append(target)

    if list3rconfig:
        list3r_results = runList3r(list3rconfig)

        for subdomain in list3r_results:
            if subdomain not in results:
                results.append(subdomain)

    if revconfig:
        reverseResults = runRevIP(revconfig, GetAddrsFromHosts(results))

        for domain in reverseResults:
            if domain not in results:
                results.append(domain)

    return results