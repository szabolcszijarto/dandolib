#!/usr/bin/python

from dandolib import *
from time import sleep

d = Dash("dc:65:0f:de:4f:8b")
#d = Dot("ef:d0:c2:36:5a:3a")
print "Connected to "+d.name

# SOUNDS
d.sound()
d.sound(TRUCK)

# BEEPS
d.beep()
sleep(0.5)
d.beep(30,100)
sleep(0.5)
d.beep(30,200)
sleep(0.5)
d.beep(63,50)
sleep(0.2)
d.beep(100,50)
