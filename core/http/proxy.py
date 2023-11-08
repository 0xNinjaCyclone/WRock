# Author  => Abdallah Mohamed
# Email   => elsharifabdallah53@gmail.com
# Date    => 3-11-2023


import socket, ssl, threading, os, datetime
from core.http.parser import *
from core.config.proxy import *
from core.data import rockPATH
from OpenSSL import crypto
from cryptography import x509 as CryptoX509
from cryptography.hazmat.primitives import serialization, hashes



class SSLKeysCreator:
    """ GENERATE SSL KEYs ( commands )
    openssl genrsa -out ca.key 2048
    openssl req -new -x509 -days 3650 -key ca.key -out ca.crt -subj "/CN=WRock CA"
    openssl genrsa -out cert.key 2048
    openssl req -new -key cert.key -subj /CN=<host> -out ca.req
    openssl x509 -req -in ca.req -days 365 -CA ca.crt -CAkey ca.key -CAcreateserial -out final.crt
    """

    CERTSDIR = os.path.join( rockPATH(), "core/http/certs/" )
    CAKEY    = "ca.key"   # Root key
    CACRT    = "ca.crt"   # Root cert
    CERTKEY  = "cert.key" # Clients certificates key

    def __init__(self) -> None:
        self.CheckOrCreateCertsDir()
        self.__keyfile = self.GetOrCreateKeyFile()
        self.__crtfile = self.GetOrCreateCRTFile()
        self.__certkey = self.GetOrCreateCertKey()

    def GetRootKeyPath(self):
        return self.__keyfile

    def GetCertPath(self):
        return self.__crtfile

    def GetCertKeyPath(self):
        return self.__certkey

    # Generate Private Key
    def CreateKeyFile(self, path):
        key = crypto.PKey()
        key.generate_key( crypto.TYPE_RSA, 2048 )
        data = key.to_cryptography_key().private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

        with open(path, "wb") as f:
            f.write( data )

    # Generate Certificate 
    def CreateCRTFile(self, path):
        key = self.__load_privatekey__( self.GetRootKeyPath() )
        certificate = crypto.X509()
        certificate.gmtime_adj_notBefore( 0 )
        certificate.gmtime_adj_notAfter( 60 * 60 * 24 * 365 )
        certificate.get_subject().CN = "WRock CA"
        certificate.set_serial_number( CryptoX509.random_serial_number() )
        certificate.set_issuer( certificate.get_subject() )
        certificate.set_pubkey( key )
        certificate.sign( key, "sha256" )

        with open(path, "wb") as f:
            f.write( crypto.dump_certificate(crypto.FILETYPE_PEM, certificate) )

    # Generate Certificate Signing Request (CSR)
    def CreateCSRCert(self, hostname):
        key_usage = [ b"Digital Signature",
                      b"Non Repudiation",
                      b"Key Encipherment" ]

        # Load private key for client certificates
        key = self.__load_privatekey__( self.GetCertKeyPath() )

        csr = crypto.X509Req()
        csr.get_subject().CN = hostname
        csr.add_extensions([
            crypto.X509Extension( b"basicConstraints", False, b"CA:FALSE" ),
            crypto.X509Extension( b"keyUsage", False, b",".join(key_usage) ),
            crypto.X509Extension( b"subjectAltName", False, b"DNS:" + hostname.encode() )
        ])
        csr.set_pubkey( key )
        csr.sign( key, "sha256" )
        return csr

    # Generate Certificate for client
    def CreateCertFile(self, path, hostname):
        key = self.__load_privatekey__( self.GetRootKeyPath() )
        crt = self.__load_certificate__( self.GetCertPath() )
        csr = self.CreateCSRCert( hostname ) 

        ca_cert = crt.to_cryptography()
        ca_key = key.to_cryptography_key() 
        csr_ = csr.to_cryptography()

        data = CryptoX509.CertificateBuilder().subject_name(
            csr_.subject
        ).issuer_name(
            ca_cert.subject
        ).public_key(
            csr_.public_key()
        ).serial_number(
            CryptoX509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=365)
        ).sign(
            ca_key, hashes.SHA256()
        ).public_bytes(
            encoding=serialization.Encoding.PEM
        )

        with open(path, "wb") as f:
            f.write( data )

        # # CREATE USING OpenSSL lib ( Doesn't work for some reasons i don't know )
        # epoch = int( time.time() * 1000 )
        # current_ts = int(datetime.datetime.now().timestamp())
        # cert = crypto.X509()
        # cert.set_serial_number( epoch )
        # cert.set_subject( csr.get_subject() )
        # cert.set_issuer( crt.get_subject() )
        # cert.gmtime_adj_notBefore( current_ts )
        # cert.gmtime_adj_notAfter( current_ts + 60 * 60 * 24 * 365 )        
        # cert.set_pubkey( csr.get_pubkey() )
        # cert.sign( key, "sha256" )

        # with open(path, "wb") as f:
        #     f.write( crypto.dump_certificate(crypto.FILETYPE_PEM, cert) )

    def CheckOrCreateCertsDir(self):
        if not os.path.isdir( SSLKeysCreator.CERTSDIR ):
            os.mkdir( SSLKeysCreator.CERTSDIR )

    def GetOrCreateKeyFile(self):
        keyfile = os.path.join( SSLKeysCreator.CERTSDIR, SSLKeysCreator.CAKEY )

        if not os.path.isfile( keyfile ):
            self.CreateKeyFile( keyfile )

        return keyfile

    def GetOrCreateCRTFile(self):
        cacrt = os.path.join( SSLKeysCreator.CERTSDIR, SSLKeysCreator.CACRT )

        if not os.path.isfile( cacrt ):
            self.CreateCRTFile( cacrt )

        return cacrt

    def GetOrCreateCertKey(self):
        certkey = os.path.join( SSLKeysCreator.CERTSDIR, SSLKeysCreator.CERTKEY )

        if not os.path.isfile( certkey ):
            self.CreateKeyFile( certkey )

        return certkey

    def GetOrCreateCertFile(self, hostname):
        certfile = os.path.join( SSLKeysCreator.CERTSDIR, hostname + '.crt' )

        if not os.path.isfile( certfile ):
            self.CreateCertFile( certfile, hostname )

        return certfile

    def __load_privatekey__(self, path):
        with open(path, "rb") as f:
            data = f.read()
        
        # return crypto.PKey.from_cryptography_key( serialization.load_pem_private_key(data, None) )
        return crypto.load_privatekey( crypto.FILETYPE_PEM, data )

    def __load_certificate__(self, path):
        with open(path, "rb") as f:
            data = f.read()

        return crypto.load_certificate( crypto.FILETYPE_PEM, data )


