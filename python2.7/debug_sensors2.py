#!/usr/bin/python

from time import sleep
from dandolib import *

def print_header():
    # print header
    i=0
    print("___"),
    while i<23:
        print "%02d" % (i),
        i+=1        
    print "|",
    i=0
    while i<23:
        print "%02d" % (i),
        i+=1
    print ""

def monitor_sensors(limit):
    # print notifications for a while
    for counter in range(0, limit):
        print "%02d:" % counter,
        b = d.getNotificationData(21)
        print "%02x" % ord(b[0]),
        print "%02x" % ord(b[1]),
        print "%02x" % ord(b[2]),
        print "%02x" % ord(b[3]),
        print "%02x" % ord(b[4]),
        print "%02x" % ord(b[5]),
        print "%02x" % ord(b[6]),
        print "--" , # TILT SENSORS
        print "%02x" % ord(b[8]),
        print "%02x" % ord(b[9]),
        print "--" , # SOUND SENSOR
        print "--" , # HIGHER 4 BITS: BUTTONS
        print "--" , # SOUND SENSOR
        print "%02x" % ord(b[13]),
        print "%02x" % ord(b[14]),
        print "%02x" % ord(b[15]),
        print "%02x" % ord(b[16]),
        print "%02x" % ord(b[17]),
        print "%02x" % ord(b[18]),
        print "%02x" % ord(b[19]),
        print "%02x" % ord(b[20]),
        print "%02x" % ord(b[21]),
        print "%02x" % ord(b[22]),
        print "|",
        b = d.getNotificationData(24)
        print "%02x" % ord(b[0]),
        print "%02x" % ord(b[1]),
        print "%02x" % ord(b[2]),
        print "%02x" % ord(b[3]),
        print "%02x" % ord(b[4]),
        print "%02x" % ord(b[5]),
        print "%02x" % ord(b[6]),
        print "%02x" % ord(b[7]),
        print "%02x" % ord(b[8]),
        print "--" , # DISTANCE SENSOR LEFT
        print "--" , # DISTANCE SENSOR RIGHT
        print "--" , # DISTANCE SENSOR REAR
        print "%02x" % ord(b[12]),
        print "%02x" % ord(b[13]),
        print "%02x" % ord(b[14]),
        print "%02x" % ord(b[15]),
        print "%02x" % ord(b[16]),
        print "%02x" % ord(b[17]),
        print "%02x" % ord(b[18]),
        print "%02x" % ord(b[19]),
        print "%02x" % ord(b[20]),
        print "%02x" % ord(b[21]),
        print "%02x" % ord(b[22]),
        print("")
        sleep(0.1)
    

if __name__ == '__main__':
    d = Dash("dc:65:0f:de:4f:8b")
    d.setWait4IdleFlag(False)
    print "Connected to", d.getName()
    sleep(0.1)

    print_header()
    monitor_sensors(10)
    #print("\nDO SOMETHING...\n")
    print
    d.move(FORWARD, 10, VERY_SLOW)
    #d.sound(ELEPHANT)
    sleep(1)
    monitor_sensors(99)
    print_header()
    #for counter in range(0, 25):
    #    print d.isIdle() ,
        #print "%02x" % ord(d.requester.notification21data[14])
    #    sleep(0.1)
    print("THE END")

    d.disconnect()

