# WRock
WebRock is a multi web security purposes tool .

## Features
- Web scanning
- Web crawling
- Subdomain enumeration

## Uses modified versions of
- [Sublist3r](https://github.com/aboul3la/Sublist3r)
- [Subfinder](https://github.com/projectdiscovery/subfinder)
- [RockRawler](https://github.com/abdallah-elsharif/RockRawler)

## Installation
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
help menu
```
┌──(user㉿hostname)-[~/path/to/WRock]
└─$ python3 webrock.py -h
Usage: 
		./webrock.py [-h or --help] for more options 


Options:
  -h, --help            show this help message and exit
  -t TARGET, --target=TARGET
                        Enter The Target Url|Domain
  -m MODE, --mode=MODE  mode [r|recon - s|scan - c|crawl] (default mode =
                        scan)
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
  -f FORMAT, --format=FORMAT
                        Output format ('text' by default)
  -o OUTPUT, --output=OUTPUT
                        Enter FileName for save output in it
  -v, --verbose         Increase verbosity
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
    --no-crawl          Don't use crawl to scan

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


```
Perform scanning
```
python3 webrock.py -t http://target.com/
python3 webrock.py -t http://target.com/ -i "-xss" # exclude xss
```

Perform subdomain enumeration
```
python3 webrock.py -t target.com -m recon
python3 webrock.py -t target.com -m r --sublist3r 
```

Perform both (collect subdomains and scan each subdomain)
```
python3 webrock.py -t target.com -m r+s
python3 webrock.py -t target.com -m r+s -o results.txt
```

Perform crawling
```
python3 webrock.py -t http://target.com/ -m crawl
python3 webrock.py -t http://target.com/ -m c --depth 2 --subs -o urls.txt
```