
from core.scan.result import *
from core.crawler.crawler import CrawlerResult
from ui.cli.view import Color, Print
from core.data import rockVERSION

def displayAppVersion():
    Print.highlight(f"WRock Version is '{rockVERSION()}'", startl="\n")

def displayUsage(usage):
    Print.normal(usage)

def displayError(err):
    Print.fail(f"Error type => {err.__class__.__name__}", startl="\n")
    Print.fail(f"Error msg  => {err}")

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

def printCrawledEndpoints(endpoints, verbose = False):
    Print.highlight("Endpoints :", endl="\n\n", startl="\n")

    for endpoint in endpoints:
        url = endpoint['url']
        
        if url.startswith("http"):
            Print.success(f"{Color.Bold}[{endpoint['m_type'].upper()}][{str(endpoint['status_code'])}]{Color.NC}" + " " * (4 % (len(endpoint['m_type'])) + 1) + url)
        
        else:
            Print.warn(url)

        if verbose and endpoint['params']:
            for param in endpoint['params']:
                Print.normal(f"param name :\t" + param['name'], startl="\t")
                Print.normal(f"param value:\t" + (param['value'] if param['value'] else "'blank'"), startl="\t")
                Print.normal(f"param type :\t" + param['p_type'], startl="\t", endl="\n\n")

    if not endpoints:
        Print.fail("No EndPoints found !!!")

def printCrawledJsFiles(jsFiles):
    Print.highlight("jsFiles :", endl="\n\n", startl="\n")

    for jsFile in jsFiles:
        Print.success(jsFile)

    if not jsFiles:
        Print.fail("No JsFiles found !!!")

def printCrawledEmails(emails):
    Print.highlight("Emails :", endl="\n\n", startl="\n")

    for email in emails:
        Print.success(email)

    if not emails:
        Print.fail("No Emails found !!!")
            
def printCrawledTotals(crawler_result):
    Print.status("Total endpoints       = {}".format(len(crawler_result.GetEndPoints())), startl="\n")
    Print.status("Total jsFiles         = {}".format(len(crawler_result.GetJsFiles())))
    Print.status("Total Emails          = {}".format(len(crawler_result.GetEmails())))

def printCrawlerResult(crawler_result: CrawlerResult, verbose = False):
    printCrawledEndpoints(crawler_result.GetEndPoints(), verbose)
    printCrawledJsFiles(crawler_result.GetJsFiles())
    printCrawledEmails(crawler_result.GetEmails())
    printCrawledTotals(crawler_result)