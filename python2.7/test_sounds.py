#!/usr/bin/python

from dandolib import *
from time import sleep

d = Dash("dc:65:0f:de:4f:8b")
#d = Dot("ef:d0:c2:36:5a:3a")
print "Connected to "+d.name

# SOUNDS
d.sound()
sleep(2)
d.sound(TRUCK)
sleep(2)
d.sound(HI)
sleep(2)
d.beep()
sleep(2)
d.beep(600,200)
sleep(2)

d.disconnect()
