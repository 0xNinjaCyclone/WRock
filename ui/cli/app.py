
import os.path
from ui.cli import builder, view, show
from core.recon.subenum.enumerate import runEnumeration
from core.scan.result import ScanResults
from core.config.base import Mode
from core.scan.scanner import scan
from core.crawler.crawl import crawl
from core.jsanalyzer.analyzer import do_analysis
from core.crawler.report import writeCrawlReport
from core.scan.report import writeScanReport, writeListScansReport
from core.recon.subenum.report import writeEnumReport


def startScan(scanner_cfg):
    results = scan(scanner_cfg)
    show.printScanResults(results, scanner_cfg.isVerboseEnabled())
    return results

def startEnumeration(enum_cfg):
    subdomains = runEnumeration(enum_cfg)
    show.printSubdomains(subdomains)
    return subdomains

def startCrawling(crawl_cfg):
    crawler_result = crawl(crawl_cfg)
    show.printCrawlerResult(crawler_result, crawl_cfg.isVerboseEnabled())
    return crawler_result

def startJsAnalysis(jsLinks, threads):
    results = do_analysis(jsLinks, threads)
    show.printJsAnalyzerResults(results)
    return results

def writeReport(output, results, reportWriter):
    if output:
        reportWriter(output, results)
        view.Print.status(f"Output has been saved at '{output.GetFileName()}'")

def run(opts):
    config = builder.OptionsBuilder(opts).buildRock()
    output = config.GetOutputConfig()
    mode   = config.GetMode()
    rock_t = view.RockTime()

    if mode == Mode.Scan:
        results = startScan(config.GetScannerConfig())
        writeReport(output, results, writeScanReport)
        rock_t.finish("scan")

    elif mode == Mode.Recon:
        subdomains = startEnumeration(config.GetEnumeratorConfig())
        writeReport(output, subdomains, writeEnumReport)
        rock_t.finish("recon")

    elif mode == Mode.Both:
        view.Print.status("Start Enumeration :")
        enum_config = config.GetEnumeratorConfig()
        subdomains  = runEnumeration(enum_config)
        view.Print.status(f"Total results = {len(subdomains)}")

        view.Print.status("Start Scanning :", startl="\n", endl="\n\n")
        results = ScanResults()
        scanner_config = config.GetScannerConfig()

        for domain in subdomains:
            scanner_config.SetTarget(domain)

            try:
                results += scan(scanner_config)
            except:
                continue


        # Display results
        show.printScanResults(results, scanner_config.isVerboseEnabled())

        if output:
            view.Print.highlight("Write reports :", startl="\n")
            reportName  = output.GetFileName()

            # Save subdomains 
            output_path , fileName = os.path.split(reportName)
            output.SetFileName(os.path.join(output_path, f"subdomains-{fileName}"))
            writeReport(output, subdomains, writeEnumReport)

            # Return fileName again after changing when wrote subdomains report
            output.SetFileName(reportName)

            # Write all results in a report 
            writeReport(output, results, writeListScansReport)


        rock_t.finish("recon and scan")

    elif mode == Mode.Crawl:
        cralwer_config = config.GetCrawlerConfig()
        crawler_result = startCrawling(cralwer_config)

        if cralwer_config.isJsAnalyzerEnabled():
            startJsAnalysis(crawler_result.GetJsFiles(), cralwer_config.GetThreads())

        show.printCrawledTotals(crawler_result)
        writeReport(output, crawler_result, writeCrawlReport)
        rock_t.finish("crawl")

    else:
        view.Print.fail("This mode is not supported !!")