class SSLNegotiatorError( Exception ):

    def __init__(self, *args: object) -> None:
        Exception.__init__(self, *args)


class SSLNegotiator:

    def __init__(self, client, cert_creator, req: RequestParser) -> None:
        self.__client = client
        self.__req = req
        self.__cert_creator = cert_creator

    def is_try_connect(self) -> bool:
        return self.__req.GetMethod() == "CONNECT"

    def reply(self):
        self.__client.sendall( b"HTTP/1.1 200 Connection Established\r\n\r\n" )

    def wrap(self) -> ssl.SSLSocket:
        context = ssl.SSLContext( ssl.PROTOCOL_TLS_SERVER )
        context.minimum_version = ssl.TLSVersion.MINIMUM_SUPPORTED
        context.maximum_version = ssl.TLSVersion.MAXIMUM_SUPPORTED
        context.load_verify_locations( cafile=self.__cert_creator.GetCertPath() )
        context.load_cert_chain(
            certfile=self.__cert_creator.GetOrCreateCertFile( self.__req.GetFullURI().hostname ),
            keyfile=self.__cert_creator.GetCertKeyPath()
        )
        
        return context.wrap_socket( self.__client, server_side=True )

    def negotiate(self):
        if not self.is_try_connect():
            raise SSLNegotiatorError("the client is trying connect without using CONNECT method")

        self.reply()
        self.__client = self.wrap()
        return self.__client


