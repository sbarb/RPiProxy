from flask import Flask, request
from flask import render_template, redirect
from jinja2 import Template
import RPi.GPIO as GPIO
import time

isOn = False
outputPin = 7
doneStr = ""

#setup gpio pinout using BOARD numbering
GPIO.setmode(GPIO.BOARD)
#ignore warnings
GPIO.setwarnings(False)
#setup pin for output
GPIO.setup(outputPin, GPIO.OUT)

def cutOnLED():
  GPIO.output(outputPin, True)
  isOn = True
  print "Going ON"
  return True

def cutOffLED():
  GPIO.output(outputPin, False)
  isOn = False
  print "Going OFF"
  return False
  
def cleanUp():
  cutOffLED()
  GPIO.cleanup() #cleanup all gpio

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
  global isOn
  isOn = (not isOn)
  print "/ LED isOn = " + str(isOn)
  return render_template('index.html', isOn=isOn)

@app.route("/LEDinfo", methods=['POST'])
def LEDinfo():
  if request.form['LED'] == "ON":
    cutOnLED()
  elif request.form['LED'] == "OFF":
    cutOffLED()
  else:
    print "Got an unexepected request @ /LEDinfo."

  #print "/LEDinfo LED isOn = {}".format(isOn)
  return redirect('/')
  
if __name__ == "__main__":
  app.debug = True
  app.run("0.0.0.0")

  print "\n\n\nServer Run Complete."
  GPIO.cleanup()
  print "GPIO Cleanup Complete"
