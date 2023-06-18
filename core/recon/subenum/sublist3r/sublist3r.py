#!/usr/bin/env python
# coding: utf-8
# Sublist3r v1.0
# By Ahmed Aboul-Ela - twitter.com/aboul3la - Abdallah Mohamed - 19-1-2022


# Resources
# https://lazyhacker.medium.com/subdomain-enumeration-tec-276da39d7e69
# https://0xffsec.com/handbook/information-gathering/subdomain-enumeration/

# modules in standard library
import re
import sys
import time
import hashlib
import random
import json
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from core.config.enumerator import List3rConfig

# external modules
import dns.resolver
import requests

# Python 2.x and 3.x compatiablity
if sys.version > '3':
    import urllib.parse as urlparse
    import urllib.parse as urllib
else:
    import urlparse
    import urllib

# In case you cannot install some of the required development packages
# there's also an option to disable the SSL warning:
try:
    import requests.packages.urllib3
    requests.packages.urllib3.disable_warnings()
except:
    pass


def subdomain_sorting_key(hostname):
    """Sorting key for subdomains

    This sorting key orders subdomains from the top-level domain at the right
    reading left, then moving '^' and 'www' to the top of their group. For
    example, the following list is sorted correctly:

    [
        'example.com',
        'www.example.com',
        'a.example.com',
        'www.a.example.com',
        'b.a.example.com',
        'b.example.com',
        'example.net',
        'www.example.net',
        'a.example.net',
    ]

    """
    parts = hostname.split('.')[::-1]
    if parts[-1] == 'www':
        return parts[:-1], 1
    return parts, 0


class enumratorBase(object):
    def __init__(self, config: List3rConfig):
        self.domain = config.GetTarget()
        self.session = requests.Session()
        self.subdomains = []
        self.threads = config.GetThreads()
        self.timeout = config.GetTimeout()
        self.recursive = config.isRecursiveEnabled()
        self.headers = config.GetHeaders()

    def get_response(self, response):
        if response is None:
            return 0

        return response.text if hasattr(response, "text") else response.content.decode("utf-8")

    # override
    def extract_domains(self, resp):
        """ chlid class should override this function """
        pass

    def get_url(self, domain):
        """ chlid class should override this function """
        pass

    def enumerate(self):
        """ chlid class should override this function """
        pass

    
class SearchEngineEnumerator(enumratorBase):

    def __init__(self, config):
        enumratorBase.__init__(self, config)

    def send_req(self, query, page_no=1):

        url = self.get_url(query, page_no)

        try:
            resp = self.session.get(url, headers=self.headers, timeout=self.timeout)
        except Exception:
            resp = None

        return self.get_response(resp)


    def check_max_subdomains(self, count):
        if self.MAX_DOMAINS == 0:
            return False

        return count >= self.MAX_DOMAINS

    def check_max_pages(self, num):
        if self.MAX_PAGES == 0:
            return False

        return num >= self.MAX_PAGES

    # override
    def check_response_errors(self, resp):
        """ chlid class should override this function
        The function should return True if there are no errors and False otherwise
        """
        return True

    def should_sleep(self):
        """Some enumrators require sleeping to avoid bot detections like Google enumerator"""
        pass

    def generate_query(self):
        """ chlid class should override this function """
        pass

    def get_page(self, num):
        """ chlid class that user different pagnation counter should override this function """
        return num + 10

    def get_url(self, query, page_no = 1):
        """ chlid class should override this function """
        pass

    def enumerate(self):
        flag = True
        page_no = 0
        prev_links = []
        retries = 0

        while flag:
            query = self.generate_query()
            count = query.count(self.domain)  # finding the number of subdomains found so far

            # if they we reached the maximum number of subdomains in search query
            # then we should go over the pages
            if self.check_max_subdomains(count):
                page_no = self.get_page(page_no)

            if self.check_max_pages(page_no):  # maximum pages for Google to avoid getting blocked
                return self.subdomains
            resp = self.send_req(query, page_no)

            # check if there is any error occured
            if not self.check_response_errors(resp):
                return self.subdomains
            links = self.extract_domains(resp)

            # if the previous page hyperlinks was the similar to the current one, then maybe we have reached the last page
            if links == prev_links:
                retries += 1
                page_no = self.get_page(page_no)

        # make another retry maybe it isn't the last page
                if retries >= 3:
                    return self.subdomains

            prev_links = links
            self.should_sleep()

        return self.subdomains



