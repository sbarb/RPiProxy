import requests as R
from time import sleep
from random import choice
import socket
# On Pi this is the HOST and PORT
HOST, PORT = "192.168.1.111", 9999
# On a local dev box
# HOST, PORT = "127.0.0.1", 9999

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((HOST, PORT))
except Exception as e:
    print "Failed to connect to socket server"
    raise e
# The Pi's ip for the Flask Server
URL = 'http://108.178.248.104/LEDinfo'
# Local Flask Server
# URL = 'http://localhost:5000/LEDinfo'
# state should be 0 or 1
def l(state=0):
  state = str(state)
  return {"pin1": state}
def q(state=0):
  state = str(state)
  return {"pin2": state}
def w(state=0):
  state = str(state)
  return {"pin3": state}
def e(state=0):
  state = str(state)
  return {"pin4": state}
def r(state=0):
  state = str(state)
  return {"pin5": state}
def t(state=0):
  state = str(state)
  return {"pin6": state}
def y(state=0):
  state = str(state)
  return {"pin7": state}
def u(state=0):
  state = str(state)
  return {"pin8": state}
def i(state=0):
  state = str(state)
  return {"pin9": state}
def o(state=0):
  state = str(state)
  return {"pin10": state}
def p(state=0):
  state = str(state)
  return {"pin11": state}

def _(*args):
  data = dict(obj.items()[0] for obj in args)
  # # HTTP
  # R.post(URL, data=data)
  # end HTTP
  # Socket
  commands = []
  for k, v in data.iteritems():
    commands.append(k+" "+v)
  command_str = "|".join(commands)
  print command_str
  sock.sendall(command_str+"\n")
  r = sock.recv(2048)
  print "received", r
  # end Socket
  return sleep

def all(state):
  return [q(state), w(state), e(state), r(state), t(state), y(state), u(state), i(state), o(state), p(state)]

def each():
  return [q,w,e,r,t,y,u,i,o,p]

def pulsate(times, frequency=0.01):
  if times < 1:
    return True
  for fn in each():
    _(fn(1))(frequency)
  for fn in each():
    _(fn(0))(frequency)
  pulsate(times-1, frequency)

def snake(times, frequency=0.01):
  if times < 1:
    return True
  lights = each()
  for fn in lights:
    _(fn(1))(frequency)
  _(q(0))(frequency)
  for i, current in enumerate(lights):
    if i+1 < len(lights):
      next = lights[i+1]
    else:
      next = lights[0]
    _(current(1), next(0))(frequency)
  snake(times-1, frequency)

def rando(times, frequency=0.5):
  if times < 1:
    return True
  data = []
  # do one random choice per light
  for thing in each():
    c = choice([1, 0])
    data.append(thing(c))
  _(*data)(frequency)
  rando(times-1, frequency)

def outsideIn(times, frequency=0.1):
  if times < 1:
    return True
  lights = each()
  length = len(lights)
  for leftIndex, left in enumerate(lights):
    rightIndex = length-1-leftIndex
    if rightIndex < leftIndex:
      break
    right = lights[rightIndex]
    polarity = 1
    _(left(polarity), right(polarity))(frequency)

  for leftIndex, left in enumerate(lights):
    rightIndex = length-1-leftIndex
    right = lights[rightIndex]
    polarity = 0
    _(left(polarity), right(polarity))(frequency)

  outsideIn(times-1, frequency)

def inAndOut(times, frequency=0.1):
  if times < 1:
    return True
  lights = each()
  length = len(lights)
  for leftIndex, left in enumerate(lights):
    rightIndex = length-1-leftIndex
    right = lights[rightIndex]
    polarity = 1
    if leftIndex > rightIndex:
      polarity=0
    _(left(polarity), right(polarity))(frequency)
  inAndOut(times-1, frequency)

def flicker(times, frequency=0.1):
  if times < 1:
    return True
  _(*all(1))(frequency)  
  _(*all(0))(frequency)
  flicker(times-1, frequency)

flicker(3, 0.05)
# animations = [rando, pulsate, snake, outsideIn, inAndOut]
# frequencies = [0.01, 0.005, 0.05]
# nums = list(range(5, 10))
# for i in range(0, 30):
#   animation = choice(animations)
#   num = choice(nums)
#   freq = choice(frequencies)
#   print animation, num, freq
#   animation(5, 0.05)

rando(10, 0.001)
pulsate(3, .005)
snake(10, 0.01)
outsideIn(2, 0.01)
inAndOut(3, 0.05)
outsideIn(3, 0.01)
inAndOut(2, 0.05)
outsideIn(3, 0.01)
inAndOut(3, 0.05)
snake(10, 0.01)

flicker(3)
# sock.close()
# lampOn()
# sleep(1)
# lampOff()
