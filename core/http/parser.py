
import dpkt, re, zlib
from urllib.parse import *
from typing import OrderedDict


class IBaseParser( dpkt.http.Message ):

    def __init__(self, *args, **kwargs):
        dpkt.http.Message.__init__(self, *args, **kwargs)

    def GetHeaders(self) -> OrderedDict | None:
        return self.headers

    def GetHeaderByKey(self, key) -> str:
        return self.headers[key]

    def HeadersContain(self, key) -> bool:
        return key in self.headers

    def GetRawHeaders(self) -> str:
        return self.pack_hdr()

    def GetBody(self) -> bytes:
        # Return parsed HTTP body
        return self.body

    def GetData(self) -> bytes:
        return self.data

    
class RequestParser( IBaseParser, dpkt.http.Request ):

    def __init__(self, *args, **kwargs):
        dpkt.http.Request.__init__(self, *args, **kwargs)

    def GetMethod(self):
        return self.method

    def GetURI(self):
        return self.uri

    def GetFullURI(self):
        uri = self.uri

        if not re.search(r'^[A-Za-z0-9+.\-]+://', uri):
            uri = "https://" + uri

        return urlparse( uri )

    def GetVersion(self):
        return self.version


class ResponseParser( IBaseParser, dpkt.http.Response ):

    def __init__(self, *args, **kwargs):
        dpkt.http.Response.__init__(self, *args, **kwargs)

    def GetStatus(self):
        return self.status

    def GetReason(self):
        return self.reason

    def GetVersion(self):
        return self.version


class RawPacketHeadersParser:

    def __init__(self, buffer: bytes) -> None:
        self._raw = buffer

    def parse(self) -> dict:
        headers = {}
        lines = self._raw.split( b"\r\n" )[1:-1]

        for line in lines:
            line = line.decode( errors='ignore' )

            if ": " not in line:
                continue

            key, val = line.split( ": ", 1 )
            headers[ key ] = val


        return headers


class BaseStreamParser( object ):
    def __init__(self, *args, **kwargs):
        self.reset()

    def reset(self, data=None):
        self._field = None
        self._data = data
        self._parse_next = self._parse_start

    def getline(self):
        i = self._data.find('\n')
        if i < 0:
            raise NeedInput
        line, self._data = self._data[:i+1], self._data[i+1:]
        return line

    def feed(self, data):
        if self._data:
            self._data += data
        else:
            self._data = data
        while self._data:
            try:
                self._parse_next()
            except NeedInput:
                break

    def _parse_start(self):
        self.handle_start()
        self._parse_next = self._parse_field

    def _parse_field(self):
        line = self.getline()
        if line.startswith(' ') or line.startswith('\t'):
            # line continuation
            self._field = '%s %s' % (self._field, line.strip())
        else:
            if self._field:
                # if we had a previous field, parse it
                name, value = self._field.split(':', 1)
                value = value.strip()
                self.handle_field(name, value)
                """
                try:
                    m = getattr(self, 'do_%s' % name.lower().replace('-', '_'))
                    m(name, value)
                except AttributeError:
                    pass
                """
                self._field = None
            line = line.strip()
            if line:
                self._field = line
            else:
                self._end_fields()

    def _end_fields(self):
        self._parse_next = self._parse_body

    def _parse_body(self):
        self.handle_body(self._data)
        self.handle_end()
        self.reset()

    def handle_start(self):
        """Override to handle start of a message."""
        pass

    def handle_end(self):
        """Override to handle the end of a message."""
        pass

    def handle_field(self, name, value):
        """Override to handle header field."""
        pass

    def handle_body(self, body):
        """Override to handle some body data (not necessarily all of it)."""
        pass


