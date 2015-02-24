import logging
import sys
import SocketServer

logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                    )


class TCPHandler(SocketServer.StreamRequestHandler):

    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger('EchoRequestHandler')
        self.logger.debug('__init__')
        SocketServer.StreamRequestHandler.__init__(self, request, client_address, server)
        return

    def setup(self):
        self.logger.debug('setup')
        return SocketServer.StreamRequestHandler.setup(self)

    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        self.data = self.rfile.readline().strip()
        print "{} wrote:".format(self.client_address[0])
        print self.data
        # Likewise, self.wfile is a file-like object used to write back
        # to the client
        self.wfile.write(self.data.upper())

    def finish(self):
        self.logger.debug('finish')
        return SocketServer.StreamRequestHandler.finish(self)

class myServer(SocketServer.TCPServer):
    
    def __init__(self, server_address, handler_class=EchoRequestHandler):
        self.logger = logging.getLogger('EchoServer')
        self.logger.debug('__init__')
        SocketServer.TCPServer.__init__(self, server_address, handler_class)
        return

    def server_activate(self):
        self.logger.debug('server_activate')
        SocketServer.TCPServer.server_activate(self)
        return

    def serve_forever(self):
        self.logger.debug('waiting for request')
        self.logger.info('Handling requests, press <Ctrl-C> to quit')
        while True:
            self.handle_request()
        return

    def handle_request(self):
        self.logger.debug('handle_request')
        return SocketServer.TCPServer.handle_request(self)

    def verify_request(self, request, client_address):
        self.logger.debug('verify_request(%s, %s)', request, client_address)
        return SocketServer.TCPServer.verify_request(self, request, client_address)

    def process_request(self, request, client_address):
        self.logger.debug('process_request(%s, %s)', request, client_address)
        return SocketServer.TCPServer.process_request(self, request, client_address)

    def server_close(self):
        self.logger.debug('server_close')
        return SocketServer.TCPServer.server_close(self)

    def finish_request(self, request, client_address):
        self.logger.debug('finish_request(%s, %s)', request, client_address)
        return SocketServer.TCPServer.finish_request(self, request, client_address)

    def close_request(self, request_address):
        self.logger.debug('close_request(%s)', request_address)
        return SocketServer.TCPServer.close_request(self, request_address)

if __name__ == "__main__":
    HOST, PORT = "192.168.1.111", 9999
    address = (HOST, PORT)

    # Create the server, binding to localhost on port 9999
    server = myServer((HOST, PORT), TCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

    logger = logging.getLogger('client')
    logger.info('Server on %s:%s', ip, port)