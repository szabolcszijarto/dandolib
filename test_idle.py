#!/usr/bin/python

from dandolib import *
from time import sleep

#d = Dash("dc:65:0f:de:4f:8b")
d = Dot("ef:d0:c2:36:5a:3a")
print "Connected to", d.getName()

#this is set by default, setting it to false would result in asynchronous execution
d.setWait4IdleFlag(False)


for i in range(1,80):
    d.isIdle()
    sleep(0.1)

#print "Moving"
#d.move(FORWARD, 20, VERY_SLOW)

print "Cow..."
d.sound(COW)

for i in range(1,40):
    d.isIdle()
    sleep(0.1)

