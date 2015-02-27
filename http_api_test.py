import requests as R
from time import sleep
from random import choice

URL = 'http://108.178.248.104/LEDinfo'
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
  R.post(URL, data=data)
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
  pulsate(times-1)

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

  snake(times-1)

def rando(times):
  if times < 1:
    return True
  data = []
  # do one random choice per light
  for thing in each():
    c = choice([1, 0])
    data.append(thing(c))
  _(*data)(0.5)
  rando(times-1)

def flicker(times, frequency=0.1):
  if times < 1:
    return True
  _(*all(1))(frequency)  
  _(*all(0))(frequency)
  flicker(times-1)

flicker(3, 0.05)
# rando(20)
snake(10, 0.01)
flicker(3)

# lampOn()
# sleep(1)
# lampOff()
