#!/usr/bin/python

from dandolib import *
from time import sleep

d = findDash()

d.setAllLights(BLACK)
d.setEyeLights(0x0000)
sleep(1)
d.setAllLights(RED)
sleep(1)
d.setAllLights(YELLOW)
sleep(1)
d.setAllLights(GREEN)
sleep(0.2)

pattern=0x0000
for i in range(0,12):
    pattern = 1 << i
    d.setEyeLights(pattern)    
    sleep(0.1)

pattern=0x0000
for i in range(0,12):
    pattern += 1 << i
    d.setEyeLights(pattern)    
    sleep(0.1)

sleep(0.5)
d.setEyeLights(0x0000)
d.setAllLights(BLACK)

