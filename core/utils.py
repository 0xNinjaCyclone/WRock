
import socket
from urllib.parse import *
from core.request import Headers


def GetAddrsFromHosts(hosts):
    addrs = []

    for host in hosts:
        try:
            ip = socket.gethostbyname(host)
            if ip not in addrs:
                addrs.append(ip)
        except:
            pass

    return addrs

def remove_duplicated_urls(urls):
    # Create a dictionary, using the List items as keys.
    # This will automatically remove any duplicates because dictionaries cannot have duplicated keys.
    
    return list(dict.fromkeys(urls))


def rduplicate(endpoints):
    # Remove duplicate urls with differents in params values 
    # like (https://example.com/?q=value1 && https://example.com/?q=value2)

    # Here we store urls with neutral values
    temp = list()

    # Here we store unduplicated urls
    results = list()

    for endpoint in endpoints:
        url = endpoint['url']
        uri = urlparse(url)
        query = parse_qs(uri.query)

        if query:
            for key in query.keys():
                query[key] = "value"

            tempurl = f"{uri.scheme}://{uri.netloc}{uri.path}?{urlencode(query)}"
            
            if tempurl not in temp:
                # Append to temp to check another urls based on
                temp.append(tempurl)

                # Append endpoing to results container because it has a uniqe url
                results.append(endpoint)

        else: # No params to check
            results.append(endpoint)


    return results


def get_urls_from_file(fileName):
    return remove_duplicated_urls([url.strip() for url in open(fileName,'r').readlines()])


def parse_headers_from_file(fileName):
    rawHeaders = str()

    with open(fileName, 'r') as f:
        for line in f.readlines():
            if ':' in line: # is a header ?
                # Convert to raw headers format
                rawHeaders += line.replace('\n', ';;')


    return Headers(Headers.Parser.toDict(rawHeaders[:-2]))