from gattlib import GATTRequester, DiscoveryService
from time import sleep

#
# CONSTANTS
#

# BUTTONS
TOP    = 0
ONE    = 1
TWO    = 2
THREE  = 3
ANY    = 99

# SOUNDS
BYEBYE    = 'BO_V7_VARI'
COOL      = 'COOL      '
HAHA      = 'HAPPYLAUGH'
HI        = 'DASH_HI_VO'
LETSGO    = 'LETS_GO'
TRUMPET   = 'TRUMPET_01'
TAHDAH    = 'TAH_DAH_01'
UHUH      = 'YAUHHUH'
UHOH      = 'WHUH_OH_20'
YIPPE     = 'YIPPEE'
OOH       = 'HAVINGFUN1'
OHYEAH    = 'BRAGGING1A'
OHNO      = 'V7_OHNO_09'
WOW       = 'CONFUSED_8'
WOW2       = 'DASH_WOW_3'
CONFUSED  = 'CONFUSED_1'
GIGGLE    = 'HAPPYLAUGH'
GOBBLE    = 'GOBBLE_001'
GRUNT     = 'HEAVYOBJEC'
SIGN      = 'BO_V7_YAWN'
SNORE     = 'SNORING'
SQUEAK    = 'OT_CUTE_04'
SURPRISED = 'SURPRISE02'
WAH       = 'DASH_WHAA1'
WEEHEE    = 'WHEEYEEYEE'
YAWN      = 'TIRED_YAWN'
CAT       = 'FX_CAT_01'
CROCODILE = 'CROCODILE'
DINOSAUR  = 'DINOSAUR_3'
COW       = 'COW_MOO11A'
DOG       = 'FX_DOG_02'
ELEPHANT  = 'ELEPHANT_0'
GOAT      = 'FX_03_GOAT'
HORSE     = 'HORSEWHIN3'
LION      = 'FX_LION_01'
TRUCK     = 'TRUCKHORN'
HORN      = 'HAPPY_HONK'
SIREN     = 'X_SIREN_02'
TIRE      = 'TIRESQUEAL'
AIRPLANE  = 'AIRPORTJET'
BEEP      = 'BOT_CUTE_0'
BOAT      = 'TUGBOAT_01'
BUZZ      = 'US_LIPBUZZ'
HELICOPTER= 'HELICOPTER'
LASERS    = 'OT_CUTE_03'
SPEEDBOOST= 'SHORTBOOST'
ENGINEREV = 'ENGINE_REV'
TRAIN     = 'TRAIN_WHIS'

# LIGHTS
BLACK   = str(bytearray([0x00, 0x00, 0x00]))
RED     = str(bytearray([0xff, 0x00, 0x00]))
ORANGE  = str(bytearray([0xff, 0x31, 0x00]))
YELLOW  = str(bytearray([0xff, 0xa0, 0x00]))
GREEN   = str(bytearray([0x20, 0xff, 0x00]))
BLUE    = str(bytearray([0x00, 0xa7, 0xff]))
PURPLE  = str(bytearray([0xff, 0x00, 0xaa]))
ON      = chr(0xff)
OFF     = chr(0x00)

# SPEEDS AND DIRECTIONS FOR DASH
VERY_SLOW     = 1
SLOW          = 2
NORMAL        = 3
FAST          = 4
REALLY_FAST   = 5
    
FORWARD       = 1
BACKWARD      = 0

#
# FUNCTIONS FOR ROBOT DISCOVERY
#
def findBT4LEDevices(device="hci0", timeout=3):
    service = DiscoveryService(device)
    devices = service.discover(timeout) # timeout in sec
    return devices.items()

def findDeviceAddrByName(name_to_find, device="hci0", timeout=3):
    service = DiscoveryService(device)
    devices = service.discover(timeout) # timeout in sec
    device_list = devices.items()
    address_found = ""
    if len(device_list)>0:
            for address, name in list(device_list):
                if name == name_to_find: address_found = address
    return address_found

def findDash(name_to_find="dash", device="hci0", timeout=3):
    address = findDeviceAddrByName(name_to_find, device, timeout)
    if address == "" : raise Exception("A robot with that name was not found")
    d = Dash(address, device)
    assert (type(d) is Dash), "Robot class couldn't be initialized"
    while not d.isConnected(): pass
    return d

