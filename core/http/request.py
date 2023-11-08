
import requests
from urllib.parse import *
from core.http.headers import Headers

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