class IForwarderHandler:

    def __init__(self, config: ProxyConfig, client, buffer, parser: RequestParser) -> None:
        self.__config = config
        self.__client = client
        self.__parser = parser
        self._uri = self.__parser.GetFullURI()
        self.__tunnel = self.establish()

        self.handle( buffer )

    def establish(self) -> socket.socket:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout( self.__config.GetTimeout() )
        sock.connect( (socket.gethostbyname(self._uri.hostname), self._uri.port if self._uri.port else 443 if self._uri.scheme == "https" else 80) )
        return sock

    def cleanup(self):
        self.__tunnel.close()
        self.__client.close()

    def forward(self, conn, buffer: bytes):
        conn.sendall( buffer )

    def forward_to_server(self, buffer: bytes):
        self.forward( self.__tunnel, buffer )

    def forward_to_client(self, buffer: bytes):
        self.forward( self.__client, buffer )

    def receive(self, conn, n = 0, forward_to = None, timeout_stop = False) -> bytes:
        receiver = Receiver( conn )
        return receiver.recv( self.__config.GetMaxRequestLength(), n, timeout_stop, forward_to )

    def receive_and_forward(self, from_, to_) -> bytes:
        receiver = Receiver( from_, self.__config.GetMaxRequestLength() )
        return receiver.recv_http_data( forward_to=to_ )

    def receive_from_server(self) -> bytes:
        receiver = Receiver( self.__tunnel, self.__config.GetMaxRequestLength() )
        return receiver.recv_http_data()

    def receive_from_client(self) -> bytes:
        receiver = Receiver( self.__client, self.__config.GetMaxRequestLength() )
        return receiver.recv_http_data()

    def handle(self, buffer):
        self.forward_to_server( buffer )

        if self.__config.IsInterceptionEnabled():
            response = self.receive_from_server()
            self.forward_to_client( response )

        else:
            self.receive_and_forward( self.__tunnel, self.__client )
        
        self.cleanup()


class HttpHandler( IForwarderHandler ):
    
    def __init__(self, config, client, buffer, parser: RequestParser) -> None:
        IForwarderHandler.__init__(self, config, client, buffer, parser)


class HttpsHandler( IForwarderHandler ):
    
    def __init__(self, config, client, buffer, parser: RequestParser) -> None:
        IForwarderHandler.__init__(self, config, client, buffer, parser)

    def establish(self):
        sock = IForwarderHandler.establish( self )
        context = ssl.SSLContext( ssl.PROTOCOL_TLS_CLIENT )
        context.minimum_version = ssl.TLSVersion.MINIMUM_SUPPORTED
        context.maximum_version = ssl.TLSVersion.MAXIMUM_SUPPORTED
        context.load_default_certs()
        return context.wrap_socket( sock, server_hostname=self._uri.hostname )


class ProxyServerNotSupportedProtocol( Exception ):

    def __init__(self, *args: object) -> None:
        Exception.__init__(self, *args)


class ProxyServerRunningAlready( Exception ):

    def __init__(self, *args: object) -> None:
        Exception.__init__(self, *args)


class ProxyServerNotRunning( Exception ):

    def __init__(self, *args: object) -> None:
        Exception.__init__(self, *args)


