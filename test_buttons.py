#!/usr/bin/python

from dandolib import *

d = Dot("ef:d0:c2:36:5a:3a", "hci0")
print "Connected to ", d.getName()

print "Now press the number buttons on your robot's head..."
print "...press top button to exit"

while not d.isButtonPressed(TOP):
    if d.isButtonPressed(ONE):
        d.beep(500,10)
    if d.isButtonPressed(TWO):
        d.beep(700,10)
    if d.isButtonPressed(THREE):
        d.beep(900,10)
