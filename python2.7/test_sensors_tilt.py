#!/usr/bin/python

from dandolib import *
from time import sleep

d = Dot("ef:d0:c2:36:5a:3a")
print "Connected to ", d.getName()

print "Tilt your robot in any direction..."
print "Press top button to exit!"

while not d.isButtonPressed(TOP):
    if d.isTiltedLeft():
        print "Left ",
    if d.isTiltedRight():
        print "Right ",
    if d.isTiltedUp():
        print "Up",
    if d.isTiltedDown():
        print "Down",
    if d.isStable():
        print "----",
    print ""
    sleep(0.1)

d.disconnect()

