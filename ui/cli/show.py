
from urllib.parse import urlencode
from core.logger import *
from core.scanner.result import *
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

def printModuleInfo(modInfo):
    vulnInfo = modInfo.GetVulnInfo()   
    vulnName = vulnInfo.vulnName

    if vulnInfo.status == Status.Vulnerable:
        Print.success(f"{vulnName} Detected")

    elif vulnInfo.status == Status.Maybe:
        Print.warn(f"{vulnName} Maybe Vulnerable")

    else:
        return

    Print.success(f"[Method: {vulnInfo.endpoint.GetMethodType()}, Url: {vulnInfo.endpoint.GetFullUrl()}]")
    
    if vulnInfo.endpoint.GetMethodType() == 'POST' and vulnInfo.endpoint.GetData():
        Print.success(f"[POST Params: {urlencode(vulnInfo.endpoint.GetData())}]")

    v = ""

    for i in vulnInfo.vulnerables:
        for key , val in i.items():
            if key and val:
                v += f"{key}:{val}, "
    
    v = v[:-2]
    Print.success(f"[VulnInfo = {v}]")

def printExtraInfo(modInfo):
    Print.highlight(f"Authors: {', '.join(modInfo.GetAuthors())}", startl=" "*4)
    Print.highlight(f"Description: {modInfo.GetDescription()}", startl=" "*4)

    risk = "Unknown"

    if modInfo.GetRisk() == Risk.Critical:
        risk = "Critical"
    elif modInfo.GetRisk() == Risk.High:
        risk = "High"
    elif modInfo.GetRisk() == Risk.Medium:
        risk = "Medium"
    elif modInfo.GetRisk() == Risk.Low:
        risk = "Low"

    Print.highlight(f"Risk: {risk}", startl=" "*4)

    ref = modInfo.GetReferances()
    if ref:
        Print.highlight("Refrences:", startl=" "*4, endl="\n\t")
        Print.normal("\n\t".join(ref))

def printScanResults(results: ScanResults, verbose = False):
    Print.highlight("Scanner Results :", endl="\n\n")

    for vulnName in results.GetAllVulnNames():
        for modInfo in results.GetResultByVuln(vulnName):
            printModuleInfo(modInfo)

            if modInfo.GetVulnInfo().status == Status.NotVulnerable:
                continue
            
            if verbose:
                printExtraInfo(modInfo)

            Print.normal() # new line                


def printJsAnalyzerResults(results, verbose = False):
    Print.highlight("Js sensitive data :", endl="\n\n", startl="\n")

    for result in results.GetFilesHaveSensitives():
        Print.success(f"Js Link -> {result.GetJsLink()}")

        for item in result.GetItems():
            extractor = item.GetExtractor()
            data = ', '.join( item.GetData() )

            Print.success(f"Data => {data} - Platform => {extractor.GetPlatform()} - Key type => {extractor.GetKeyType()} - Regex => {extractor.GetExpression()}")

    else:
        Print.fail("No sensitive data found !!!")

    Print.highlight("All JsFiles :", verbose=verbose, endl="\n\n", startl="\n")
    
    for result in results:
        Print.success(result.GetJsLink(), verbose=verbose)

    Print.status("Total processed js files = {}".format( results.GetNumberOfJsLinks() ), startl="\n")
    Print.status("Number of files that have sensitives = {}".format( results.GetNumberOfFilesHaveSensitives() ))
    Print.status("Number of sensitives = {}".format( results.GetNumberOfSensitives() ))

def printFuzzerResult(result, verbose = False):

    if not result:
        Print.fail("There are no results")
        return

    # Get largest words length
    largest = 0
    for item in result:
        words = item.GetFuzzingWords()

        # Get string summation of fuzzing words + 2 for each word for ', '
        length = sum(len(i) for i in words) + ( 2 * len(words) )

        if length > largest:
            largest = length

    spaces = ' ' * ( largest - len("Words") - 4 )

    Print.highlight(f"    Duration            Status   Size    Words{spaces}    Url ")

    for item in result:
        durationStr = item.GetTimeDuration().GetStr()
        spaces1 = ' ' * ( 12 - len(durationStr) ) 
        length = item.GetContentLength()
        spaces2 = ' ' * ( 8 - len(str(length)) )
        words = ', '.join( item.GetFuzzingWords() )
        spaces3 = ' ' * ( largest - len(words) )
        Print.success(f"[{durationStr}]{spaces1}\t{item.GetStatusCode()}\t {str(length)}{spaces2}{words}{spaces3}{item.GetUrl()}")

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
            status_code = f"[{str(endpoint['status_code'])}]" if endpoint['status_code'] != 0 else str()
            scope = "[InScope]" if endpoint['in_scope'] else "[OutScope]"
            colored_scope = f"{Color.NC}{Color.Green}{scope}" if endpoint['in_scope'] else f"{Color.NC}{Color.Red}{scope}"
            Print.success(f"{Color.Bold}[{endpoint['m_type'].upper()}]{status_code}{colored_scope}{Color.NC}" + " " * ((4 + 10) % (len(endpoint['m_type']) + len(scope)) + 1) + url)
        
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

def handleLogger(verbosity):
    # Under dev ( need more improvement )
    
    logger = Logger()
    v_level = verbosity.GetLevel()

    while True:
        record = logger.get()
        l_level = record.GetLevel()


        if l_level == Level.CRITICAL:
            printRecord( record )

        elif l_level == Level.INFO and v_level in ( Level.INFO, Level.DEBUG ):
            printRecord( record )

        elif l_level == Level.DEBUG and v_level == Level.DEBUG:
            printRecord( record )


        logger.task_done()

def printRecord(record: Record):
    msgtype = record.GetType()

    if msgtype == MessageType.SUCCESS:
        Print.success( record.GetMessage() )

    elif msgtype == MessageType.STATUS:
        Print.status( record.GetMessage() )

    elif msgtype == MessageType.WARN:
        Print.warn( record.GetMessage() )

    elif msgtype == MessageType.ERROR:
        Print.fail( record.GetMessage() )