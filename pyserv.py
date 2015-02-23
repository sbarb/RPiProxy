from flask import Flask, request, render_template, redirect
from jinja2 import Template
import RPi.GPIO as GPIO
import time

isOnLight = False
isOnLed = False
light = 7
led = 11

#setup gpio pinout using BOARD numbering
GPIO.setmode(GPIO.BOARD)
#ignore warnings
GPIO.setwarnings(False)
#setup pin for output
GPIO.setup(light, GPIO.OUT)
GPIO.setup(led, GPIO.OUT)

def writeHigh(pin):
  GPIO.output(pin, True)
  return True

def writeLow(pin):
  GPIO.output(pin, False)
  return False
  
def cleanUp():
  if isOn:
    writeLow(light) # cut light off
  GPIO.cleanup() # cleanup all gpio 

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
  print "/ Light isOn = " + str(isOnLight)
  print "/ LED isOn = " + str(isOnLed)
  return render_template('index.html', isOnLight=isOnLight, isOnLed=isOnLed)

@app.route("/LEDinfo", methods=['POST', 'GET'])
def LEDinfo():
  global isOnLight, isOnLed
  lampIsOn = request.form.get('Lamp')
  ledIsOn = request.form.get('LED')
  print "Going " + ledIsOn

  if lampIsOn == "ON": 
    isOnLight = writeLow(light)
  elif lampIsOn == "OFF": 
    isOnLight = writeLow(light)
  elif ledIsOn == "ON":
    isOnLed = writeHigh(led)
  elif ledIsOn == "OFF": 
    isOnLed = writeLow(led)
  else:
    print "Got an unexepected request."
  
  print ledIsOn
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
