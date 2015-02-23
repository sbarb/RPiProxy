from flask import Flask, request, render_template, redirect
from jinja2 import Template
import RPi.GPIO as GPIO
import time

isOn1 = False
isOn2 = False
isOn3 = False
isOn4 = False
pin1 = 7
pin2 = 11
pin3 = 13
pin4 = 15

#setup gpio pinout using BOARD numbering
GPIO.setmode(GPIO.BOARD)
#ignore warnings
GPIO.setwarnings(False)
#setup pin for output
GPIO.setup(pin1, GPIO.OUT)
GPIO.setup(pin2, GPIO.OUT)
GPIO.setup(pin3, GPIO.OUT)
GPIO.setup(pin4, GPIO.OUT)

def writeHigh(pin):
  GPIO.output(pin, True)
  return True

def writeLow(pin):
  GPIO.output(pin, False)
  return False
  
def cleanUp():
  if isOn1:
    writeLow(pin1) # cut pin1 off
  elif isOn2:
    writeLow(pin2) # cut pin2 off
  elif isOn3:
    writeLow(pin3) # cut pin3 off
  elif isOn4:
    writeLow(pin4) # cut pin4 off
  GPIO.cleanup() # cleanup all gpio 

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
  print "/ Lamp = pin1 = " + str(isOn1)
  print "/ LED 1 = pin2 = " + str(isOn2)
  print "/ LED 2 = pin3 = " + str(isOn3)
  print "/ LED 3 = pin4 = " + str(isOn4)
  return render_template('index.html', isOn1=isOn1, isOn2=isOn2, isOn3=isOn3, isOn4=isOn4)

@app.route("/LEDinfo", methods=['POST', 'GET'])
def LEDinfo():
  global isOn1, isOn2, isOn3, isOn4
  pin1IsOn = request.form.get('lamp')
  pin2IsOn = request.form.get('led1')
  pin3IsOn = request.form.get('led2')
  pin4IsOn = request.form.get('led3')
  
  if pin1IsOn == "ON": 
    isOn1 = writeHigh(pin1)
  elif pin1IsOn == "OFF": 
    isOn1 = writeLow(pin1)

  elif pin2IsOn == "ON":
    isOn2 = writeHigh(pin2)
  elif pin2IsOn == "OFF": 
    isOn2 = writeLow(pin2)

  elif pin3IsOn == "ON":
    isOn3 = writeHigh(pin3)
  elif pin3IsOn == "OFF": 
    isOn3 = writeLow(pin3)

  elif pin4IsOn == "ON":
    isOn4 = writeHigh(pin4)
  elif pin4IsOn == "OFF": 
    isOn4 = writeLow(pin4)

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