class ProxyServer:

    def __init__(self, config: ProxyConfig) -> None:
        self.__config = config
        self.__sock = None
        self.__running = False
        self.__cert_creator = SSLKeysCreator()

    def running(self) -> bool:
        return self.__running

    def Start(self, HttpForwarderHandler = HttpHandler, HttpsForwarderHandler = HttpsHandler):
        if self.running():
            raise ProxyServerRunningAlready(f"The proxy server is running already on {self.__config.GetHost()}:{self.__config.GetPort()}")

        
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__sock.bind( (self.__config.GetHost(), self.__config.GetPort()) )
        self.__sock.listen( 10 )
        self.__running = True

        while self.running():
            client, _ = self.__sock.accept()
            thrd = threading.Thread( target=self.handle, args=(client, HttpForwarderHandler, HttpsForwarderHandler,) )
            thrd.daemon = True
            thrd.start()

    def Stop(self):
        if not self.running():
            raise ProxyServerNotRunning("The proxy is not running !!")

        self.__running = False
        self.__sock = self.__sock.close()

    def handle(self, client, HttpForwarderHandler, HttpsForwarderHandler):
        buffer = self.__recvreq__( client )

        if not buffer:
            return

        req_parser = RequestParser( buffer )
        protocol = req_parser.GetFullURI().scheme

        if protocol == "https":
            try:
                negotiator = SSLNegotiator(client, self.__cert_creator, req_parser)
                client = negotiator.negotiate()
                buffer = self.__recvreq__( client )
                HttpsForwarderHandler( self.__config, client, buffer, req_parser )
            except:
                return


        elif protocol == "http":
            try:
                HttpForwarderHandler( self.__config, client, buffer, req_parser )
            except:
                return

        else:
            raise ProxyServerNotSupportedProtocol( f"{protocol} is not supported !!" )

    def __recvreq__(self, conn):
        nMaxReqLen = self.__config.GetMaxRequestLength()
        receiver = Receiver( conn, nMaxReqLen )
        return receiver.recv_http_data()


class Receiver:

    def __init__(self, conn, maxlen) -> None:
        self._conn = conn
        self._nReadMaxLen = maxlen

    def recv(self, n = 0, timeout_stop = False, transfer_chunked = False, forward_to = None):
        buf = b''

        if n != 0:
            while n > 0:
                try:
                    data = self._conn.recv( self._nReadMaxLen )
                    buf += data
                    n -= len( data )

                    if forward_to:
                        forward_to.send( data )
                except:
                    break

        elif timeout_stop:
            timeout = self._conn.gettimeout()
            self._conn.settimeout( 1.5 )

            while True:
                try:
                    data = self._conn.recv( self._nReadMaxLen )
                    buf += data

                    if not data:
                        break

                    if forward_to:
                        forward_to.send( data )

                except:
                    break

            self._conn.settimeout( timeout )

        elif transfer_chunked:
            data = b''

            while not data.endswith( b"\x30\x0d\x0a\x0d\x0a" ):
                try:
                    data = self._conn.recv( self._nReadMaxLen )
                    buf += data

                    if not data:
                        break

                    if forward_to:
                        forward_to.send( data )
                except:
                    break

        else:
            try:
                buf += self._conn.recv( self._nReadMaxLen )
            except:
                pass

            if forward_to:
                forward_to.send( buf )
            

        return buf

    def recv_http_data(self, forward_to = None) -> bytes:
        buf = self.recv( forward_to=forward_to )

        if not buf:
            return buf

        headers = RawPacketHeadersParser( buf ).parse()

        if "Content-Length" in headers:
            nContentAlreadyRead = len( buf.split( b"\r\n\r\n" )[1] )
            nBytesToRead = int( headers["Content-Length"] ) - nContentAlreadyRead
            buf += self.recv( nBytesToRead, forward_to=forward_to )

        # Chunked Transfer as descriped in rfc2616#section-4.4
        elif "Transfer-Encoding" in headers and headers["Transfer-Encoding"] != 'identity':
            if not buf.endswith( b"\x30\x0d\x0a\x0d\x0a" ):
                buf += self.recv( transfer_chunked=True, forward_to=forward_to )

        else:
            buf += self.recv( timeout_stop=True, forward_to=forward_to )

        return buf




