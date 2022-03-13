
from core.scan.result import *
from ui.cli.view import Print

def printScanResults(results: ScanResults, verbose = False):
    Print.highlight("Results :")

    for vulnName in results.GetAllVulnNames():
        Print.status(f"{vulnName} results :", startl="\n")
        
        for vulnInfo in results.GetResultByVuln(vulnName):
            if vulnInfo.status == Status.Vulnerable:
                Print.success(vulnInfo.url)

            elif vulnInfo.status == Status.Maybe:
                Print.warn(vulnInfo.url)

            else:
                Print.fail(vulnInfo.url, verbose = verbose)


def printSubdomains(subdomains):
    Print.highlight("Subdomains :", endl="\n\n")

    for subdomain in subdomains:
        Print.success(subdomain)

    Print.status("Total subdomains = {}".format(len(subdomains)), startl="\n")


def printCrawledUrls(urls):
    Print.highlight("Urls :", endl="\n\n")

    for url in urls:
        if url.startswith("http"):
            Print.success(url)
        else:
            Print.warn(url)

    Print.status("Total urls = {}".format(len(urls)), startl="\n")