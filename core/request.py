
import requests
from urllib.parse import *


class HeadersValueError(ValueError):
    def __init__(self, *args: object) -> None:
        ValueError.__init__(self, *args)

class HeadersTypeError(TypeError):
    def __init__(self, *args: object) -> None:
        TypeError.__init__(self, *args)


class Headers( dict ):

    class Parser:

        @classmethod
        def toDict(cls, rawHeaders):
            if isinstance(rawHeaders, str):
                headers = {}
                unparsed = rawHeaders.splitlines() if '\n' in rawHeaders else rawHeaders.split(";;") if ';;' in rawHeaders else [rawHeaders]
                
                for header in unparsed:
                    if ':' not in header:
                        raise HeadersValueError("headers flag not formatted properly (no colon to separate header and value)")

                    delimiter = ': ' if ': ' in header else ':' 
                    headerName, headerValue = header.split(delimiter)
                    headers[headerName] = headerValue


                return headers

            raise HeadersTypeError(f"{type(rawHeaders)} not expected, pass string seperated by two semi-colons")

        @classmethod
        def toRaw(cls, headers):
            if isinstance(headers, dict):
                rawHeaders = str()

                for key , value in headers.items():
                    rawHeaders += key + ': ' + value + ';;'

                return rawHeaders[:-2] if rawHeaders else rawHeaders

            raise HeadersTypeError(f"{type(headers)} not expected, pass a dict")

        @classmethod
        def toHttpRaw(cls, headers):
            if isinstance(headers, dict):
                rawHttpHeadersList = [
                    f"{hname}: {hvalue}" for hname, hvalue in headers.items()
                ]

            elif isinstance(headers, str):
                rawHttpHeadersList = headers.split(';;')

            else:
                raise HeadersTypeError(f"{type(headers)} not expected")

            return '\n'.join(rawHttpHeadersList)


    def __init__(self, __map = None, **kwargs):
        dict.__init__(self, __map if bool(__map) else {}, **kwargs)
        self.__set_defaults()

    def add(self, headname, headval):
        if not self.ishead(headname):
            self[headname] = headval

    def update2(self, headname, headval):
        self[headname] = headval

    def remove(self, headname):
        if self.ishead(headname):
            del self[headname]

    def ishead(self, headname):
        return headname in self

    def __set_defaults(self):

        self.add('User-Agent', 
                        'Mozilla/5.0 (Windows NT 10.0; rv:54.0) Gecko/20100101 Firefox/54.0'
        )

        self.add('Accept',
                        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        )

        self.add('Accept-Encoding', 'gzip, deflate')
        self.add('Accept-Language', 'en-US,en;q=0.5')
        self.add('Upgrade-Insecure-Requests', '1')
        self.add('Connection', 'keep-alive')



class Request:

    def __init__(self, url, params = {}, data = {}, headers: Headers = Headers()) -> None:
        self.url                = url
        self.params             = params # Url parameters
        self.data               = data   # Body parameters
        self.headers            = headers
        self.session            = self.GetReqSession()

    def SetUrl(self, url):
        self.url = url

    def SetParams(self, params: dict):
        self.params = params

    def SetData(self, data):
        self.data = data

    def SetHeaders(self, headers: Headers):
        self.headers = headers

    def GetReqSession(self) -> requests.Session:
        return requests.Session()

    def Send(self, **args) -> requests.Response or None:
        pass

    def get(self, **args):
        return self.SendReq(self.session.get, **args)

    def post(self, **args):
        return self.SendReq(self.session.post, **args)

    def SendReq(self, reqMethod, **args):
        return reqMethod(self.url, params=self.params, data=self.data, headers=self.headers, **args)


class Get(Request):
    def __init__(self, url, params={}, data={}, headers: Headers = Headers()) -> None:
        Request.__init__(self, url, params, data, headers)

    def Send(self, **args) -> requests.Response or None:
        return Request.get(self, **args)


class Post(Request):
    def __init__(self, url, params={}, data={}, headers: Headers = Headers()) -> None:
        Request.__init__(self, url, params, data, headers)

    def Send(self, **args) -> requests.Response or None:
        return Request.post(self, **args)