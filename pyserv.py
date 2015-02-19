from flask import Flask, request
from flask import render_template, redirect
from jinja2 import Template
import RPi.GPIO as GPIO
import time
import json

isOn = False
outputPin = 7
doneStr = ""
err = None

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
  global err
  print "/ LED isOn = " + str(isOn)
  return render_template('index.html', isOn=isOn, error=err)

@app.route("/LEDinfo", methods=['POST', 'GET'])
def LEDinfo():
  global isOn, err
  button = json.dumps(request.form['LED']) # request.args.get('LED', '')
  # if request.form['LED'] == "ON":
  print "button = " + button
  if button == "ON":
    isOn = cutOnLED()
  elif button == "OFF":
    isOn = cutOffLED()
  else:
    print "Got an unexepected request @ /LEDinfo."
    err = "BAD REQUEST!!!"
  
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
