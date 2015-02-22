from flask import Flask, request
from flask import render_template, redirect
from jinja2 import Template
import RPi.GPIO as GPIO
import time
import json

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
  return True

def cutOffLED():
  GPIO.output(outputPin, False)
  return False
  
def cleanUp():
  cutOffLED()
  GPIO.cleanup() #cleanup all gpio

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
  print "/ LED isOn = " + str(isOn)
  return render_template('index.html', isOn=isOn)

@app.route("/LEDinfo", methods=['POST', 'GET'])
def LEDinfo():
  global isOn
  isOn = request.form.get('LED')
#  print ledIsOn
#  print "\n\n" 
#  print request.__dict__ 
#  print "\n\n"
#  print request.environ['werkzeug.request'].__dict__
#  print "\n\n"
# if request.form['LED'] == "ON":
  if isOn == False:
    isOn = cutOnLED()
# if request.form['LED'] == "OFF":
  elif isOn == True: 
    isOn = cutOffLED()
  else:
    print "Got an unexepected request @ /LEDinfo."
  print "The light is " + str(isOn)
  return redirect('/')
# 
# 
# @app.errorhandler(400)
# def page_not_found(error):
    
#     return render_template('page_not_found.html'), 400
# 
# 
if __name__ == "__main__": 
  app.debug = True
  app.run("0.0.0.0")

  print "\n\n\nServer Run Complete."
  GPIO.cleanup()
  print "GPIO Cleanup Complete"
