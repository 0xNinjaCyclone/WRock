
from os.path import *
from core.scan.module import *


class SQLi(GeneralScanner):

    def __init__(self, config) -> None:
        GeneralScanner.__init__(self, config)
        self.save_sqlmap_format = self.options.get('sqlmap')
        self.response = None

    def check(self):
        # check if url has parameters
        # we cannot scan SQLi without parameters
        # put all prameters to vulnerable_params for scan it with payloads
        
        self.InsertAllParamsToScan()
        return bool(self.may_vulnerable_params)

    def GetPayloads(self):
        return list("'")

    def run(self):
        
        vulnerable = GeneralScanner.run(self)
            
        if vulnerable.status == Status.Vulnerable:
            if self.save_sqlmap_format and self.response != None:
                res = self.response
                uri = self.GetEndPoint().GetUri()
                vulnerableFileName = basename(uri.path)
                host = uri.hostname
                fileName = f"{vulnerableFileName if vulnerableFileName else host}-{self.vulnInfo.vulnerable_params[0]['param']}.sqlmap"
                http_version = '.'.join(list(str(res.raw.version)))
                self.ExportSqlmapFormat(fileName, http_version)
            
        return vulnerable

    def is_vulnerable(self, res):
        self.response = res

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
        if not isfile(fileName):
            with open(fileName,'w+') as f:
                req = self.GetRequester()
                headers = req.headers.GetAll()
                endpoint = self.GetEndPoint()
                uri = endpoint.GetUri()
                query = endpoint.GetQuery()

                f.write(f"{endpoint.GetMethodType()} {uri.path}" + (f"?{query} " if query else ' ') + f"HTTP/{http_version}\n")
                
                if "Host" not in headers.keys():
                    f.write(f"Host: {uri.hostname}\n")

                for header, value in headers.items():
                    f.write(f"{header}: {value}\n")

                # Write Body
                body = endpoint.GetBody()

                if body:
                    f.write(f"\n{body}")

