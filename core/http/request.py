
import requests, threading
from urllib.parse import *
from core.http.headers import Headers

class Request:
    _sess = None
    _mutex = threading.Lock()

    def __init__(self, url, params = {}, data = {}, headers: Headers = Headers(), proxy = None) -> None:
        self.url                = url
        self.params             = params # Url parameters
        self.data               = data   # Body parameters
        self.headers            = headers
        self.proxy              = proxy

        with Request._mutex:
            if not Request._sess:
                Request._sess = self.GetReqSession()

    def SetUrl(self, url):
        self.url = url

    def SetParams(self, params: dict):
        self.params = params

    def SetData(self, data):
        self.data = data

    def SetHeaders(self, headers: Headers):
        self.headers = headers

    def GetReqSession(self) -> requests.Session:
        s = requests.Session()
        if self.proxy:
            s.proxies.update( self.proxy )
        return s

    def Send(self, **args) -> requests.Response or None:
        pass

    def get(self, **args):
        return self.SendReq(Request._sess.get, **args)

    def post(self, **args):
        return self.SendReq(Request._sess.post, **args)

    def SendReq(self, reqMethod, **args):
        if "timeout" not in args: # force specifying timeout to avoid stuck at any f*cking point
            args[ "timeout" ] = 10
        return reqMethod(self.url, params=self.params, data=self.data, headers=self.headers, **args)


class Get(Request):
    def __init__(self, url, params={}, data={}, headers: Headers = Headers(), proxy = None) -> None:
        Request.__init__(self, url, params, data, headers, proxy)

    def Send(self, **args) -> requests.Response or None:
        return Request.get(self, **args)


class Post(Request):
    def __init__(self, url, params={}, data={}, headers: Headers = Headers(), proxy = None) -> None:
        Request.__init__(self, url, params, data, headers, proxy)

    def Send(self, **args) -> requests.Response or None:
        return Request.post(self, **args)