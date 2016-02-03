import threading
import os
import logging
from wsgiref.simple_server import make_server

logger = logging.getLogger("restsense")


class HTTPServerThread(threading.Thread):
    """
    Open a HTTP/TCP Port and spit out json response.
    """
    def __init__(self, ipaddress, port, app):
        super(HTTPServerThread, self).__init__()
        self.ipaddress = ipaddress
        self.port = port
        self.name = "HTTPServerThread-%s" % self.ipaddress
        self.setDaemon(True)
        self.stop_event = threading.Event()
        self.httpd = make_server(self.ipaddress, self.port, app)
        logger.debug("Thread : %s. %s:%s initialized" % (self.name, self.ipaddress, str(self.port)))

    def stop(self):
        self.stop_event.set()
        self.httpd.shutdown()


    def run(self):
        logger.debug("Thread : %s. Serving on %s:%s" % (self.name, self.ipaddress, str(self.port)))
        self.httpd.serve_forever()
