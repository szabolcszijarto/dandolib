#!/usr/bin/python

from dandolib import *
from time import sleep

d = Dash("dc:65:0f:de:4f:8b")
#d = Dot("ef:d0:c2:36:5a:3a")
print "Connected to", d.getName()

d.setEyeLights(ON)
sleep(1)
d.setEyeLights(OFF)
print "red"
d.setFrontLight(RED)
d.setLeftLight(RED)
d.setRightLight(RED)
sleep(2)
print "orange"
d.setAllLights(ORANGE)
sleep(2)
print "yellow"
d.setAllLights(YELLOW)
sleep(2)
print "green"
d.setAllLights(GREEN)
sleep(2)
print "blue"
d.setAllLights(BLUE)
sleep(2)
print "purple"
d.setAllLights(PURPLE)
sleep(2)
print "off"
d.setAllLights(BLACK)
sleep(2)

if d.isDash():
    print "tail on, then off"
    d.setTailLight(ON)
    sleep(2)
    d.setTailLight(OFF)
