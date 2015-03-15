from collections import OrderedDict

# mapping of physical pin (and human readable name) to the internal GPIO pin numbering
# ie: {name: data}
_unordered_pins = {

# Breadboard with 10 LEDs starting at pin2 
  # 'pin1': { 'pin': 7, 'name' : 'Lamp', 'state': False, 'weight': 1 },
  # 'pin2': { 'pin': 11, 'name' : 'LED 1', 'state': False, 'weight': 2 },
  # 'pin3': { 'pin': 13, 'name' : 'LED 2', 'state': False, 'weight': 3 },
  # 'pin4': { 'pin': 15, 'name' : 'LED 3', 'state': False, 'weight': 4 },
  # 'pin5': { 'pin': 12, 'name' : 'LED 4', 'state': False, 'weight': 5 },
  # 'pin6': { 'pin': 16, 'name' : 'LED 5', 'state': False, 'weight': 6 },
  # 'pin7': { 'pin': 18, 'name' : 'LED 6', 'state': False, 'weight': 7 },
  # 'pin8': { 'pin': 22, 'name' : 'LED 7', 'state': False, 'weight': 8 },
  # 'pin9': { 'pin': 24, 'name' : 'LED 8', 'state': False, 'weight': 9 },
  # 'pin10': { 'pin': 26, 'name' : 'LED 9', 'state': False, 'weight': 10 },
  # 'pin11': { 'pin': 19, 'name' : 'LED 10', 'state': False, 'weight': 11 }
# Office light controled via relay
  'pin1': { 'pin': 11, 'name' : 'Light', 'state': False, 'weight': 1 }
}
# guarantees order during iteration based on the weight key
PinsMap = OrderedDict(sorted(_unordered_pins.items(), key=lambda t: t[1]['weight']))
PinNames = PinsMap.keys()