#!/usr/bin/python

from dandolib import *
from time import sleep

#d = Dot("ef:d0:c2:36:5a:3a")
d = Dash("dc:65:0f:de:4f:8b")

d.setWait4IdleFlag(False)

if d.name == 'Dot1':
    d._horizontal_stable_pos = 15
    d._vertical_stable_pos   = 0
elif d.name == 'dash':
    d._horizontal_stable_pos = 0
    d._vertical_stable_pos   = 15
    
print "Move ", d.getName(), " around... ",
print "press top button to exit!"

while not d.isButtonPressed(TOP):
    x = not d.isStable()
    y = d.isIdle()
    print "Flying=",x," Idle=",y
    if x and y:
        d.move(FORWARD, 30, VERY_SLOW)
        #d.sound(HELICOPTER)
    sleep(0.1)
    
d.disconnect()

