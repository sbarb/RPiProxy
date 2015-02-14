from flask import Flask 
from flask import render_template
import RPi.GPIO as GPIO
import time

isOn = False
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
	return render_template('index.html')
	
if __name__ == "__main__":
	app.debug=True
	app.run("0.0.0.0")
	
print "\n\n\nDone"

GPIO.cleanup()