def findDot(name_to_find="dot", device="hci0", timeout=3):
    address = findDeviceAddrByName(name_to_find, device, timeout)
    if address == "" : raise Exception("A robot with that name was not found")
    d = Dot(address, device)
    assert (type(d) is Dot), "Robot class couldn't be initialized"
    while not d.isConnected(): pass
    return d

#
# CLASS FOR BT 4 LE GATT COMMUNICATION
#
class Requester(GATTRequester):
    
    def __init__(self, address, do_connect, device ):
        GATTRequester.__init__(self, address, do_connect, device)
        self.notification21data = ""
        self.notification24data = ""

    def on_notification(self, handle, data):
        # save all data received in the notification
        if handle==21: self.notification21data = data
        if handle==24: self.notification24data = data
#
# SUPERCLASS FOR DASH AND DOT
# Contains features common to both types of robots
#
class WWRobot(object):

    _horizontal_stable_pos = 0
    _vertical_stable_pos   = 15

    def __init__(self, address, device="hci0", timeout=3, auto_connect=True):
        self.device = device
        self.address = address
        self.requester = Requester(self.address, False, self.device)
        self.setWait4IdleFlag(True)
        if auto_connect: self.connect()

    def __del__(self):
        if self.isConnected():
            self.disconnect()

    def isDash(self):
        return False

    def isDot(self):
        return False

    def setWait4IdleFlag(self, param=True):
        self.wait4IdleFlag = (param == True)
        

    #
    # CONNECTION
    #
    
    def connect(self):
        self.requester.connect(True, "random", "low")
        if self.isConnected():
            self.setName()
            self.reset()
            self.startNotifications()

    def isConnected(self):
        if (self.address == ""): return False
        else: return self.requester.is_connected()

    def disconnect(self):
        self.requester.disconnect()

    def reset(self):
        self.requester.write_by_handle(0x0013, chr(0xc8) + chr(0x04))

    def setName(self):
        self.name = self.requester.read_by_handle(0x0003)[0]

    def getName(self):
        return self.name

    def getDevice(self):
        return self.device
        
    def getAddress(self):
        return self.address

    def startNotifications(self):
        self.requester.write_by_handle(0x0011, str(bytearray([0x01, 0x00])) )
        self.requester.write_by_handle(0x0016, str(bytearray([0x01, 0x00])) )
        self.requester.write_by_handle(0x0019, str(bytearray([0x01, 0x00])) )
        self.requester.write_by_handle(0x0013, str(bytearray([0xc9, 0x18, 0x1c])) )
        self.requester.write_by_handle(0x0013, str(bytearray([0xc8, 0x41, 0x20, 0x53, 0x4e, 0x20, 0x47, 0x45, 0x54, 0x0a])) )

    def getNotificationData(self, handle):
        # notifications are received on handles 21 or 24
        if handle==21: d = self.requester.notification21data
        if handle==24: d = self.requester.notification24data
        return d

    #
    # IDLE DETECTION
    #
    
    def isIdle(self):
        stat = ord(self.requester.notification21data[14])
        #TODO: these constants are still not quite clear...
        #0x02 = sound is playing
        #0x10 = dash hears clap?
        #0x20 = dash is moving - even if not by itself
        if self.isDash():
            status = stat & 0xef
            _idle = 0x28
        if self.isDot():
            status = stat
            _idle = 0x00
        #print "Idle status = " +"{0:08b}".format(stat)+ " / " +"{0:08b}".format(status)+ " (expected status for idle =" +"{0:08b}".format(_idle) + ")"
        return (status == _idle)

    def waitUntilIdle(self):
        if (self.wait4IdleFlag):
            while not self.isIdle():
                sleep(0.05)

    def waitUntilBusy(self):
        if (self.wait4IdleFlag):
            while self.isIdle():
                sleep(0.01)
        

    #
    # BUTTONS
    #
  
    def isButtonPressed(self, button=ANY):
        r = False
        _m1 = ord(self.getNotificationData(21)[11])
        if button == TOP:   r = ( (_m1 & 0x10) > 0)
        if button == ONE:   r = ( (_m1 & 0x20) > 0)
        if button == TWO:   r = ( (_m1 & 0x40) > 0)
        if button == THREE: r = ( (_m1 & 0x80) > 0)
        if button == ANY:   r = ( (_m1 & 0xf0) > 0)
        return r

    #
    # SOUNDS
    #

    def sound(self, what=HORN):
        #print "Playing %s" % what
        self.requester.write_by_handle(0x0013, chr(0x18) + 'SYST' + what)
        sleep(0.1)
        if (self.wait4IdleFlag):
            # wait until command completes
            while ( ord(self.requester.notification21data[14]) & 0x02 ) > 0 :
                pass
            

    def beep(self, pitch=400, duration=50):
        _p1 = pitch // 256 # HI byte
        _p2 = pitch % 256  # LO byte
        self.requester.write_by_handle(0x0013, chr(0x19) + chr(_p1) + chr(_p2) + chr(duration))

    #
    # LIGHTS
    #

    def setEyeLights(self, pattern) :
        if pattern == OFF:
            _hi = 0x00
            _lo = 0x00
        elif pattern == ON:
            _hi = 0x0f
            _lo = 0xff
        else:
            _hi = pattern >> 8       # HIBYTE
            _lo = pattern & 0x00ff   # LOBYTE
        self.requester.write_by_handle(0x0013, chr(0x08) + chr(0xff) + chr(0x09) + chr(_hi) + chr(_lo) )

    def setLeftLightRGB(self, red, green, blue) :
        self.requester.write_by_handle(0x0013, chr(0x0b) + red + green + blue)

    def setLeftLight(self, color) :
        self.setLeftLightRGB(color[0] , color[1] , color[2])

    def setRightLightRGB(self, red, green, blue) :
        self.requester.write_by_handle(0x0013, chr(0x0c) + red + green + blue)

    def setRightLight(self, color) :
        self.setRightLightRGB(color[0] , color[1] , color[2])

    def setFrontLightRGB(self, red, green, blue) :
        self.requester.write_by_handle(0x0013, chr(0x03) + red + green + blue)

    def setFrontLight(self, color) :
        self.setFrontLightRGB(color[0] , color[1] , color[2])

    def setAllLightsRGB(self, red, green, blue) :
        self.requester.write_by_handle(0x0013, chr(0x03) + red + green + blue + \
                                               chr(0x0b) + red + green + blue + \
                                               chr(0x0c) + red + green + blue )

    def setAllLights(self, color) :
        self.setAllLightsRGB(color[0] , color[1] , color[2])

    #
    # SOUND SENSORS
    #
    
    def hearSound(self):
        _m1 = ord(self.getNotificationData(21)[10]) # left?
        _m2 = ord(self.getNotificationData(21)[12]) # right?
        return (_m1 > 0x01) or (_m2 > 0x80)

    def hearClap(self):
        stat = ord(self.requester.notification21data[14])
        #0x10 = dash hears clap?
        status = stat & 0x10
        return (status > 0)

    #
    # TILT SENSORS
    #

    # TODO: to avoid "drifting", these methods need offset values which are different for each individual robot

    def getHorizontalTilt(self):
        _m1 = ord(self.getNotificationData(21)[7])
        _horizontal = (_m1 & 0x0f) - self._horizontal_stable_pos
        #print "horizontal status: %02x " % _m1 , _horizontal
        return _horizontal

    def getVerticalTilt(self):
        _m1 = ord(self.getNotificationData(21)[7])
        _vertical = (_m1 >> 4) - self._vertical_stable_pos
        #print "vertical status: %02x " % _m1 , _vertical
        return _vertical        

    def isStable(self):
        _m1 = ord(self.getNotificationData(21)[7])
        _horizontal = self.getHorizontalTilt()
        _vertical = self.getVerticalTilt()
        _tilted_horizontally = _horizontal <> 0
        _tilted_vertically = _vertical <> 0
        #print "Tilt status: %02x " % _m1 , _horizontal, _vertical, _tilted_horizontally, _tilted_vertically
        return (not _tilted_horizontally) and (not _tilted_vertically)

    def isTilted(self):
        return not self.isStable()

    def isTiltedLeft(self):
        _m1 = self.getNotificationData(21)[7]
        _horizontal = ord(_m1) & 0x0f
        _tilted_left = (_horizontal >= 11) and (_horizontal <= 15)
        return _tilted_left

    def isTiltedRight(self):
        _m1 = self.getNotificationData(21)[7]
        _horizontal = ord(_m1) & 0x0f
        _tilted_right = (_horizontal >= 1) and (_horizontal <= 3)
        return _tilted_right

    def isTiltedUp(self):
        _m1 = self.getNotificationData(21)[7]
        _vertical = ord(_m1) >> 4
        _tilted_up = (_vertical >= 0) and (_vertical <= 3)
        return _tilted_up

    def isTiltedDown(self):
        _m1 = self.getNotificationData(21)[7]
        _vertical = ord(_m1) >> 4
        _tilted_down = (_vertical >= 11) and (_vertical <= 14)
        return _tilted_down

    def isBeingShaken(self):
        _m1 = ord(self.getNotificationData(21)[5])
        _m2 = ord(self.getNotificationData(21)[6])
        _m4 = ord(self.getNotificationData(21)[9])
        # TODO
        return ( False )

