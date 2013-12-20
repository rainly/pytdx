"""macro.py imports a SendKeys module which may be downloaded at:
http://www.rutherfurd.net/python/sendkeys/

It also defines the following functions:

click() -- calls left mouse click
hold() -- presses and holds left mouse button
release() -- releases left mouse button

rightclick() -- calls right mouse click
righthold() -- calls right mouse hold
rightrelease() -- calls right mouse release

middleclick() -- calls middle mouse click
middlehold() -- calls middle mouse hold    
middlerelease() -- calls middle mouse release


move(x,y) -- moves mouse to x/y coordinates (in pixels)

slide(x,y) -- slides mouse to x/y coodinates (in pixels)
              also supports optional speed='slow', speed='fast'

The imported SendKeys has many features, but the basics are as
follows: SendKeys("Text goes here",pause=0.5,with_spaces=True)
The first string is typed on screep with a 0.5 second pause.
with_spaces = True means to NOT ignore spaces.

SendKeys("{ENTER}",pause=0.1) ; "{ENTER}" (in curly brackets) is
not typed, but instead presses the enter button on the keyboard.

"""

from ctypes import*
from SendKeys import*
user32 = windll.user32

# START SENDINPUT TYPE DECLARATIONS
PUL = POINTER(c_ulong)
class KeyBdInput(Structure):
    _fields_ = [("wVk", c_ushort),
             ("wScan", c_ushort),
             ("dwFlags", c_ulong),
             ("time", c_ulong),
             ("dwExtraInfo", PUL)]

class HardwareInput(Structure):
    _fields_ = [("uMsg", c_ulong),
             ("wParamL", c_short),
             ("wParamH", c_ushort)]

class MouseInput(Structure):
    _fields_ = [("dx", c_long),
             ("dy", c_long),
             ("mouseData", c_ulong),
             ("dwFlags", c_ulong),
             ("time",c_ulong),
             ("dwExtraInfo", PUL)]

class Input_I(Union):
    _fields_ = [("ki", KeyBdInput),
              ("mi", MouseInput),
              ("hi", HardwareInput)]

class Input(Structure):
    _fields_ = [("type", c_ulong),
             ("ii", Input_I)]

class POINT(Structure):
    _fields_ = [("x", c_ulong),
             ("y", c_ulong)]
# END SENDINPUT TYPE DECLARATIONS

  #  LEFTDOWN   = 0x00000002,
  #  LEFTUP     = 0x00000004,
  #  MIDDLEDOWN = 0x00000020,
  #  MIDDLEUP   = 0x00000040,
  #  MOVE       = 0x00000001,
  #  ABSOLUTE   = 0x00008000,
  #  RIGHTDOWN  = 0x00000008,
  #  RIGHTUP    = 0x00000010

MIDDLEDOWN = 0x00000020
MIDDLEUP   = 0x00000040
MOVE       = 0x00000001
ABSOLUTE   = 0x00008000
RIGHTDOWN  = 0x00000008
RIGHTUP    = 0x00000010


FInputs = Input * 2
extra = c_ulong(0)

click = Input_I()
click.mi = MouseInput(0, 0, 0, 2, 0, pointer(extra))
release = Input_I()
release.mi = MouseInput(0, 0, 0, 4, 0, pointer(extra))

x = FInputs( (0, click), (0, release) )
#user32.SendInput(2, pointer(x), sizeof(x[0])) CLICK & RELEASE

x2 = FInputs( (0, click) )
#user32.SendInput(2, pointer(x2), sizeof(x2[0])) CLICK & HOLD

x3 = FInputs( (0, release) )
#user32.SendInput(2, pointer(x3), sizeof(x3[0])) RELEASE HOLD

from ctypes.wintypes import *
import time

def move(x,y):
    windll.user32.SetCursorPos(x,y)
def getpos():
    global pt
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return pt.x, pt.y
def slide(a,b,speed=0):
    while True:
        if speed == 'slow':
            time.sleep(0.005)
            Tspeed = 2
        if speed == 'fast':
            time.sleep(0.001)
            Tspeed = 5
        if speed == 0:
            time.sleep(0.001)
            Tspeed = 3
        
        x = getpos()[0]
        y = getpos()[1]
        if abs(x-a) < 5:
            if abs(y-b) < 5:
                break
            
        if a < x:
            x -= Tspeed
        if a > x:
            x += Tspeed
        if b < y:
            y -= Tspeed
        if b > y:
            y += Tspeed
        move(x,y)

def click():
    user32.SendInput(2,pointer(x),sizeof(x[0]))
def hold():
    user32.SendInput(2, pointer(x2), sizeof(x2[0]))
def release():
    user32.SendInput(2, pointer(x3), sizeof(x3[0]))
    

def rightclick(): 
    windll.user32.mouse_event(RIGHTDOWN,0,0,0,0)
    windll.user32.mouse_event(RIGHTUP,0,0,0,0)
def righthold():
    windll.user32.mouse_event(RIGHTDOWN,0,0,0,0)
def rightrelease():
    windll.user32.mouse_event(RIGHTUP,0,0,0,0)

def middleclick():
    windll.user32.mouse_event(MIDDLEDOWN,0,0,0,0)
    windll.user32.mouse_event(MIDDLEUP,0,0,0,0)
def middledown():
    windll.user32.mouse_event(MIDDLEDOWN,0,0,0,0)
def middleup():
    windll.user32.mouse_event(MIDDLEUP,0,0,0,0)

def move(x,y):
    user32.SetCursorPos(x,y)

def getcolor(x=-1,y=-1,max_colors=256):
        #returns a tuple with the RGB value of the screen color
        #if no x,y position input, returns color under mouse at current location
        #if x,y input, then color at that location"""
        import ImageGrab
        if x == -1 and y == -1:
            x,y = getpos() # get current mouse position
        bbox = [x,y,x+1,y+1] # left, upper, right, lower - just 1 pixel
        img=ImageGrab.grab(bbox)
        color = img.getcolors(max_colors)
        #print color
        return color


