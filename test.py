import requests as R
from time import sleep
from random import choice


import wave, struct

waveFile = wave.open('sine.wav', 'r')

length = waveFile.getnframes()
for i in range(0,length):
    waveData = waveFile.readframes(1)
    data = struct.unpack("<h", waveData)
    print int(data[0])

URL = 'http://108.178.248.104/LEDinfo'
# state should be 0 or 1
def l(state=0):
  state = str(state)
  return {"Lamp": state}
def a(state=0):
  state = str(state)
  return {"Alpha": state}
def t(state=0):
  state = str(state)
  return {"pin3": state}
def f(state=0):
  state = str(state)
  return {"pin4": state}

  
def _(*args):
  data = dict(obj.items()[0] for obj in args)
  R.post(URL, data=data)


_(l(1), a(0), t(1), f(0))

def pulsate(times):
  if times < 1:
    return True
  _(a(1))
  sleep(.01)
  _(t(1))
  sleep(.01)
  _(a(0), f(1))
  sleep(.01)
  _(t(0))
  sleep(.01)
  _(f(0))
  pulsate(times-1)

def rando(times):
  if times < 1:
    return True
  data = []
  # do one random choice per light
  choiceA = choice([1, 0])
  data.append(a(choiceA))
  choiceT = choice([1, 0])
  data.append(t(choiceA))
  choiceF = choice([1, 0])
  print choiceA, choiceT, choiceF
  data.append(f(choiceA))
  _(*data)
  sleep(.5)
  rando(times-1)

def flicker(times):
  if times < 1:
    return True
  _(a(1), t(1), f(1))  
  _(a(0), t(0), f(0))
  sleep(.3)
  flicker(times-1)
# flicker(5)
# rando(20)
# # pulsate(30)
# flicker(5)

# lampOn()
# sleep(1)
# lampOff()
