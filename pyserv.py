from flask import Flask, request, render_template, redirect
from jinja2 import Template
import RPi.GPIO as GPIO
import time

isOnLamp = False
isOnLed = False
isOn2Led = False
isOn3Led = False
light = 7
led = 11
led2 = 13
led3 = 15

#setup gpio pinout using BOARD numbering
GPIO.setmode(GPIO.BOARD)
#ignore warnings
GPIO.setwarnings(False)
#setup pin for output
GPIO.setup(light, GPIO.OUT)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
GPIO.setup(led3, GPIO.OUT)

def writeHigh(pin):
  GPIO.output(pin, True)
  return True

def writeLow(pin):
  GPIO.output(pin, False)
  return False
  
def cleanUp():
  if isOnLamp:
    writeLow(light) # cut light off
  elif isOnLed:
    writeLow(led) # cut led off
  elif isOn2Led:
    writeLow(led2) # cut led2 off
  elif isOn3Led:
    writeLow(led3) # cut led3 off
  GPIO.cleanup() # cleanup all gpio 

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
  print "/ Light isOn = " + str(isOnLamp)
  print "/ LED isOn = " + str(isOnLed)
  print "/ LED 3 isOn = " + str(isOn2Led)
  print "/ LED 3 isOn = " + str(isOn3Led)
  return render_template('index.html', isOnLamp=isOnLamp, isOnLed=isOnLed, isOn2Led=isOn2Led, isOn3Led=isOn3Led)

@app.route("/LEDinfo", methods=['POST', 'GET'])
def LEDinfo():
  global isOnLamp, isOnLed, isOnLed2, isOnLed3
  lampIsOn = request.form.get('Lamp')
  ledIsOn = request.form.get('LED')
  ledIsOn2 = request.form.get('LED2')
  ledIsOn2 = request.form.get('LED3')
  # print "Going " + ledIsOn

  if lampIsOn == "ON": 
    isOnLamp = writeHigh(light)
  elif lampIsOn == "OFF": 
    isOnLamp = writeLow(light)

  elif ledIsOn == "ON":
    isOnLed = writeHigh(led)
  elif ledIsOn == "OFF": 
    isOnLed = writeLow(led)

  elif ledIsOn2 == "ON":
    is2OnLed = writeHigh(led2)
  elif ledIsOn2 == "OFF": 
    is2OnLed = writeLow(led2)

  elif ledIsOn3 == "ON":
    is3OnLed = writeHigh(led3)
  elif ledIsOn3 == "OFF": 
    is3OnLed = writeLow(led3)

  else:
    print "Got an unexepected request."
  
  # print ledIsOn
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
