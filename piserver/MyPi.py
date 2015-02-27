import os
from PinsConfig import PinsMap as PinsMap
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                    )
# Configure if the program is running as a Raspberry pi
# expected value is 0 or 1
# NOTE: this is where the environment variable is processed
if 'PI' in os.environ:
    IS_PI = True if os.environ['PI'] is "1" 
    import RPi.GPIO as GPIO
else:
    IS_PI = False

class MyPi(object):
    @staticmethod
    def isPi():
        return IS_PI

    @staticmethod
    # converts string '1' or '0' to bool True or False
    def toBoolean(boolStr):
        if str(boolStr) == "1":
            return True
        elif str(boolStr) == "0":
            return False
        else: # Any input that is not '1' or '0' will return None
            return None

    @staticmethod
    def makeDebugString(pin_tuple):
        return "/ "+ pin_tuple[0] +" = " + pin_tuple[1]

    @staticmethod
    def notAPi(body):
        print "This is not a running on a pi. Skipping a pi feature: " + body

    def __init__(self):
        # If this host is a RPi this will initialize the gpio PinsMap
        # and set start the program with all PinsMap OFF
        self.logger = logging.getLogger('MyPi')
        if not MyPi.isPi():
            MyPi.notAPi("init pi")
            return

        #setup gpio pinout using BOARD numbering
        GPIO.setmode(GPIO.BOARD)
        #ignore warnings
        GPIO.setwarnings(False)
        #setup pin for output
        for name, data in PinsMap.iteritems():
            GPIO.setup(data['pin'], GPIO.OUT)
        self.writeAll(False)

    # Tell 'pinName' to be in state 'state'
    def writePin(self, pinName, state):
        if state is None:
            self.logger.info("Not doing anything. Someone requesting something absurd.")
            return
        global PinsMap
        # updates global state
        PinsMap[pinName]['state'] = state
        if not MyPi.isPi():
            MyPi.notAPi("Write " + str(state) + " on pin "+pinName+" " + str(PinsMap[pinName]['name']))
            return
        GPIO.output(PinsMap[pinName]['pin'], state)
    
    # Deprecated
    # Write High for 'pinName'
    def writeHigh(self, pinName):
        self.writePin(pinName, True)
    
    # Deprecated
    # Write Low for 'pinName'
    def writeLow(self, pinName):
        self.writePin(pinName, False)
    
    # Write 'state' for ALL PinsMap
    def writeAll(self, state):
        for name, data in PinsMap.iteritems():
            # if data['state'] != state:
            self.writePin(name, state)

    # Cut off and cleanup (remove) all gpio PinsMap 
    def cleanUp(self):
        # turn off all the PinsMap
        self.writeAll(False)
        GPIO.cleanup() # cleanup all gpio 
