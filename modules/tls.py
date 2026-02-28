
import ssl, socket, datetime
from Crypto.PublicKey import RSA, DSA, ECC
from Crypto.Util.asn1 import DerSequence
from Crypto.IO import PEM
from core.scanner.module import *


class TLSMisconfiguration( GlobalLevelScanner ):

    TIMEOUT = 10

    WEAK_RSA_BITS = 2048
    WEAK_DSA_BITS = 2048
    WEAK_ECC_BITS = 224


    def __init__(self, config, info = {
        "Authors": ["Abdallah Mohamed"],
        "Name": "TLS/SSL Misconfiguration",
        "Risk": Risk.High
    }):
        GlobalLevelScanner.__init__(self, config, info)
  
        self._hostname, self._port = self.__parse_host_and_port()

    def InitVulnInfo(self):
        return TLSMisConfigVulnInfo( self.GetEndPoint(), "TLS/SSL Misconfiguration" )

    def run(self):
        try:
            cipher, cert = self.__tls_send( ssl.create_default_context() )

            if cert:
                # Expiration
                not_after = cert.get( "notAfter" )
                if not_after:
                    expiry_date = datetime.datetime.strptime( not_after, "%b %d %H:%M:%S %Y %Z" )
                    if expiry_date < datetime.datetime.utcnow():
                        self.vulnInfo.register_vuln( "Certificate expired", str(expiry_date) )

                # Self-signed
                issuer = cert.get( "issuer" )
                subject = cert.get( "subject" )
                if issuer == subject:
                    self.vulnInfo.register_vuln( "Self-signed certificate", f"issuer = {issuer}, subject = {subject}" )

                # Weak key length
                vulnerable, key_type, bits = self.__check_weak_key_len()
                if vulnerable:
                    self.vulnInfo.register_vuln( "Weak key length", f"Key Type ({key_type}), Key Length ({str(bits)})" )

            if cipher:
                cipher_name, _, bits = cipher

                # Weak cipher strength
                if bits < 128:
                    self.vulnInfo.register_vuln( "Weak cipher", f"{cipher_name} ({bits} bits)" )

        except ssl.SSLError as e:
            self.vulnInfo.register_maybe( "SSL Error", str(e) )

        except Exception:
            return self.GetModuleInfo()

        for v in ( ssl.TLSVersion.TLSv1, ssl.TLSVersion.TLSv1_1 ):
            ctx = ssl.SSLContext( ssl.PROTOCOL_TLS_CLIENT )
            ctx.minimum_version = v
            ctx.maximum_version = v
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            try:
                self.__tls_send( ctx )
                self.vulnInfo.register_vuln( "Weak TLS version", v.name )
                break
            except:
                continue

        return self.GetModuleInfo()


    def __tls_send(self, ctx):
        conn = socket.create_connection( (self._hostname, self._port), timeout=self.TIMEOUT )
        conn = ctx.wrap_socket( conn, server_hostname=self._hostname )
        cipher, cert = conn.cipher(), conn.getpeercert()
        conn.close()
        return cipher, cert
    
    def __check_weak_key_len(self):
        try:
            pem = ssl.get_server_certificate( (self._hostname, self._port) )
            der = PEM.decode( pem )[0]

            cert = DerSequence()
            cert.decode( der )

            tbs_cert = DerSequence()
            tbs_cert.decode( cert[0] )

            spki_der = tbs_cert[ 5 + int(tbs_cert[0] >> 24 == 0xa0) ]

            try:
                bits = RSA.import_key( spki_der ).size_in_bits()
                if bits >= self.WEAK_RSA_BITS:
                    raise

                return True, "RSA", bits
            except:
                pass

            try:
                bits = DSA.import_key( spki_der ).y.bit_length()
                if bits >= self.WEAK_DSA_BITS:
                    raise
                
                return True, "DSA", bits
            except:
                pass

            try:
                bits = ECC.import_key( spki_der ).pointQ.size_in_bits()
                if bits >= self.WEAK_ECC_BITS:
                    raise
                
                return True, "ECC", bits
            except:
                pass

        except:
            pass

        return False, "", -1
    
    def __parse_host_and_port(self):
        uri = self.GetEndPoint().GetUri()
        hostname = ''
        port = 0
        if ':' in uri.netloc:
            hostname, port = uri.netloc.split( ':' )
            port = int( port )
        else:
            hostname = uri.netloc
            port = 443

        return hostname, port
        


class TLSMisConfigVulnInfo( VulnerabilityInfo ):

    def __init__(self, endpoint, vulnName) -> None:
        VulnerabilityInfo.__init__(self, endpoint, vulnName)

    def _add_vuln_(self, misconfig_type, evidence):
        self.vulnerables.append( {"Misconfiguration": misconfig_type, "Evidence": evidence} )