class GoogleEnum(SearchEngineEnumerator):
    def __init__(self, config):
        self.MAX_DOMAINS = 11
        self.MAX_PAGES = 200
        SearchEngineEnumerator.__init__(self, config)

    def get_url(self, query, page_no = 1):
        return "https://google.com/search?q={query}&btnG=Search&hl=en-US&biw=&bih=&gbv=1&start={page_no}&filter=0".format(query=query, page_no=page_no)


    def extract_domains(self, resp):
        links_list = list()
        link_regx = re.compile('<cite.*?>(.*?)<\/cite>')
        try:
            links_list = link_regx.findall(resp)
            for link in links_list:
                link = re.sub('<span.*>', '', link)
                if not link.startswith('http'):
                    link = "http://" + link
                subdomain = urlparse.urlparse(link).netloc
                if subdomain and subdomain not in self.subdomains and subdomain != self.domain:
                    self.subdomains.append(subdomain.strip())
        except Exception:
            pass

        return links_list

    def check_response_errors(self, resp):
        if type(resp) is not str and 'Our systems have detected unusual traffic' in resp:
            return False
        
        return True

    def should_sleep(self):
        time.sleep(5)

    def generate_query(self):
        if self.subdomains:
            fmt = 'site:{domain} -www.{domain} -{found}'
            found = ' -'.join(self.subdomains[:self.MAX_DOMAINS - 2])
            query = fmt.format(domain=self.domain, found=found)
        else:
            query = "site:{domain} -www.{domain}".format(domain=self.domain)

        return query


class YahooEnum(SearchEngineEnumerator):
    def __init__(self, config):
        self.MAX_DOMAINS = 10
        self.MAX_PAGES = 0
        SearchEngineEnumerator.__init__(self, config)

    def get_url(self, query, page_no=1):
        return "https://search.yahoo.com/search?p={query}&b={page_no}".format(query=query, page_no=page_no)

    def extract_domains(self, resp):
        link_regx2 = re.compile('<span class=" fz-.*? fw-m fc-12th wr-bw.*?">(.*?)</span>')
        link_regx = re.compile('<span class="txt"><span class=" cite fw-xl fz-15px">(.*?)</span>')
        links_list = []

        try:
            links = link_regx.findall(resp)
            links2 = link_regx2.findall(resp)
            links_list = links + links2

            for link in links_list:
                link = re.sub("<(\/)?b>", "", link)
                if not link.startswith('http'):
                    link = "http://" + link

                subdomain = urlparse.urlparse(link).netloc
                if not subdomain.endswith(self.domain):
                    continue

                if subdomain and subdomain not in self.subdomains and subdomain != self.domain:
                    self.subdomains.append(subdomain.strip())
        except Exception:
            pass

        return links_list

    def should_sleep(self):
        return

    def get_page(self, num):
        return num + 10

    def generate_query(self):
        if self.subdomains:
            fmt = 'site:{domain} -domain:www.{domain} -domain:{found}'
            found = ' -domain:'.join(self.subdomains[:77])
            query = fmt.format(domain=self.domain, found=found)
        else:
            query = "site:{domain}".format(domain=self.domain)

        return query


class AskEnum(SearchEngineEnumerator):
    def __init__(self, config):
        self.MAX_DOMAINS = 11
        self.MAX_PAGES = 0
        SearchEngineEnumerator.__init__(self, config)

    def get_url(self, query, page_no=1):
        return "http://www.ask.com/web?q={query}&page={page_no}&qid=8D6EE6BF52E0C04527E51F64F22C4534&o=0&l=dir&qsrc=998&qo=pagination".format(query=query, page_no=page_no)

    def extract_domains(self, resp):
        links_list = list()
        link_regx = re.compile('<p class="web-result-url">(.*?)</p>')
        try:
            links_list = link_regx.findall(resp)
            for link in links_list:
                if not link.startswith('http'):
                    link = "http://" + link
                subdomain = urlparse.urlparse(link).netloc
                if subdomain not in self.subdomains and subdomain != self.domain:
                    self.subdomains.append(subdomain.strip())
        except Exception:
            pass

        return links_list

    def get_page(self, num):
        return num + 1

    def generate_query(self):
        if self.subdomains:
            fmt = 'site:{domain} -www.{domain} -{found}'
            found = ' -'.join(self.subdomains[:self.MAX_DOMAINS])
            query = fmt.format(domain=self.domain, found=found)
        else:
            query = "site:{domain} -www.{domain}".format(domain=self.domain)

        return query


