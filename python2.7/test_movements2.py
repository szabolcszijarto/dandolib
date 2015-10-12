#!/usr/bin/python

from dandolib import *
from time import sleep

d = findDash("dash")

d.move(FORWARD, 50, SLOW)
sleep(3)

d.move(BACKWARD, 30, FAST)
sleep(3)

d.drive(FORWARD, NORMAL)
sleep(2)
d.stop()
sleep(1)

d.turn_left(45)
sleep(2)
d.turn_right(90+45)
sleep(2)
d.turn_left(90+180)
sleep(2)

d.disconnect()
