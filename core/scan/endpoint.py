
from urllib.parse import unquote, urlencode, urlparse, parse_qsl
from core.request import Get, Headers, Post


class EndPoint:

    def __init__(self, endpoint: dict) -> None:
        self.__uri          = urlparse(endpoint['url'])
        self.__m_type       = endpoint['m_type'].upper()
        self.__rawparams    = endpoint['params']
        self.__params       = self.__parse_params__()  # url params
        self.__data         = self.__parse_data__()    # body params

    def GetUri(self):
        return self.__uri

    def GetUrl(self):
        return f"{self.__uri.scheme}://{self.__uri.netloc + self.__uri.path}"

    def GetFullUrl(self):
        query = self.GetQuery()
        return self.GetUrl() + (f"?{query}" if query else str())

    def GetMethodType(self):
        return self.__m_type

    def GetQuery(self):
        return unquote(urlencode(self.GetParams()))

    def GetBody(self):
        return unquote(urlencode(self.GetData()))

    def GetParams(self):
        return self.__params

    def GetData(self):
        return self.__data

    def SetParam(self, pname, pvalue):
        if pname in self.__params:
            self.__params[pname] = pvalue

        elif pname in self.__data:
            self.__data[pname] = pvalue

        else:
            raise Exception(f"'{pname}' invalid parameter")

    def SetParams(self, params):
        for pname, pvalue in params.items():
            self.SetParam(pname, pvalue)

    def GetAllParams(self):
        return self.__params | self.__data

    def GetAllParamNames(self):
        return list(self.__params.keys()) + list(self.__data.keys())

    def GetParmTypeByName(self, pname):
        for p in self.__rawparams:
            if p['name'] == pname:
                return p['p_type']

        return ''

    def GetRequester(self, headers: Headers):
        return Get(self.GetUrl(), self.GetParams(), self.GetData(), headers) if self.GetMethodType() == 'GET' else Post(self.GetUrl(), self.GetParams(), self.GetData(), headers) 

    def __parse_params__(self):
        # Avoid using parse_qs because it represents values as a list like => {'param': ['value']}
        # We expect result as => {'param': 'value'}
        # For this reason we used parse_qsl then cast to a dict
        params = dict(parse_qsl(self.__uri.query))

        if self.GetMethodType() == 'GET':
            for param in self.__rawparams:
                params[param['name']] = param['value']

        return params

    def __parse_data__(self):
        params = dict()

        if self.GetMethodType() == 'POST':
            for param in self.__rawparams:
                params[param['name']] = param['value']

        return params