class BingEnum(SearchEngineEnumerator):
    def __init__(self, config):
        self.MAX_DOMAINS = 30
        self.MAX_PAGES = 0
        SearchEngineEnumerator.__init__(self, config)

    def get_url(self, query, page_no=1):
        return "https://www.bing.com/search?q={query}&go=Submit&first={page_no}".format(query=query, page_no=page_no)

    def extract_domains(self, resp):
        links_list = list()
        link_regx = re.compile('<li class="b_algo"><h2><a href="(.*?)"')
        link_regx2 = re.compile('<div class="b_title"><h2><a href="(.*?)"')
        try:
            links = link_regx.findall(resp)
            links2 = link_regx2.findall(resp)
            links_list = links + links2

            for link in links_list:
                link = re.sub('<(\/)?strong>|<span.*?>|<|>', '', link)
                if not link.startswith('http'):
                    link = "http://" + link
                subdomain = urlparse.urlparse(link).netloc
                if subdomain not in self.subdomains and subdomain != self.domain:
                    self.subdomains.append(subdomain.strip())
        except Exception:
            pass

        return links_list

    def generate_query(self):
        if self.subdomains:
            fmt = 'domain:{domain} -www.{domain} -{found}'
            found = ' -'.join(self.subdomains[:self.MAX_DOMAINS])
            query = fmt.format(domain=self.domain, found=found)
        else:
            query = "domain:{domain} -www.{domain}".format(domain=self.domain)
        return query


class BaiduEnum(SearchEngineEnumerator):
    def __init__(self, config):
        self.MAX_DOMAINS = 2
        self.MAX_PAGES = 760
        SearchEngineEnumerator.__init__(self, config)
        self.querydomain = self.domain

    def get_url(self, query, page_no=1):
        return "https://www.baidu.com/s?pn={page_no}&wd={query}&oq={query}".format(query=query, page_no=page_no)

    def extract_domains(self, resp):
        links = list()
        found_newdomain = False
        subdomain_list = []
        link_regx = re.compile('<a.*?class="c-showurl".*?>(.*?)</a>')
        try:
            links = link_regx.findall(resp)
            for link in links:
                link = re.sub('<.*?>|>|<|&nbsp;', '', link)
                if not link.startswith('http'):
                    link = "http://" + link
                subdomain = urlparse.urlparse(link).netloc
                if subdomain.endswith(self.domain):
                    subdomain_list.append(subdomain)
                    if subdomain not in self.subdomains and subdomain != self.domain:
                        found_newdomain = True
                        self.subdomains.append(subdomain.strip())
        except Exception:
            pass
        if not found_newdomain and subdomain_list:
            self.querydomain = self.findsubs(subdomain_list)
        return links

    def findsubs(self, subdomains):
        count = Counter(subdomains)
        subdomain1 = max(count, key=count.get)
        count.pop(subdomain1, "None")
        subdomain2 = max(count, key=count.get) if count else ''
        return (subdomain1, subdomain2)

    def check_response_errors(self, resp):
        return True

    def should_sleep(self):
        time.sleep(random.randint(2, 5))

    def generate_query(self):
        if self.subdomains and self.querydomain != self.domain:
            found = ' -site:'.join(self.querydomain)
            query = "site:{domain} -site:www.{domain} -site:{found} ".format(domain=self.domain, found=found)
        else:
            query = "site:{domain} -site:www.{domain}".format(domain=self.domain)
        return query


