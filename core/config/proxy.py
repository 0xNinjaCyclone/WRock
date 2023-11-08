

class ProxyConfig:
    
    def __init__(self) -> None:
        self.__host         = "0.0.0.0"
        self.__port         = 8000
        self.__timeout      = 20
        self.__max_req_len  = 1048576 # 1024KB
        self.__intercept    = False

    def SetHost(self, host):
        self.__host = host

    def GetHost(self):
        return self.__host

    def SetPort(self, port):
        self.__port = port

    def GetPort(self):
        return self.__port

    def SetTimeout(self, timeout):
        self.__timeout = timeout

    def GetTimeout(self):
        return self.__timeout

    def SetMaxRequestLength(self, n):
        self.__max_req_len = n

    def GetMaxRequestLength(self):
        return self.__max_req_len

    def EnableInterception(self):
        self.__intercept = True

    def DisableInterception(self):
        self.__intercept = False

    def IsInterceptionEnabled(self):
        return self.__intercept

        