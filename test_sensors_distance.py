#!/usr/bin/python

from dandolib import *
from time import sleep

d = Dash("dc:65:0f:de:4f:8b")
print "Connected to ", d.getName()

print "Test your robot's distance sensors"
print "Press top button to exit!"

while not d.isButtonPressed(TOP):
    if d.isSomethingAhead():
        x = d.getObjectDistanceLeft()
        y = d.getObjectDistanceRight()
        print("object ahead: "+ str(x) +"/"+ str(y)),
        d.beep(800 - x - y , 10)
    else:
        if d.isSomethingLeft():
            x = d.getObjectDistanceLeft()
            print("object left: "), str(x)
            d.beep(800 - 2*x , 10)
        if d.isSomethingRight():
            x = d.getObjectDistanceRight()
            print("object right: ", str(x))
            d.beep(800 - 2*x , 10)
    if d.isSomethingBehind():
        x = d.getObjectDistanceBehind()
        print("object behind: ", str(x))
        d.beep(800 - 2*x , 10)
    print ""
    sleep(0.1)  

d.disconnect()