class NetcraftEnum(enumratorBase):
    def __init__(self, config):
        enumratorBase.__init__(self, config)

    def get_url(self, domain):
        return f"https://searchdns.netcraft.com/?restriction=site+ends+with&host={domain}"

    def req(self, url, cookies=None):
        cookies = cookies or {}
        try:
            resp = self.session.get(url, headers=self.headers, timeout=self.timeout, cookies=cookies)
        except:
            resp = None

        return resp

    def should_sleep(self):
        time.sleep(random.randint(1, 2))
        return

    def get_next(self, resp):
        link_regx = re.compile('<a.*?href="(.*?)">Next Page')
        link = link_regx.findall(resp)
        url = 'http://searchdns.netcraft.com' + link[0]
        return url

    def create_cookies(self, cookie):
        cookies = dict()
        cookies_list = cookie[0:cookie.find(';')].split("=")
        cookies[cookies_list[0]] = cookies_list[1]
        # hashlib.sha1 requires utf-8 encoded str
        cookies['netcraft_js_verification_response'] = hashlib.sha1(urllib.unquote(cookies_list[1]).encode('utf-8')).hexdigest()
        return cookies

    def get_cookies(self, headers):
        if 'set-cookie' in headers:
            cookies = self.create_cookies(headers['set-cookie'])
        else:
            cookies = {}
        return cookies

    def enumerate(self):
        start_url = self.get_url('example.com')
        resp = self.req(start_url)
        cookies = self.get_cookies(resp.headers)
        url = self.get_url(self.domain)

        while True:
            resp = self.get_response(self.req(url, cookies))
            self.extract_domains(resp)
            if 'Next Page' not in resp:
                return self.subdomains

            url = self.get_next(resp)
            self.should_sleep()

    def extract_domains(self, resp):
        #print(resp)
        links_list = list()
        link_regx = re.compile('<a class="results-table__host" href="(.*?)"')
        try:
            links_list = link_regx.findall(resp)
            for link in links_list:
                subdomain = urlparse.urlparse(link).netloc
                if not subdomain.endswith(self.domain):
                    continue
                if subdomain and subdomain not in self.subdomains and subdomain != self.domain:
                    self.subdomains.append(subdomain.strip())
        except Exception:
            pass
        return links_list


class DNSdumpster(enumratorBase):
    def __init__(self, config):
        self.base_url = 'https://dnsdumpster.com/'
        self.live_subdomains = []
        self.lock = None
        enumratorBase.__init__(self, config)

    def check_host(self, host):
        is_valid = False
        Resolver = dns.resolver.Resolver()
        Resolver.nameservers = ['8.8.8.8', '8.8.4.4']
        try:
            ip = Resolver.query(host, 'A')[0].to_text()
            if ip:
                is_valid = True
                self.live_subdomains.append(host)
        except:
            pass
        
        return is_valid

    def check_hosts(self):
        # for subdomain in self.subdomains
        with ThreadPoolExecutor(max_workers=self.threads) as e:
            [e.submit(self.check_host, subdomain) for subdomain in self.subdomains]

    def req(self, req_method, url, params=None):
        params = params or {}
        headers = dict(self.headers)
        headers['Referer'] = self.base_url 
        try:
            if req_method == 'GET':
                resp = self.session.get(url, headers=headers, timeout=self.timeout)
            else:
                resp = self.session.post(url, data=params, headers=headers, timeout=self.timeout)
        except Exception as e:
            resp = None

        return self.get_response(resp)


    def dnsdumpester_enum(self, domain):
        resp = self.req('GET', self.base_url)
        soup = BeautifulSoup(resp, 'html.parser')
        csrf_middleware = soup.findAll('input', attrs={'name': 'csrfmiddlewaretoken'})[0]['value']

        cookies = {'csrftoken': csrf_middleware}
        headers = {'Referer': self.base_url, 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}
        data = {'csrfmiddlewaretoken': csrf_middleware, 'targetip': domain, 'user': 'free'}
        resp = requests.post(self.base_url, cookies=cookies, data=data, headers=headers).text

        # Extract subdomains from response
        self.extract_domains(resp)
        
    def enumerate(self):

        # Main enum 
        self.dnsdumpester_enum(self.domain)

        # Check live subdomains
        self.check_hosts()
        
        # Recursive search
        if self.recursive:
            for subdomain in self.live_subdomains:
                self.dnsdumpester_enum(subdomain)
    

        return self.live_subdomains

    def extract_domains(self, resp):
        # Useful resource => https://github.com/PaulSec/API-dnsdumpster.com
        
        soup = BeautifulSoup(resp, 'html.parser')
        tables = soup.findAll('table')

        # Store data in subdomains container
        # Host Records (A) in table 3 on the site

        if tables and len(tables) > 3:
            for entry in self.retrieve_results(tables[3]):
                subdomain = entry['domain']

                if subdomain not in self.subdomains and subdomain != self.domain:
                    self.subdomains.append(subdomain)

    def retrieve_results(self, table):
        res = []
        trs = table.findAll('tr')
        for tr in trs:
            tds = tr.findAll('td')
            pattern_ip = r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})'
            try:
                ip = re.findall(pattern_ip, tds[1].text)[0]
                domain = str(tds[0]).split('<br/>')[0].split('>')[1].split('<')[0]
                header = ' '.join(tds[0].text.replace('\n', '').split(' ')[1:])
                reverse_dns = tds[1].find('span', attrs={}).text

                additional_info = tds[2].text
                country = tds[2].find('span', attrs={}).text
                autonomous_system = additional_info.split(' ')[0]
                provider = ' '.join(additional_info.split(' ')[1:])
                provider = provider.replace(country, '')
                data = {'domain': domain,
                        'ip': ip,
                        'reverse_dns': reverse_dns,
                        'as': autonomous_system,
                        'provider': provider,
                        'country': country,
                        'header': header}
                res.append(data)
            except:
                pass

        return res


