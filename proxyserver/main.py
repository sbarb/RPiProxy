import socket
import sys
from PinsConfig import PinsMap as PinsMap
import errno
from flask import Flask, request, render_template, redirect, jsonify
def makeDebugString(pin_tuple):
    return "/ "+ pin_tuple[0] +" = " + pin_tuple[1]

def toBoolean(boolStr):
    if str(boolStr) == "1":
        return True
    elif str(boolStr) == "0":
        return False
    else:
        return None

def updatePins(inputReceived):
    global PinsMap
    commands = inputReceived.split('|')
    for command in commands:
        try:
            pinName, state = command.split(" ")
            state = toBoolean(state)
            PinsMap[pinName]['state'] = state
            print "Changed {}".format(pinName, state)
            print "Received: {}".format(command)
        except:
            print "\n\ninputReceived = " + command

HOST, PORT = "192.168.1.111", 9999
# HOST, PORT = "127.0.0.1", 9999

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((HOST, PORT))
except Exception as e:
    print "Failed to connect to socket server"
    raise e

# Define the flask application
app = Flask(__name__)

@app.route('/state', methods=["GET"])
def state():
    return jsonify(PinsMap)

@app.route("/", methods=['GET'])
def index():
    # list of pin name and state as a string ("pin1", "True")
    pins_info = [(name, str(data['state'])) for name, data in PinsMap.iteritems()]
    # transform into a list of strings
    pin_strings = [makeDebugString(pin_obj) for pin_obj in pins_info]
    # print the strings one line at a time
    print "\n".join(pin_strings)
    return render_template('index.html', pins=PinsMap)

@app.route("/LEDinfo", methods=['POST', 'GET'])
def LEDinfo():
    global sock
    # iterate through list of fields in the submitted form
    commands = []
    for pinName in request.form.keys():
        # check if the name of the field is one of the defined pins
        if pinName not in PinsMap:
            print "Someone attempted to do something other than toggle a pin."
            continue # skip this one
        # deal with the request
        state = request.form.get(pinName)
        command = " ".join([str(pinName), str(state)])
        commands.append(command)
    data = "|".join(commands)
    try:
        # connection established, send some stuff
        print "data = " + data
        sock.sendall(data + "\n")
        print "Sent " + data
        received = sock.recv(2048)
        # update the client
        updatePins(received)
        print 'received:', received
        
    except socket.error, v:
        errorcode=v[0]
        if errorcode == errno.ECONNREFUSED:
            print "Connection Refused"
        elif errorcode == errno.EPIPE: 
            print "Broken Pipe"
    finally:
        return redirect('/')


    return redirect('/')

if __name__ == "__main__": 
  try:
    # app.debug = True
    app.run("0.0.0.0")
  except KeyboardInterrupt as stop:
    print "\nClosing Socket."
    sock.close()
    print "\n\n\nServer Run Complete."


