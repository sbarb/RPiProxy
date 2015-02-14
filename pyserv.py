from flask import Flask, request
from flask import render_template
from jinja2 import Template
import RPi.GPIO as GPIO
import time

isOn = "OFF"
notIsOn = "ON"
output = 7
doneStr = ""

#setup gpio pinout using BOARD numbering
GPIO.setmode(GPIO.BOARD)
#ignore warnings
GPIO.setwarnings(False)
#setup pin for output
GPIO.setup(output, GPIO.OUT)

def cutOnLED():
	GPIO.output(output, True)
	print "Going ON"
	return True

def cutOffLED():
	GPIO.output(output, False)
	print "Going OFF"
	return False
def cleanUp():
	cutOffLED()
	GPIO.cleanup() #cleanup all gpio
	
#try:
#	while (doneStr != 'stop'):
#		doneStr = str(raw_input("Turn light on?\t"))
#		if doneStr in ['Y', 'y', 'YES', 'Yes', 'yes']:
#			isOn = cutOnLED()
#      
#		doneStr = str(raw_input("Enter stop to exit...\nTurn light off?	"))
#		if doneStr in ['Y', 'y', 'YES', 'Yes', 'yes']:
#			isOn = cutOffLED()
#	
#except KeyboardInterrupt:
#	cleanUp()

app = Flask(__name__)

@app.route("/")
def index():
	return render_template('index.html', isOn=isOn, notIsOn=notIsOn)

@app.route("/LEDinfo", methods=['POST'])
def LEDinfo():
	isOn = request.form['LED']
	if isOn == "ON":
		notIsOn = "OFF"
	elif isOn == "OFF":
		notIsOn = "ON"
		
	print "LED = ", isOn
		
	if request.form['LED'] == "ON":
		isOn = "ON"
		notIsOn = "OFF"
		cutOnLED()
	elif request.form['LED'] == "OOFF":
		isOn = "OFF"
		notIsOn = "ON"
		cutOffLED()

	return render_template('index.html', isOn=isOn, notIsOn=notIsOn)
	
if __name__ == "__main__":
	app.debug=True
	app.run("0.0.0.0")
	
print "\n\n\nDone"

# GPIO.cleanup()