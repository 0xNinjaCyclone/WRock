
from os.path import *
from core.scan.module import *


class SQLi(GeneralScanner):

    def __init__(self, config) -> None:
        GeneralScanner.__init__(self, config)
        self.save_sqlmap_format = self.options.get('sqlmap')

    def check(self):
        # check if url has parameters
        # we cannot scan SQLi without parameters
        # put all prameters to vulnerable_params for scan it with payloads
        
        self.vulnerable_params = self.request.GetParams()
        return bool(self.vulnerable_params)

    def GetPayloads(self):
        return list("'")

    def run(self):
        
        vulnerable = GeneralScanner.run(self)
            
        if vulnerable.status == Status.Vulnerable:
            if self.save_sqlmap_format:
                res = self.request.Send()
                fileName = f"{basename(self.request.uri.path)}-{list(self.request.GetParams())[0]}.sqlmap"
                http_version = '.'.join(list(str(res.raw.version)))
                self.ExportSqlmapFormat(fileName, http_version)
            
        return vulnerable

    def is_vulnerable(self,res):
        expected_errors = [
            "Fatal error:","mysql_fetch_array()","Warning: mysql_fetch_array()",
            "ORA-01756:","quoted string not properly terminated.","MariaDB","SQL syntax","Syntax error",
            "You have an error in your SQL syntax","Unclosed quotation mark after the character string"
        ]

        for err in expected_errors:
            if err.lower() in res.text.lower():
                return True

        return False

    def ExportSqlmapFormat(self, fileName, http_version):
        headers = self.request.headers
        params = self.request.GetParams()

        if not isfile(fileName):
            with open(fileName,'w+') as f:
                query = str()
                for param in params.keys():
                    query += f"{param}={params[param][0]}"
                    
                    # if this not last query
                    if param != list(params.keys())[-1]:
                        query += '&'
                
                f.write(f"GET {self.request.uri.path}?{query} HTTP/{http_version}\n")
                
                for header, value in headers.GetAll().items():
                    f.write(f"{header}: {value}\n")

