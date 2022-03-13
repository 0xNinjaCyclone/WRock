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