
from core.scanner.module import *

class ServerInformationDisclosure( HeadersBasedDataExposure, GlobalLevelScanner ):

    def __init__(self, config, info = {"Authors": ["Abdallah Mohamed"]}):
        HeadersBasedDataExposure.__init__(self, config, info)
        GlobalLevelScanner.__init__(self, config, info)

    def Check(self, data):
        s = data.get( "Server" )
        if s:
            self.SetHeaderName( "Server" )
            self.SetData( s )
            return Status.Vulnerable
        
        return Status.NotVulnerable
    

class XPowerdByInformationDisclosure( HeadersBasedDataExposure, GlobalLevelScanner ):

    def __init__(self, config, info = {"Authors": ["Abdallah Mohamed"]}):
        HeadersBasedDataExposure.__init__(self, config, info)
        GlobalLevelScanner.__init__(self, config, info)

    def Check(self, data):
        x_powered_by = data.get( "X-Powered-By" )
        if x_powered_by:
            self.SetHeaderName( "X-Powered-By" )
            self.SetData( x_powered_by )
            return Status.Vulnerable
        
        return Status.NotVulnerable
    

class SensitiveFilesExposure( UriScanner, GlobalLevelScanner ):

    def __init__(self, config, info = {"Authors": ["Abdallah Mohamed"]}):
        UriScanner.__init__(self, config, info)
        GlobalLevelScanner.__init__(self, config, info)
        
    def GetPayloads(self):
        return [ ".env", ".DS_Store", ".git/" ]
    
    def is_vulnerable(self, response):
        return Status.Vulnerable if 200 <= response.status_code < 400 else Status.NotVulnerable