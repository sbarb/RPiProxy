import logging
import sys
import SocketServer
from collections import OrderedDict
import os

logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                    )
   
############################################
# Pi helper functions
# mapping of physical pin (and human readable name) to the internal GPIO pin numbering
# ie: {name: data}
_unordered_pins = {
  'pin1': { 'pin': 7, 'name' : 'Lamp', 'state': False, 'weight': 1 },
  'pin2': { 'pin': 11, 'name' : 'LED 1', 'state': False, 'weight': 2 },
  'pin3': { 'pin': 13, 'name' : 'LED 2', 'state': False, 'weight': 3 },
  'pin4': { 'pin': 15, 'name' : 'LED 3', 'state': False, 'weight': 4 },
  'pin5': { 'pin': 12, 'name' : 'LED 4', 'state': False, 'weight': 5 },
  'pin6': { 'pin': 16, 'name' : 'LED 5', 'state': False, 'weight': 6 },
  'pin7': { 'pin': 18, 'name' : 'LED 6', 'state': False, 'weight': 7 },
  'pin8': { 'pin': 22, 'name' : 'LED 7', 'state': False, 'weight': 8 },
  'pin9': { 'pin': 24, 'name' : 'LED 8', 'state': False, 'weight': 9 },
  'pin10': { 'pin': 26, 'name' : 'LED 9', 'state': False, 'weight': 10 },
  'pin11': { 'pin': 19, 'name' : 'LED 10', 'state': False, 'weight': 11 }
}
# guarantees order during iteration based on the weight key
pins = OrderedDict(sorted(_unordered_pins.items(), key=lambda t: t[1]['weight']))
# determins if the host is a RPi or not
def notAPi(body):
    print "This is not a running on a pi. Skipping a pi feature: " + body

def makeDebugString(pin_tuple):
    return "/ "+ pin_tuple[0] +" = " + pin_tuple[1]
# converts string '1' or '0' to bool True or False
def toBoolean(boolStr):
    if str(boolStr) == "1":
        return True
    elif str(boolStr) == "0":
        return False
    else: # Any input that is not '1' or '0' will return None
        return None
# Tell 'pinName' to be in state 'state'
def writePin(pinName, state):
    if state is None:
        print "Not doing anything. Someone requesting something absurd."
        return
    global pins
    # updates global state
    pins[pinName]['state'] = state
    if not isPi:
        notAPi("Write " + str(state) + " on pin "+pinName+" #" + str(pins[pinName]['pin']))
        return
    GPIO.output(pins[pinName]['pin'], state)
# Write High for 'pinName'
def writeHigh(pinName):
    writePin(pinName, True)
# Write Low for 'pinName'
def writeLow(pinName):
    writePin(pinName, False)
# Write 'state' for ALL pins
def writeAll(state):
    for name, data in pins.iteritems():
        # if data['state'] != state:
        writePin(name, state)
# Cut off and cleanup (remove) all gpio pins 
def cleanUp():
    global pins
    # turn off all the pins
    writeAll(False)
    GPIO.cleanup() # cleanup all gpio 
# If this host is a RPi this will initialize the gpio pins
# and set start the program with all pins OFF
def initPi():
    if not isPi:
        notAPi("init pi")
        return
    #setup gpio pinout using BOARD numbering
    GPIO.setmode(GPIO.BOARD)
    #ignore warnings
    GPIO.setwarnings(False)
    #setup pin for output
    for name, data in pins.iteritems():
        GPIO.setup(data['pin'], GPIO.OUT)
    writeAll(False)

# Configure if the program is running as a Raspberry pi
# expected value is 0 or 1
#### this is where the environment variable is processed
if 'PI' in os.environ:
    isPi = toBoolean(os.environ['PI'])
else:
    isPi = False

if isPi:
    import RPi.GPIO as GPIO
    initPi()
# End Pi helper functions
############################################
# socket data helper functions
class TCPHandler(SocketServer.StreamRequestHandler):

    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger('TCPHandler')
        self.logger.debug('__init__')
        SocketServer.StreamRequestHandler.__init__(self, request, client_address, server)
        return

    def setup(self):
        self.logger.debug('setup')
        return SocketServer.StreamRequestHandler.setup(self)

    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        # self.data = self.rfile.readline().strip()
        
        # get input with wait if no data

        if (len(self.data)==self.BUFFER_SIZE):
            while 1:
                try: #error means no more data
                    pinName = self.data.split(" ")[0]
                    state = self.data.split(" ")[1]
                    data += self.request.recv(self.BUFFER_SIZE, socket.MSG_DONTWAIT)
                except:
                    break
        print "{} wrote:".format(self.client_address[0])
        print self.data
        print "Pin Name {}".format(pinName)
        print "State {}".format(state)
        # Likewise, self.wfile is a file-like object used to write back
        # to the client
        self.wfile.write(self.data)
        if pinName in pins:
            print "***IF EXECUTED***"
            self.wfile.write(pinName)
            self.wfile.write(state)
            self.wfile.write(pins)
            writePin(pinName, toBoolean(state))
        elif str(pinName) in ("all", "ALL", "All", "aLL", "alL", "aLl"):
            print "***ELIF (ALL) EXECUTED***"
            self.wfile.write(pinName)
            self.wfile.write(state)
            writeAll(toBoolean(state))
        else:
            print "*** SOMETHING ISN'T RIGHT ***"
    def finish(self):
        self.logger.debug('finish')
        return SocketServer.StreamRequestHandler.finish(self)
# End socket data helper functions
############################################
# socket functions
class SocketHandler(SocketServer.TCPServer):
    
    def __init__(self, server_address, handler_class=TCPHandler):
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
# End socket functions

############################################

# set the socket host and port addresses
socketHost, socketPort = "192.168.1.111", 9999
address = (socketHost, socketPort)

# Create the server, binding to socketHost on socketPort 
socketServer = SocketHandler(address, TCPHandler)

# Start the program
if __name__ == "__main__":
    global socketServer
    try:
        logger = logging.getLogger('client')
        logger.info('Socket Server running on %s:%s', socketHost, socketPort)

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        socketServer.serve_forever()

        # list of pin name and state as a string ("pin1", "True")
        pins_info = [(name, str(data['state'])) for name, data in pins.iteritems()]
        # transform into a list of strings
        pin_strings = [makeDebugString(pin_obj) for pin_obj in pins_info]
        # print the strings one line at a time
        print "\n".join(pin_strings)
        # raise KeyboardInterrupt    
    except KeyboardInterrupt as stop:    
        print "\nClosing Socket."
        # close the socket
        socketServer.socket.close()
        print "\n\n\nServer Run Complete."
    