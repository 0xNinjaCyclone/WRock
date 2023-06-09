
import sys
from optparse import *


def register_modules_options(parser):
    modules_options = OptionGroup(parser,"Modules options")
    modules_options.add_option('--burp-collaborator',dest="collaborator",help="Set Collaborator server host to detect blind vulns EX (host.burpcollaborator.net)")
    modules_options.add_option('--sqlmap-format',action="store_true",dest="sqlmap",help="Save output of vulnerable urls with sqlmap format (will be saved in this format page-param.sqlmap)")
    modules_options.add_option('--xsshunter',dest="xsshunter",help="xsshunter url EX (https://hacker.xss.ht)")
    parser.add_option_group(modules_options)

def register_subdomain_options(parser):
    subdomain_options = OptionGroup(parser,"Subdomain collector options")
    subdomain_options.add_option("--sources",dest="sources",help="Enumerations Sources separated by comm (Note add minus before source to exclude)")
    subdomain_options.add_option("--timeout",dest="timeout",help="Time out (default = 30)",type=int,default=30)
    subdomain_options.add_option("--subfinder-apis", dest="subfinder_apis",help="yamlfile or submit in this format -> 'Source1:API1+API2,Source2:API1'")
    subdomain_options.add_option("--subfinder-all",action="store_true",dest="subfinder_all",help="Use all sources")
    subdomain_options.add_option("--maxEnumerationTime",dest="maxEnumerationTime",help="Minutes to wait for enumeration results (default = 10)",type=int,default=10)
    subdomain_options.add_option("--recursive",action="store_true",dest="recursive",help="Collect recursivly")
    subdomain_options.add_option("--sublist3r",action="store_true",dest="sublist3r",help="Use sublist3r")
    subdomain_options.add_option("--revip",action="store_true",dest="revip",help="Reverse IPs all collected subdomains")
    parser.add_option_group(subdomain_options)

def register_crawler_options(parser):
    crawler_options = OptionGroup(parser,"Crawler options")
    crawler_options.add_option("--depth", dest="depth", help="Depth to crawl. (default = 5)", type=int, default=5)
    crawler_options.add_option("--subs",action="store_true",dest="subsInScope",help="Include subdomains in crawling")
    crawler_options.add_option("--insecure",action="store_true",dest="insecure",help="Disable TLS verification")
    crawler_options.add_option("--no-crawl",action="store_true",dest="nocrawl",help="Don't use crawler for scanning or analysis js files (use the main url)")
    crawler_options.add_option("--get-sc",action="store_true",dest="sc",help="Get status code of crawled urls")
    crawler_options.add_option("--no-outofscope",action="store_true",dest="noOutOfScope",help="Exclude out of scope pages")
    parser.add_option_group(crawler_options)

def register_jsanalyzer_options(parser):
    jsanalyzer_options = OptionGroup(parser,"Js Analyzer options")
    jsanalyzer_options.add_option("--by-platform", dest="by_platforms", help="Use specific extractors by comma-sperated platforms EX(Google,GitHub,General)")
    jsanalyzer_options.add_option("--by-key", dest="by_keys", help="Use specific extractors by comma-sperated keys type EX(APIKey,OAuth,JWT)")
    parser.add_option_group(jsanalyzer_options)

def register_advanced(parser):
    register_modules_options(parser)
    register_crawler_options(parser)
    register_subdomain_options(parser)
    register_jsanalyzer_options(parser)

def register():
    parser = OptionParser(f"\n\t\t./{sys.argv[0].split('/')[-1]} [-h or --help] for more options \n")
    parser.add_option('-t','--target',dest="target",help="Enter The Target Url|Domain")
    parser.add_option('-m','--mode',dest="mode",help="mode [r|recon - s|scan - c|crawl - a|jsanalyze] (default mode = scan)",default="scan")
    parser.add_option('-T','--threads',dest="threads",help="Set Number Of Threads (default = 5)", type=int, default=5)
    parser.add_option('-H','--headers',dest="headers",help="Custom headers separated by two semi-colons. E.g. -h \"Cookie: foo=bar;;Referer: http://example.com/\" Or File")
    parser.add_option('-i','--include',dest="included_modules",help="Include specified vulnerabilities for scanning EX 'sqli,ssrf' (Note add minus before source to exclude EX '-xss')")
    parser.add_option('-p','--post-params',dest="post",help="Post params ('p1=v1&p2=v2|param_type')")
    parser.add_option('-f','--format',dest="format",help="Output format ('text' by default)",default="text")
    parser.add_option('-o','--output',dest="output",help="Enter FileName for save output in it")
    parser.add_option('-v','--verbose',action="store_true",dest="verbose",help="Increase verbosity",default=False)
    parser.add_option('-V','--version',action="store_true",dest="version",help="Show version")

    register_advanced(parser)
    opt , _ = parser.parse_args()

    return parser , opt
