#!/usr/bin/python

from dandolib import *

print "Discovering BT 4 LE devices..."
rl = findBT4LEDevices() # defaults: device hci0 , timeout = 3 sec
l = len(rl)
print "%d devices found." % l
if l > 0:
    for address, name in list(rl):
        print("name: {}, address: {}".format(name, address))

name = "dash"
print "\nLooking for", name
d = findDot(name)
if d.isConnected():
    print "Connected to %s" % d.getName()
    d.setAllLights(RED)
    print "Press top button on %s to exit" % d.getName()
    while not d.isButtonPressed(TOP): pass
