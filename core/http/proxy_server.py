
import threading
from core.http.proxy import ProxyServer, HttpHandler, HttpsHandler
from core.config.proxy import ProxyConfig


def run_proxy_server(config: ProxyConfig, HttpForwarderHandler = HttpHandler, HttpsForwarderHandler = HttpsHandler, in_thread = False):
    server = ProxyServer( config )

    if in_thread:
        t = threading.Thread( target=server.Start, args=(HttpForwarderHandler, HttpsForwarderHandler) )
        t.daemon = True
        t.start()

    else:
        try:
            server.Start(HttpForwarderHandler, HttpsForwarderHandler)
        except:
            server.Stop()

    return server