import requests as R
from time import sleep
from random import choice

# URL = 'http://108.178.248.104/LEDinfo'
URL = 'http://localhost:5000/LEDinfo'
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

def pulsate(times):
  if times < 1:
    return True
  _(q(1))(.01)
  _(w(1))(.01)
  _(e(1))(.01)
  _(r(1))(.01)
  _(t(1))(.01)
  _(y(1))(.01)
  _(u(1))(.01)
  _(i(1))(.01)
  _(o(1))(.01)
  _(p(1))(.01)
  _(q())(.01)
  _(w())(.01)
  _(e())(.01)
  _(r())(.01)
  _(t())(.01)
  _(y())(.01)
  _(u())(.01)
  _(i())(.01)
  _(o())(.01)
  _(p())
  pulsate(times-1)

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

def flicker(times):
  if times < 1:
    return True
  _(*all(1))(0.1)  
  _(*all(0))(0.1)
  flicker(times-1)

flicker(3)
rando(20)
# pulsate(10)
flicker(3)

# lampOn()
# sleep(1)
# lampOff()
