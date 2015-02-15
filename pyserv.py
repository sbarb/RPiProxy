from flask import Flask, request
from flask import render_template, redirect
from jinja2 import Template
import RPi.GPIO as GPIO
import time

isOn = "OFF"
notIsOn = "ON"
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
	print "Going ON"
	return True

def cutOffLED():
	GPIO.output(outputPin, False)
	print "Going OFF"
	return False
	
def cleanUp():
	cutOffLED()
	GPIO.cleanup() #cleanup all gpio

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
	print isOn
	return render_template('index.html', isOn=isOn, notIsOn=notIsOn)

@app.route("/LEDinfo", methods=['POST'])
def LEDinfo():
	if request.form['LED'] == "ON":
		isOn = True
		notIsOn = "OFF"
		cutOnLED()
	elif request.form['LED'] == "OFF":
		isOn = False
		notIsOn = "ON"
		cutOffLED()
		
	print "LED = ", isOn
	#print notIsOn
	return redirect('/')
	
if __name__ == "__main__":
	app.debug=True
	app.run("0.0.0.0")


	
print "\n\n\nDone"

GPIO.cleanup()