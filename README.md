<h1 align="center">WRock</h1>


<p align="center">
  <img src="imgs/logo.png" alt="Logo">
</p>

> WRock is a professional and powerful tool specifically crafted for modern web security. It provides comprehensive capabilities for advanced web scanning, intelligent web crawling, and thorough subdomain enumeration.

## Features

Experience the power and versatility of WRock, a modern web security tool designed to empower your assessments:

* 🔒 **Web Scanning**: Uncover vulnerabilities and enhance security with an advanced scanning capabilities. Identify potential risks and weaknesses in web applications to fortify your defenses.

* 🌐 **Intelligent Web Crawling**: Explore the intricacies of website structures, uncover hidden paths, and gather valuable information. Our intelligent crawling mechanism provides comprehensive visibility into web assets.

* 🌍 **Subdomain Enumeration**: Expand your attack surface by discovering associated domains and services with a modified version of Sublist3r.

* 🔍 **Advanced Analysis**: Utilize the built-in analyzer module to perform comprehensive analysis of JavaScript files, identifying potential vulnerabilities and security issues. Generate detailed reports with the integrated report writer for effective documentation.


## Uses modified versions of
- [Sublist3r](https://github.com/aboul3la/Sublist3r)
- [Subfinder](https://github.com/projectdiscovery/subfinder)
- [RockRawler](https://github.com/abdallah-elsharif/RockRawler)

## Installation

**Get started with WRock by following these steps:**

```
git clone https://github.com/abdallah-elsharif/WRock.git
cd WRock
chmod 755 install.sh
sudo ./install.sh
```

## Example usages
```
┌──(user㉿hostname)-[~/path/to/WRock]
└─$ python3 webrock.py 

                @@@@@@@@@@@@@@@@@@%##%&&&(%#(*/.... . .  ....*(///////(//##(##(*.    ,.. ..../*(
                @@@@@@@@@@@@@@@@@@&(##%&&%/*/..    .*,. ,*(///(//////(/(/((##%%%##*   ..  .. ,,,
                &&@@@@@@@@@@@@@@@&#(%&@@%(%. *.**./##((((//((((((/**,****//(#%&%%###(   .,  . ..
                @&@@@@@@@@@@@@@&&%(#&@@&%,, ..*#.(#(#((((((##*(****///*,,,,,,,/(%&%%%%(.  . *.. 
                @@@@@@@@@@@@&&&&%#(#%&#*#.*. (%/##%#%(#((#/(//*/,.      ...*/#%(*,(%&%%#... ., .
                @@@@@@@@@@@&%%%%%#(%&,#/,,,..#(#%%%(//(*,(/, .        . .*****( /*,*(&&%%**.,,, 
                @@@@@@@@@@@%%%%%#((##.//,., .*%%%(/(#/,.. ,/**...    ,  /   ,///*///*(#&&&&/,*(,
                @@@@@@@@@&%####((((###//....  ###((*.      .*(**. .,.*,,,,*.  .**////(#(%%&&&((,
                ###############((((####*   .* *&(*,      .. /#*,,....... ...,****/(((((#(%%&&#%%
                ###############((((#####(..*, .#*,  ,,      /%(*(/,*****/#(((///.**/**/((##%%%%%
                ###############(((#########*.. (/ * .  , .,,,#%#(%####(*,/((////*/*,,***,,/(%%%%
                #########%####((((#########(.,..#..*,./ .*/(*%%#(/(#%%##%**,.,//*/*,,.. ..*/###%
                ##############((((#######%%%##*.,,**.*.*#%#(.#(/**,/(    .*/((*.,*///*.  .,*/###
                ########%%%###((((#####%%%%%%%##.#(%*(/##%%*#*. ,.... ..,*,*,,.//(**#*,. .,/,//(
                #####%%%&&&%%#((((#####%%%%%%%%%%(%((,*/##(%%#/.. ,,  , .      ..*//(#/*,*,,#/(#
                ####%&&@@@@&%#(((#####%%%%%%%%%%# #(,**,,(##(/((%&%%#/,   (#((   */#,/(((/(#(/(/
                ###%&&&&&&&&%#((((####%%%%%%%%%%## #*,.,..,//&&%(#%/*%*(%#%%%%(,.%%,.,*(%##%///#
                #(##%%%%%%%%##(((((###%%%%%%%%%%%##//...  .((%(%/*. .*,/&%&///(%//(*,/(##/*(/(((
                ((##%%%%%%%##(((((####%%%%%%%%%%%%##(((*,,.%/,/,  .(/(/*/#*/#%,.,.,,*(#%///#((#*
                (###%%%%%####((((####%%%%%%%%%%%%%%####%/%/**,  #(*/****//     .. *, */#(*/%/*#(
                ####%%%%%%%%#(((((###%%%Abdallah%%%###%%*/*/*.##((/**///     .*(##&%%,(#%#/*/##%
                %&&&&&&&&&&&&%((((###%%%&Mohamed%%%###%///,,*/*,***//*.    *(/*/(##((,(*#%**/*#%
                %&&&&&&&&&&&%%((((###%%%%%%%%%%%%%##%&/,*/,.//,..,*,...,((*(/(**//,*//,*,*/.,#(,
                #%%&&%%%%%%%#(//(((##%%%%%%%%%%%%%##&,*,. %@&#*(/  .,#(###(/(((* ,*#*, ,   ,...,
                #%%&&%&%%%%%#///((###%%%%%%%%%%%%%##,**..//&/*,.. %*,*/.,((#(.*,..           ,,,
                #%%%%&&%%%%#(//(#%%%%%%%%%%%%%%%%#(/*,. ((,.     #,,...  ,/,,,.*.          ...,,
                **/(%%##(*****(#%&&&%###(((/////%(*,,/((/,.,..  .*,..../,../,*.  ,/(#%%%   .....
                ,./##%#/..,*/(#%%%%%#/,       #%/**/*/#/**,,,.,/*,..,(*     (((%#(*(*(#.   . .  
                ##%%%%%%#%%%%%%%%%#/,      ((###/((*(#//**,*.*/*.,.*/,/ .#**,,.*#%(,,.    .     
                /////////((((((((*.       *//(###,.*//,*,,*,//.,,,***,,//***..,..,   ..         
                ..,,,,,,,,,,........    .,/(#%/(***/..,*..,**/,,,,**//,,.....#, ,  .*       ...
                ..,,,***//**,*,,......  ..,#%(*%#*/#, /..,,. .,,*/(*,,,,.,,%%(%*,. .(,*,....,...
            

		./webrock.py [-h or --help] for more options 



```
**Help menu**
```
┌──(user㉿hostname)-[~/path/to/WRock]
└─$ python3 webrock.py -h
Usage: 
		./webrock.py [-h or --help] for more options 


Options:
  -h, --help            show this help message and exit
  -t TARGET, --target=TARGET
                        Enter The Target Url|Domain
  -m MODE, --mode=MODE  mode [r|recon - s|scan - c|crawl - a|jsanalyze]
                        (default mode = scan)
  -T THREADS, --threads=THREADS
                        Set Number Of Threads (default = 5)
  -H HEADERS, --headers=HEADERS
                        Custom headers separated by two semi-colons. E.g. -h
                        "Cookie: foo=bar;;Referer: http://example.com/" Or
                        File
  -i INCLUDED_MODULES, --include=INCLUDED_MODULES
                        Include specified vulnerabilities for scanning EX
                        'sqli,ssrf' (Note add minus before source to exclude
                        EX '-xss')
  -p POST, --post-params=POST
                        Post params ('p1=v1&p2=v2|param_type')
  -f FORMAT, --format=FORMAT
                        Output format ('text' by default)
  -o OUTPUT, --output=OUTPUT
                        Enter FileName for save output in it
  -v, --verbose         Increase verbosity
  -l LEVEL, --level=LEVEL
                        verbosity level [1-3]
  -V, --version         Show version

  Modules options:
    --burp-collaborator=COLLABORATOR
                        Set Collaborator server host to detect blind vulns EX
                        (host.burpcollaborator.net)
    --sqlmap-format     Save output of vulnerable urls with sqlmap format
                        (will be saved in this format page-param.sqlmap)
    --xsshunter=XSSHUNTER
                        xsshunter url EX (https://hacker.xss.ht)

  Crawler options:
    --depth=DEPTH       Depth to crawl. (default = 5)
    --subs              Include subdomains in crawling
    --insecure          Disable TLS verification
    --no-crawl          Don't use crawler for scanning or analysis js files
                        (use the main url)
    --get-sc            Get status code of crawled urls
    --no-outofscope     Exclude out of scope pages

  Subdomain collector options:
    --sources=SOURCES   Enumerations Sources separated by comm (Note add minus
                        before source to exclude)
    --timeout=TIMEOUT   Time out (default = 30)
    --subfinder-apis=SUBFINDER_APIS
                        yamlfile or submit in this format ->
                        'Source1:API1+API2,Source2:API1'
    --subfinder-all     Use all sources
    --maxEnumerationTime=MAXENUMERATIONTIME
                        Minutes to wait for enumeration results (default = 10)
    --recursive         Collect recursivly
    --sublist3r         Use sublist3r
    --revip             Reverse IPs all collected subdomains

  Js Analyzer options:
    --by-platform=BY_PLATFORMS
                        Use specific extractors by comma-sperated platforms
                        EX(Google,GitHub,General)
    --by-key=BY_KEYS    Use specific extractors by comma-sperated keys type
                        EX(APIKey,OAuth,JWT)


```
**Perform scanning**
```
python3 webrock.py -t http://target.com/
python3 webrock.py -t http://target.com/ -i "-xss" # exclude xss
```

**Perform subdomain enumeration**
```
python3 webrock.py -t target.com -m recon
python3 webrock.py -t target.com -m r --sublist3r 
```

**Perform both** (collect subdomains and scan each subdomain)
```
python3 webrock.py -t target.com -m r+s
python3 webrock.py -t target.com -m r+s -o results.txt
```

**Perform crawling**
```
python3 webrock.py -t http://target.com/ -m crawl
python3 webrock.py -t http://target.com/ -m c --depth 2 --subs -o urls.txt
```

## Important Notes

* Please Note: WRock is currently under development, and additional features and enhancements will be added in future updates. We appreciate your understanding and patience as we continue to improve and expand the capabilities of the tool.
  
* WRock is intended for educational and security research purposes only. By using this tool, you acknowledge that you are responsible for complying with all applicable laws and regulations. The developers and contributors of WRock assume no liability and are not responsible for any misuse or damage caused by the tool. Use at your own risk.
  
* Contact me for any questions in my [+] email: elsharifabdallah53@gmail.com | facebook account: [+] https://www.facebook.com/abdallah.elsharif07