#
# DOT
#

class Dot(WWRobot):

    def __init__(self, address, device="hci0", timeout=3, auto_connect=True):
        super(Dot,self).__init__(address, device, timeout, auto_connect)

    def isDot(self):
        return True

#
# DASH
#

class Dash(WWRobot):

    def __init__(self, address, device="hci0", timeout=3, auto_connect=True):
        self.setDistanceTreshold(200)
        super(Dash,self).__init__(address, device, timeout, auto_connect)
        
    def isDash(self):
        return True

    #
    # DISTANCE SENSORS
    #

    def setDistanceTreshold(self, t):
        self.distancetreshold = t
    
    def getObjectDistanceLeft(self):
        _m1 = ord(self.getNotificationData(24)[9])
        return 255 - _m1
        
    def getObjectDistanceRight(self):
        _m1 = ord(self.getNotificationData(24)[10])
        return 255 - _m1

    def getObjectDistanceBehind(self):
        _m1 = ord(self.getNotificationData(24)[11])
        return 255 - _m1

    def isSomethingLeft(self):
        return self.getObjectDistanceLeft() < self.distancetreshold

    def isSomethingRight(self):
        return self.getObjectDistanceRight() < self.distancetreshold

    def isSomethingBehind(self):
        return self.getObjectDistanceBehind() < self.distancetreshold

    def isSomethingAhead(self):
        return (self.getObjectDistanceLeft() < self.distancetreshold) and (self.getObjectDistanceRight() > self.distancetreshold)


    #
    # TAIL LIGHT
    #

    def setTailLight(self, on_or_off) :
        self.requester.write_by_handle(0x0013, chr(0x04) + on_or_off)

    #
    # MOVING AROUND
    #
    
    def move(self, direction=FORWARD, distance=20, speed=NORMAL):
        # the input parameter distance is measured in centimeters
        # however the protocol requires this is millimeters, hence a coversion is needed
        _distance = distance*10
        if speed==VERY_SLOW :   _multiplier = 12.5
        if speed==SLOW :        _multiplier = 5
        if speed==NORMAL :      _multiplier = 2.5
        if speed==FAST :        _multiplier = 1.5
        if speed==REALLY_FAST : _multiplier = 1
        if direction==FORWARD :
            # forward
            _d1 = int ( _distance % 256 )                   # LO byte
            _d2 = int ( _distance // 256 )                  # HI byte
            _d3 = int ( (_distance * _multiplier) // 256 )  # HI byte
            _d4 = int ( (_distance * _multiplier) % 256 )   # LO byte
            self.requester.write_by_handle(0x0013, chr(0x23) +chr(_d1) +chr(0x00) +chr(0x00) \
                                                  +chr(_d3) +chr(_d4) +chr(_d2) +chr(0x00) +chr(0x80))
        if direction==BACKWARD :
            # backward, distance is expressed negative
            _d1 = int ( ( 16384 - _distance ) % 256 )       # LO byte
            _d2 = int ( ( 16384 - _distance ) // 256 )      # HI byte
            _d3 = int ( (_distance * _multiplier) // 256 )  # HI byte
            _d4 = int ( (_distance * _multiplier) % 256 )   # LO byte
            self.requester.write_by_handle(0x0013, chr(0x23) +chr(_d1) +chr(0x00) +chr(0x00) \
                                                  +chr(_d3) +chr(_d4) +chr(_d2) +chr(0x00) +chr(0x41))
        if (self.wait4IdleFlag):
            self.waitUntilBusy() # wait until command actually gets executed
            self.waitUntilIdle() # wait until command completes


    def drive(self,direction=FORWARD, speed=NORMAL):
        if direction==FORWARD :
            if speed==VERY_SLOW :
                _m1 = 0x28
                _m2 = 0x00
            if speed==SLOW :
                _m1 = 0x64
                _m2 = 0x00
            if speed==NORMAL :
                _m1 = 0xc8
                _m2 = 0x00
            if speed==FAST :
                _m1 = 0x2c
                _m2 = 0x01
            if speed==REALLY_FAST :
                _m1 = 0x90
                _m2 = 0x01
        if direction==BACKWARD :
            if speed==VERY_SLOW :
                _m1 = 0xd8
                _m2 = 0x07
            if speed==SLOW :
                _m1 = 0x9c
                _m2 = 0x07
            if speed==NORMAL :
                _m1 = 0x38
                _m2 = 0x07
            if speed==FAST :
                _m1 = 0xd4
                _m2 = 0x06
            if speed==REALLY_FAST :
                _m1 = 0x70
                _m2 = 0x06
        self.requester.write_by_handle(0x0013, chr(0x02) +chr(_m1) +chr(0x00) +chr(_m2))

    def stop(self):
        self.requester.write_by_handle(0x0013, chr(0x02) +chr(0x00) +chr(0x00) +chr(0x00))

    def turn_left(self, angle=90):
        _ang = angle
        if _ang>360: _ang = 360
        if _ang<1:   _ang = 0
        _magic1 = _ang * 1.74
        _magic2 = _ang * 5.81
        _m1 = int ( _magic1 // 256 ) * 64    # HI byte
        _m2 = int ( _magic1 % 256 )          # LO byte
        _m3 = int ( _magic2 // 256 )         # HI byte
        _m4 = int ( _magic2 % 256  )         # LO byte
        self.requester.write_by_handle(0x0013, chr(0x23) +chr(0x00) +chr(0x00) \
                                              +chr(_m2) +chr(_m3) +chr(_m4) +chr(_m1) \
                                              +chr(0x00) +chr(0x80) )
        if (self.wait4IdleFlag):
            self.waitUntilBusy() # wait until command actually gets executed
            self.waitUntilIdle() # wait until command completes


    def turn_right(self, angle=90):
        _ang = angle
        if _ang>360: _ang = 360
        if _ang<1:   _ang = 0
        _magic1 = 1024 - ( _ang * 1.74 )
        _magic2 = _ang * 5.81
        _m1 = int ( _magic1 // 256 ) * 64    # HI byte
        _m2 = int ( _magic1 % 256 )          # LO byte
        _m3 = int ( _magic2 // 256 )         # HI byte
        _m4 = int ( _magic2 % 256  )         # LO byte
        self.requester.write_by_handle(0x0013, chr(0x23) +chr(0x00) +chr(0x00) \
                                              +chr(_m2) +chr(_m3) +chr(_m4) +chr(_m1) \
                                              +chr(0xc0) +chr(0x80) )
        if (self.wait4IdleFlag):
            self.waitUntilBusy() # wait until command actually gets executed
            self.waitUntilIdle() # wait until command completes

    #
    # TURNING THE HEAD
    #
    
    def look(self, horizontal, vertical):
        self.look_horizontal(horizontal)
        self.look_vertical(vertical)

    def look_horizontal(self,horizontal):
        # horizontal: between 22 (up) , 0 (straight) , -7 (down)
        if horizontal<0 :
            _h1 = ( 65536 + horizontal * 100) // 256 # HI byte
            _h2 = ( 65536 + horizontal * 100) % 256  # LO byte
        else :
            _h1 = ( horizontal * 100 ) // 256 # HI byte
            _h2 = ( horizontal * 100 ) % 256  # LO byte
        self.requester.write_by_handle(0x0013, chr(0x06) +chr(_h1) +chr(_h2))        

    def look_vertical(self,vertical):
        # vertical: between 22 (up) , 0 (straight) , -7 (down)
        if vertical<0 :
            _v1 = ( 65536 + vertical * 100) // 256 # HI byte
            _v2 = ( 65536 + vertical * 100) % 256  # LO byte
        else :
            _v1 = ( vertical * 100 ) // 256 # HI byte
            _v2 = ( vertical * 100 ) % 256  # LO byte
        self.requester.write_by_handle(0x0013, chr(0x07) +chr(_v1) +chr(_v2))        

