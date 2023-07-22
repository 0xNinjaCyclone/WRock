
from os.path import *
from core.scanner.module import *


class SQLi(ParamsScanner):

    def __init__(self, config, info = {
        "Authors": ["Abdallah Mohamed"],
        "Name": "SQL Injection",
        "Description": 'The product constructs all or part of an SQL command using externally-influenced input from an upstream component, but it does not neutralize or incorrectly neutralizes special elements that could modify the intended SQL command when it is sent to a downstream component.',
        "Risk": Risk.Critical,
        "Referances": [
            "https://cwe.mitre.org/data/definitions/89.html",
            "https://owasp.org/www-community/attacks/SQL_Injection"
        ]
    }) -> None:
        ParamsScanner.__init__(self, config, info)
        self.save_sqlmap_format = self.options.get('sqlmap')
        self.response = None
        

    def GetPayloads(self):
        return list("'")

    def run(self):
        
        result = ParamsScanner.run(self)
        vulnerable = result.GetVulnInfo()
            
        if vulnerable.status == Status.Vulnerable:
            if self.save_sqlmap_format and self.response != None:
                res = self.response
                uri = self.GetEndPoint().GetUri()
                vulnerableFileName = basename(uri.path)
                host = uri.hostname
                fileName = f"{vulnerableFileName if vulnerableFileName else host}-{self.vulnInfo.vulnerables[0]['param']}.sqlmap"
                http_version = '.'.join(list(str(res.raw.version)))
                self.ExportSqlmapFormat(fileName, http_version)
            
        return result

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
                headers = self.GetHeaders()
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

