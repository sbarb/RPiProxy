import SocketServer
from PinsConfig import PinNames
from MyPi import MyPi
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                    )
logger = logging.getLogger('GPIOTCPHandler')
# http://stackoverflow.com/questions/6792803/finding-all-possible-case-permutations-in-python
# get all possible permuations of the capitalization of a string
def all_casings(input_string):
    if not input_string:
        yield ""
    else:
        first = input_string[:1]
        if first.lower() == first.upper():
            for sub_casing in all_casings(input_string[1:]):
                yield first + sub_casing
        else:
            for sub_casing in all_casings(input_string[1:]):
                yield first.lower() + sub_casing
                yield first.upper() + sub_casing

pi = MyPi()
# socket request handler
# Handle incoming TCPRequests
class GPIOTCPHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        # read the next line and remove surrounding whitespace
        while 1:
            self.data = self.rfile.readline().strip()
            # TODO: check if self.data is a "done" signal.
            if self.data == "TURN_OFF":
                pass
            print "data", self.data
            for command in self.data.split("|"):
                pinName, state = command.split(" ")
                print pinName, state
                state = MyPi.toBoolean(state)
                print "{} wrote:".format(self.client_address[0])
                print "Pin Name {}".format(pinName)
                print "State {}".format(state)
                if pinName in PinNames:
                    logger.debug("***IF EXECUTED***")
                    pi.writePin(pinName, state)
                elif pinName in all_casings("all"):
                    logger.debug("***ELIF (ALL) EXECUTED***")
                    pi.writeAll(state)
                else:
                    logger.error("*** SOMETHING ISN'T RIGHT ***")
                
            # Likewise, self.wfile is a file-like object used to 
            # write back to the client
            # Echo back the request to the client on completion
            self.wfile.write(self.data)
