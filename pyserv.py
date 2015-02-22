from flask import Flask, request, render_template, redirect
from jinja2 import Template
import RPi.GPIO as GPIO
import time

isOn = False
light = 7

#setup gpio pinout using BOARD numbering
GPIO.setmode(GPIO.BOARD)
#ignore warnings
GPIO.setwarnings(False)
#setup pin for output
GPIO.setup(light, GPIO.OUT)

def writeHigh(pin):
  GPIO.output(pin, True)
  return True

def writeLow(pin):
  GPIO.output(pin, False)
  return False
  
def cleanUp():
  if !isOn:
    writeLow(light) # cut light off
  GPIO.cleanup() # cleanup all gpio 

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
  print "/ LED isOn = " + str(isOn)
  return render_template('index.html', isOn=isOn)

@app.route("/LEDinfo", methods=['POST', 'GET'])
def LEDinfo():
  global isOn
  ledIsOn = request.form.get('LED')

  if ledIsOn == "ON":
    isOn = writeHigh(light)
  elif ledIsOn == "OFF": 
    isOn = writeLow(light)
  else:
    print "Got an unexepected request @ /LEDinfo."
  
  print ledIsOn
  return redirect('/')

if __name__ == "__main__": 
  try:
    app.debug = True
    app.run("0.0.0.0")

  except (KeyboardInterrupt, SystemExit):
    print "\n\n\nServer Run Complete."
    cleanUp()
    print "GPIO Cleanup Complete"
