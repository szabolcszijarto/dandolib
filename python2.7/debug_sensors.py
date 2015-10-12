#!/usr/bin/python

from time import sleep
from dandolib import *

def print_header():
    # print header
    i=0
    while i<23:
        print "%02d" % (i),
        i+=1        
    print "|",
    i=0
    while i<23:
        print "%02d" % (i),
        i+=1
    print ""

if __name__ == '__main__':
    d = findDash("dash")
    print "Connected to", d.getName()
    sleep(0.1)

    print_header()
    # print notifications until top button is pressed
    while not d.isButtonPressed(TOP):
        b = d.getNotificationData(21)
        print "%02x" % ord(b[0]),
        print "%02x" % ord(b[1]),
        print "%02x" % ord(b[2]),
        print "%02x" % ord(b[3]),
        print "%02x" % ord(b[4]),
        print "%02x" % ord(b[5]),
        print "%02x" % ord(b[6]),
        print "%02x" % ord(b[7]),
        print "%02x" % ord(b[8]),
        print "%02x" % ord(b[9]),
        print "%02x" % ord(b[10]),
        print "%02x" % ord(b[11]),
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
        print "%02x" % ord(b[9]),
        print "%02x" % ord(b[10]),
        print "%02x" % ord(b[11]),
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
    print_header()

    d.disconnect()