class StreamHttpParser( BaseStreamParser ):
    methods = dict.fromkeys((
        'GET', 'PUT', 'ICY',
        'COPY', 'HEAD', 'LOCK', 'MOVE', 'POLL', 'POST',
        'BCOPY', 'BMOVE', 'MKCOL', 'TRACE', 'LABEL', 'MERGE',
        'DELETE', 'SEARCH', 'UNLOCK', 'REPORT', 'UPDATE', 'NOTIFY',
        'BDELETE', 'CONNECT', 'OPTIONS', 'CHECKIN',
        'PROPFIND', 'CHECKOUT', 'CCM_POST',
        'SUBSCRIBE', 'PROPPATCH', 'BPROPFIND',
        'BPROPPATCH', 'UNCHECKOUT', 'MKACTIVITY',
        'MKWORKSPACE', 'UNSUBSCRIBE', 'RPC_CONNECT',
        'VERSION-CONTROL',
        'BASELINE-CONTROL'
        ))
    proto = 'HTTP'

    def __init__(self, *args, **kwargs):
        BaseStreamParser.__init__(self, *args, **kwargs)

    def reset(self, data=None):
        """Reset HTTP parser."""
        BaseStreamParser.reset( self, data )
        self.body_len = self.chunk_len = self.zlib = self.gzcnt = None
        self.headers = {}

    def _parse_start(self):
        # XXX - RFC 2616, 4.1
        while True:
            line = self.getline().strip()
            if line: break

        l = line.split(None, 2)
        if len(l) == 2:
            l.append('')    # XXX - empty version

        if l[0].startswith(self.proto):
            # HTTP response
            version, status, reason = l
            status = int(status)
            if status == 204 or status == 304 or 100 <= status < 200:
                self.body_len = 0
            self.handle_response(version, status, reason)
        else:
            # HTTP request
            try:
                method, uri, version = l
            except ValueError:
                return
            if method not in self.methods or \
                   not version.startswith(self.proto):
                return  # XXX - be forgiving of mid-stream parsing
            if method == 'HEAD':
                self.body_len = 0
            self.handle_request(method, uri, version)

        BaseStreamParser._parse_start( self )

    def handle_headers(self, headers):
        """Overload to handle a dict of HTTP headers."""
        pass

    def handle_request(self, method, uri, version):
        """Overload to handle a new HTTP request."""
        pass

    def handle_response(self, version, status, reason):
        """Overload to handle a new HTTP response."""
        pass

    def handle_field(self, name, value):
        """HTTP header field collector."""
        name = name.lower()
        self.headers[name] = value

    def _end_fields(self):
        self.handle_headers(self.headers)
        self._zlib_setup(self.headers)
        if self.headers.get('transfer-encoding', '').lower() == 'chunked':
            self._parse_next = self.__parse_body_chunked
        elif self.body_len == 0:
            self.reset(self._data)
        elif 'content-length' in self.headers:
            self.body_len = int(self.headers['content-length'])
            self._parse_next = self.__parse_body_len
        elif self.headers.get('connection', '').lower() == 'keep-alive':
            self.reset(self._data)
        else:
            self._parse_next = self.__parse_body_close

    def _zlib_setup(self, hdrs):
        if 'gzip' in hdrs.get('content-encoding', '') or \
           'gzip' in hdrs.get('transfer-encoding', ''):
            self.zlib = zlib.decompressobj(-zlib.MAX_WBITS)
            self.gzcnt = 10     # XXX - vanilla gzip hdr len
        else:
            self.zlib = None
            self.gzcnt = 0

    def _zlib_decompress(self, buf):
        if self.zlib is not None:
            if self.gzcnt:
                n = min(self.gzcnt, len(buf))
                self.gzcnt -= n
                buf = buf[n:]
            if buf:
                buf = self.zlib.decompress(buf)
        return buf

    def __parse_body_close(self):
        self.handle_body(self._zlib_decompress(self._data))
        self._data = ''
        # XXX - self.handle_end() never called!

    def __parse_body_len(self):
        buf = self._data[:self.body_len]
        self.handle_body(self._zlib_decompress(buf))
        self._data = self._data[self.body_len:]
        self.body_len -= len(buf)
        if not self.body_len:
            self.handle_end()
            self.reset(self._data)

    def __parse_body_chunked(self):
        if self.chunk_len is None:
            line = self.getline()
            self.chunk_len = int(line.split(None, 1)[0], 16)
            if self.chunk_len == 0:
                self.chunk_len = -1
        elif self.chunk_len > 0:
            buf = self._data[:self.chunk_len]
            s = self._zlib_decompress(buf)
            if s:
                self.handle_body(s)
            self._data = self._data[self.chunk_len:]
            self.chunk_len -= len(buf)
        else:
            line = self.getline()
            if self.chunk_len < 0:
                self.handle_end()
                self.reset(self._data)
            else:
                self.chunk_len = None


class NeedInput(Exception):

    def __init__(self, *args: object) -> None:
        Exception.__init__(self, *args)


class ParseError(Exception):

    def __init__(self, *args: object) -> None:
        Exception.__init__(self, *args)