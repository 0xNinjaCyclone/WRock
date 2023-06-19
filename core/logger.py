
from queue import Queue
from enum import Enum, auto


class Level( Enum ):
    CRITICAL = auto()
    INFO     = auto()
    DEBUG    = auto()

class MessageType( Enum ):
    SUCCESS = auto()
    STATUS  = auto()
    WARN    = auto()
    ERROR   = auto()


class Record:

    def __init__(self, level, msgtype, message) -> None:
        self.__level   = level
        self.__msgtype = msgtype
        self.__message = message

    def GetLevel(self):
        return self.__level

    def GetType(self):
        return self.__msgtype

    def GetMessage(self):
        return self.__message


class Logger( Queue ):

    _initialized = False

    # Singleton pattern to access the same logger object many times in different places 
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Logger, cls).__new__(cls)
            
        return cls.instance

    def __init__(self, maxsize: int = 0) -> None:
        if not Logger._initialized:
            Logger._initialized = True
            Queue.__init__(self, maxsize)

    def Log(self, level, msgtype, message):
        self.put( Record(level, msgtype, message) )

    def LogCritical(self, msgtype, message):
        self.Log(Level.CRITICAL, msgtype, message)

    def LogInfo(self, msgtype, message):
        self.Log(Level.INFO, msgtype, message)

    def LogDebug(self, msgtype, message):
        self.Log(Level.DEBUG, msgtype, message)