#!/usr/bin/python

from dandolib import *
from time import sleep

d = Dash("dc:65:0f:de:4f:8b")
#d = Dot("ef:d0:c2:36:5a:3a")
print "Connected to", d.getName()

#this is set by default, setting it to false would result in asynchronous execution
#d.setWait4IdleFlag(True)

print "Cow..."
d.sound(COW)

print "Moving"
d.move(FORWARD, 30, NORMAL)

print "Hi..."
d.sound(HI)

