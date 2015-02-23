from collections import OrderedDict
from flask import Flask, request, render_template, redirect
import os

# helper functions
def notAPi(body):
    print "This is not a running on a pi. Skipping a pi feature: " + body

def makeDebugString(pin_tuple):
    return "/ "+ pin_tuple[0] +" = " + pin_tuple[1]

def toBoolean(boolStr):
    if str(boolStr) == "1":
        return True
    elif str(boolStr) == "0":
        return False
    else:
        return None

# Configure if the program is running as a Raspberry pi
# expected value is 0 or 1
if 'PI' in os.environ:
    isPi = toBoolean(os.environ['PI'])
else:
    isPi = False

if isPi:
    import RPi.GPIO as GPIO

# mapping of physical pin (and human readable name) to the internal GPIO pin numbering
# ie: {name: data}
_unordered_pins = {
  'pin1': { 'pin': 7, 'state': False, 'weight': 1 },
  'pin2': { 'pin': 11, 'state': False, 'weight': 2 },
  'pin3': { 'pin': 13, 'state': False, 'weight': 3 },
  'pin4': { 'pin': 15, 'state': False, 'weight': 4 },
  'pin5': { 'pin': 12, 'state': False, 'weight': 5 },
  'pin6': { 'pin': 16, 'state': False, 'weight': 6 },
  'pin7': { 'pin': 18, 'state': False, 'weight': 7 },
  'pin8': { 'pin': 22, 'state': False, 'weight': 8 },
  'pin9': { 'pin': 24, 'state': False, 'weight': 9 },
  'pin10': { 'pin': 26, 'state': False, 'weight': 10 },
  'pin11': { 'pin': 19, 'state': False, 'weight': 11 }
}
# guarantees order during iteration based on the weight key
pins = OrderedDict(sorted(_unordered_pins.items(), key=lambda t: t[1]['weight']))

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

def writeHigh(pinName):
    writePin(pinName, True)

def writeLow(pinName):
    writePin(pinName, False)
  
def cleanUp():
    global pins
    # turn off all the pins
    writeAll(False)
    GPIO.cleanup() # cleanup all gpio 

def writeAll(state):
    for name, data in pins.iteritems():
        if pins[name]['state'] not state:
            writePin(data['pin'], state)
            pins[name]['state'] = state

# Define the flask application
app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    # list of pin name and state as a string ("pin1", "True")
    pins_info = [(name, str(data['state'])) for name, data in pins.iteritems()]
    # transform into a list of strings
    pin_strings = [makeDebugString(pin_obj) for pin_obj in pins_info]
    # print the strings one line at a time
    print "\n".join(pin_strings)
    return render_template('index.html', pins=pins)

@app.route("/LEDinfo", methods=['POST', 'GET'])
def LEDinfo():
    # iterate through list of fields in the submitted form
    for pinName in request.form.keys():
        # check if the name of the field is one of the defined pins
        if pinName not in pins:
            print "Someone attempted to do something other than toggle a pin."
            continue # skip this one
        # deal with the request
        value = request.form.get(pinName)
        writePin(pinName, toBoolean(value))
    return redirect('/')

if __name__ == "__main__": 
  try:
    initPi()
    app.debug = True
    app.run("0.0.0.0")
    raise KeyboardInterrupt

  finally:
    print "\n\n\nServer Run Complete."
    cleanUp()
    print "GPIO Cleanup Complete"
