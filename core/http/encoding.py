

import zlib, brotli


class IBaseCompressor:

    def __init__(self, buffer) -> None:
        self._buffer = buffer

    def compress(self) -> bytes:
        pass


class IBaseDecompressor:

    def __init__(self, buffer) -> None:
        self._buffer = buffer

    def decompress(self) -> bytes:
        pass


class GZipCompressor( IBaseCompressor ):

    def __init__(self, buffer) -> None:
        IBaseCompressor.__init__(self, buffer)

    def compress(self) -> bytes:
        return zlib.compress( self._buffer )


class GZipDecompressor( IBaseDecompressor ):

    def __init__(self, buffer) -> None:
        IBaseDecompressor.__init__(self, buffer)

    def decompress(self) -> bytes:
        return zlib.decompress( self._buffer, 16 + zlib.MAX_WBITS )


class BrotliCompressor( IBaseCompressor ):

    def __init__(self, buffer) -> None:
        IBaseCompressor.__init__(self, buffer)

    def compress(self) -> bytes:
        return brotli.compress( self._buffer )


class BrotliDecompressor( IBaseDecompressor ):

    def __init__(self, buffer) -> None:
        IBaseDecompressor.__init__(self, buffer)

    def decompress(self) -> bytes:
        return brotli.decompress( self._buffer )


class Compressor( IBaseCompressor ):

    def __init__(self, buffer, method) -> None:
        IBaseCompressor.__init__(self, buffer)
        self._method = method

    def get_compressor(self):
        if ( "gzip" or "deflate" ) in self._method:
            return GZipCompressor( self._buffer )

        elif "br" in self._method:
            return BrotliCompressor( self._buffer )

        else:
            raise CompressorError(f"{self._method} encoding is not supported !!")

    def compress(self) -> bytes:
        compressor = self.get_compressor()
        return compressor.compress()


class Decompressor( IBaseDecompressor ):

    def __init__(self, buffer, method) -> None:
        IBaseDecompressor.__init__( self, buffer )
        self._method = method

    def get_decompressor(self):
        if ( "gzip" or "deflate" ) in self._method:
            return GZipDecompressor( self._buffer )

        elif "br" in self._method:
            return BrotliDecompressor( self._buffer )

        else:
            raise DecompressorError(f"{self._method} encoding is not supported !!")

    def decompress(self) -> bytes:
        decompressor = self.get_decompressor()
        return decompressor.decompress()


class CompressorError( TypeError ):

    def __init__(self, *args: object) -> None:
        TypeError.__init__(self, *args)


class DecompressorError( TypeError ):

    def __init__(self, *args: object) -> None:
        TypeError.__init__(self, *args)

        