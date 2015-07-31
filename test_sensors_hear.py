#!/usr/bin/python

from dandolib import *
from time import sleep

d = Dot("ef:d0:c2:36:5a:3a")

print "Say hello to", d.getName(),"!"

while not d.hearSound():
    sleep (0.1)

sleep(1)

d.sound(HI)

d.disconnect()