class ThreatCrowd(enumratorBase):
    def __init__(self, config):
        enumratorBase.__init__(self, config)

    def get_url(self, domain):
        return f"https://www.threatcrowd.org/searchApi/v2/domain/report/?domain={domain}"

    def req(self, url):
        try:
            resp = self.session.get(url, headers=self.headers, timeout=self.timeout)
        except Exception:
            resp = None

        return self.get_response(resp)

    def threatcrowd_enum(self, domain):
        url = self.get_url(domain)
        resp = self.req(url)
        if resp:
            self.extract_domains(resp)

    def enumerate(self):
        # Main enumeration on main domain
        self.threatcrowd_enum(self.domain)

        if self.recursive:
            # enumerate recursivly
            for subdomain in self.subdomains:
                self.threatcrowd_enum(subdomain)
                    

        return self.subdomains

    def extract_domains(self, resp):
        try:
            links = json.loads(resp)['subdomains']
            for link in links:
                subdomain = link.strip()
                if not subdomain.endswith(self.domain):
                    continue
                if subdomain not in self.subdomains and subdomain != self.domain:
                    self.subdomains.append(subdomain.strip())
        except:
            pass


class CrtSearch(enumratorBase):
    def __init__(self, config):
        self.wildcardsubdomains = list()
        enumratorBase.__init__(self, config)

    def get_url(self, domain):
        return f"https://crt.sh/?q={domain}&output=json"

    def req(self, url):
        try:
            resp = self.session.get(url, headers=self.headers, timeout=self.timeout)
        except Exception:
            resp = None

        return self.get_response(resp)

    def crtsh_enum(self, domain):
        url = self.get_url(domain)
        resp = self.req(url)
        if resp:
            self.extract_domains(resp)

    def enumerate(self):
        
        # Main enumeration on main domain
        self.crtsh_enum(self.domain)

        if self.recursive:
            # enumerate recursivly
            for wildcardsubdomain in self.wildcardsubdomains:
                wildcardsubdomain = wildcardsubdomain.replace('*.', '')
                self.crtsh_enum(wildcardsubdomain)

        return self.subdomains

    def extract_domains(self, resp):
        try:
            data = json.loads(resp)
            for i in range(len(data)):
                name_value = data[i]['name_value']
                subdomains = name_value.splitlines()

                for subdomain in subdomains:
                    if subdomain.find('*'):
                        if subdomain not in self.subdomains:
                            self.subdomains.append(subdomain)
                    else:
                        if subdomain not in self.wildcardsubdomains and subdomain != f"*.{self.domain}":
                            self.wildcardsubdomains.append(subdomain)
        except:
            pass

class PassiveDNS(enumratorBase):
    def __init__(self, config):
        enumratorBase.__init__(self, config)

    def get_url(self, domain):
        return f"https://api.sublist3r.com/search.php?domain={domain}"

    def req(self, url):
        try:
            resp = self.session.get(url, headers=self.headers, timeout=self.timeout)
        except:
            resp = None

        return self.get_response(resp)

    def passivedns_enum(self, domain):
        url = self.get_url(domain)
        resp = self.req(url)
        if resp:
            self.extract_domains(resp)


    def enumerate(self):
        # Main enumeration
        self.passivedns_enum(self.domain)

        if self.recursive:
            # enumerate recursivly
            for subdomain in self.subdomains:
                self.passivedns_enum(subdomain)    


        return self.subdomains

    def extract_domains(self, resp):
        try:
            subdomains = json.loads(resp)
            for subdomain in subdomains:
                if subdomain not in self.subdomains and subdomain != self.domain:
                    self.subdomains.append(subdomain.strip())
        except:
            pass

