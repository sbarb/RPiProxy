import SocketServer
from GPIOTCPHandler import GPIOTCPHandler
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                    )

# set the socket host and port addresses
# SOCKET_HOST, SOCKET_PORT = "192.168.1.111", 9999
SOCKET_HOST = "127.0.0.1"
SOCKET_PORT = 9999

# EntryPoint to the program
if __name__ == "__main__":
    
    # Create the server, binding to SOCKET_HOST on SOCKET_PORT 
    PiSocketServer = SocketServer.TCPServer((SOCKET_HOST, SOCKET_PORT), GPIOTCPHandler)

    logger = logging.getLogger('Socket Server')
    logger.info('Socket Server running on %s:%s', SOCKET_HOST, SOCKET_PORT)
    try:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        PiSocketServer.serve_forever()
    except KeyboardInterrupt as stop:    
        print "\nClosing Socket."
        # close the socket
        PiSocketServer.socket.close()
        # shutdown the server
        PiSocketServer.shutdown()
        print "\n\n\n"
        logger.info("Server Run Complete.")
    