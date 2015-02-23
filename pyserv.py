from flask import Flask, request, render_template, redirect
import RPi.GPIO as GPIO
# TODO: rename HTML form names to pins' keys

# Configure if the program is running as a Raspberry pi
isPi = False # TODO: do env var

# mapping of physical pin (and human readable name) to the internal GPIO pin numbering
# ie: {name: data}
pins = {
  'pin1': { 'pin': 7, 'state': False },
  'pin2': { 'pin': 11, 'state': False },
  'pin3': { 'pin': 13, 'state': False },
  'pin4': { 'pin': 15, 'state': False }
}

# helper function
def notAPi(body):
    print "This is not a running on a pi. Skipping a pi feature: " + body

def makeDebugString(pin_tuple):
    return "/ "+ pin_tuple[0] +" = " + pin_tuple[1]

def toBoolean(boolStr):
    if boolStr == "1":
        return True
    elif boolStr == "0":
        return False
    else
        return None

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
        GPIO.setup(data.pin, GPIO.OUT)

def writePin(pinName, state):
    if state is None:
        print "Not doing anything. Someone requesting something absurd."
        return
    global pins
    # updates global state
    pins[pinName].state = state
    if not isPi:
        notAPi("Write " + str(state) + " on pin "+pinName+" #" + str(pinName.pin))
        return
    GPIO.output(pin, state)

def writeHigh(pinName):
    writePin(pinName, True)

def writeLow(pinName):
    writePin(pinName, False)
  
def cleanUp():
    global pins
    # turn off all the pins
    for name, data in pins.iteritems():
        if data.state
            writeLow(data.pin, GPIO.OUT)
            pins[name].state = False
    GPIO.cleanup() # cleanup all gpio 

# Define the flask application
app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    # tuple of pin name and state as a string ("pin1", "True")
    pins_info = (name, str(data.state) for name, data in pins.iteritems())
    # transform into a list of strings
    pin_strings = map(pins_info, makeDebugString)
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
        else:
            print "Got an unexepected request."  
    return redirect('/')

if __name__ == "__main__": 
  try:
    app.debug = True
    app.run("0.0.0.0")
    raise KeyboardInterrupt

  finally:
    print "\n\n\nServer Run Complete."
    cleanUp()
    print "GPIO Cleanup Complete"
