
import os.path, threading
from core.fuzzer.report import FuzzerReport
from core.logger import Logger
from ui.cli import builder, view, show
from core.recon.subenum.enumerate import runEnumeration
from core.scanner.result import ScanResults
from core.config.base import Mode
from core.scanner.scanner import scan
from core.crawler.crawl import crawl
from core.jsanalyzer.analyzer import do_analysis
from core.fuzzer.fuzzer import fuzz
from core.crawler.report import CrawlerReport
from core.scanner.report import ScannerReport
from core.recon.subenum.report import EnumeratorReport
from core.jsanalyzer.report import JsAnalyzerReport
from core.output import Report, ReportWriter, Type


def startScan(scanner_cfg):
    results = scan(scanner_cfg)
    show.printScanResults(results, scanner_cfg.GetVerbosity().IsEnabled())
    return results

def startEnumeration(enum_cfg):
    subdomains = runEnumeration(enum_cfg)
    show.printSubdomains(subdomains)
    return subdomains

def startCrawling(crawl_cfg):
    crawler_result = crawl(crawl_cfg)
    show.printCrawlerResult(crawler_result, crawl_cfg.GetVerbosity().IsEnabled())
    return crawler_result

def startJsAnalysis(jsanalyzer_cfg):
    results = do_analysis(jsanalyzer_cfg)
    show.printJsAnalyzerResults(results, jsanalyzer_cfg.GetVerbosity().IsEnabled())
    return results

def startFuzzing(fuzzer_cfg):
    result = fuzz(fuzzer_cfg)
    show.printFuzzerResult(result, fuzzer_cfg.GetVerbosity().IsEnabled())
    return result

def writeReport(output, results, Report: Type[Report]):
    if output:
        ReportWriter( output ).write( Report, results )
        view.Print.status(f"Output has been saved at '{output.GetFileName()}'")

def run(opts):
    config = builder.OptionsBuilder(opts).buildRock()
    output = config.GetOutputConfig()
    mode   = config.GetMode()
    rock_t = view.RockTime()
    logger = Logger()
    threading.Thread(target=show.handleLogger, args=( config.GetVerbosity(), ), daemon=True).start()


    if mode == Mode.Scan:
        results = startScan(config.GetScannerConfig())
        writeReport(output, results, ScannerReport)
        rock_t.finish("scan")

    elif mode == Mode.Recon:
        subdomains = startEnumeration(config.GetEnumeratorConfig())
        writeReport(output, subdomains, EnumeratorReport)
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
        show.printScanResults(results, scanner_config.GetVerbosity().IsEnabled())

        if output:
            view.Print.highlight("Write reports :", startl="\n")
            reportName  = output.GetFileName()

            # Save subdomains 
            output_path , fileName = os.path.split(reportName)
            output.SetFileName(os.path.join(output_path, f"subdomains-{fileName}"))
            writeReport(output, subdomains, EnumeratorReport)

            # Return fileName again after changing when wrote subdomains report
            output.SetFileName(reportName)

            # Write all results in a report 
            writeReport(output, results, ScannerReport)


        rock_t.finish("recon and scan")

    elif mode == Mode.Crawl:
        crawler_result = startCrawling(config.GetCrawlerConfig())
        writeReport(output, crawler_result, CrawlerReport)
        rock_t.finish("crawl")

    elif mode == Mode.JsAnalyze:
        results = startJsAnalysis(config.GetJsAnalyzerConfig())
        writeReport(output, results, JsAnalyzerReport)
        rock_t.finish("js analysis")

    elif mode == Mode.Fuzz:
        result = startFuzzing(config.GetFuzzerConfig())
        writeReport(output, result, FuzzerReport)
        rock_t.finish("fuzz")

    else:
        view.Print.fail("This mode is not supported !!")

    logger.join()