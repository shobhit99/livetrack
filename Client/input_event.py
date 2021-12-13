from os import sys
platform = sys.platform[:3]

if platform == 'lin':
    from Xlib.display import Display
    from Xlib import X
    from Xlib.ext.xtest import fake_input

elif platform == 'mac':
    from Quartz import *
    from AppKit import NSEvent
    pressID =   [None, kCGEventLeftMothe,
                kCGEventRightMouseDown, kCGEventOtherMouseDown]
    releaseID = [None, kCGEventLeftMouseUp,
                kCGEventRightMouseUp, kCGEventOtherMouseUp]

elif platform == 'win':
    from ctypes import *
    import win32api, win32con
    class POINT(Structure):
        _fields_ = [("x", c_ulong),
                    ("y", c_ulong)]

 
button_ids = [None, 1, 3, 2, 4, 5, 6, 7]

CustomCodes = {
16777217 : 23, 
16777220 : 36, 
32 : 65, 
126 : 10, 
34 : 48, 
64 : 12, 
36 : 13, 
37 : 14, 
38 : 16, 
39 : 48, 
40 : 187, 
41 : 188, 
42 : 17, 
43 : 21, 
44 : 59, 
45 : 20, 
46 : 60, 
47 : 61, 
48 : 19, 
49 : 10, 
50 : 11, 
51 : 12, 
52 : 13, 
53 : 14, 
54 : 15, 
55 : 16, 
56 : 17, 
57 : 18, 
58 : 47, 
59 : 47, 
60 : 94, 
61 : 21, 
62 : 60, 
63 : 61, 
64 : 11, 
91 : 34, 
92 : 51, 
93 : 35, 
94 : 15, 
95 : 20, 
96 : 49, 
65 : 38, 
66 : 56, 
67 : 54, 
68 : 40, 
69 : 26, 
70 : 41, 
71 : 42, 
72 : 43, 
73 : 31, 
74 : 44, 
75 : 45, 
76 : 46, 
77 : 58, 
78 : 57, 
79 : 32, 
80 : 33, 
81 : 24, 
82 : 27, 
83 : 39, 
84 : 28, 
85 : 30, 
86 : 55, 
87 : 25, 
88 : 53, 
89 : 29, 
90 : 52, 
123 : 34, 
124 : 51, 
125 : 35, 
126 : 49, 
16777251 : 64,
16777219 : 22, 
16777252 : 66,
16777249 : 37, 
16777223 : 119, 
16777223 : 119, 
16777237 : 116, 
16777233 : 115, 
16777216 : 9,  
16777264 : 67, 
16777273 : 76, 
16777274 : 95, 
16777275 : 96, 
16777265 : 68, 
16777266 : 69, 
16777267 : 70, 
16777268 : 71, 
16777269 : 72, 
16777270 : 73, 
16777271 : 74, 
16777272 : 75, 
16777232 : 110, 
16777222 : 118, 
16777234 : 113, 
16777253 : 77, 
16777239 : 117, 
16777238 : 112, 
16777344 : 127, 
16777236 : 114, 
16777254 : 78, 
16777248 : 50, 
16777248 : 50, 
16777235 : 111, 
16777250 : 133, 
16777219 : 22, 
}

KEY_BackSpace    = 0xff08
KEY_Tab          = 0xff09
KEY_Return       = 0xff0d
KEY_Escape       = 0xff1b
KEY_Insert       = 0xff63
KEY_Delete       = 0xffff
KEY_Home         = 0xff50
KEY_End          = 0xff57
KEY_PageUp       = 0xff55
KEY_PageDown     = 0xff56
KEY_Left         = 0xff51
KEY_Up           = 0xff52
KEY_Right        = 0xff53
KEY_Down         = 0xff54
KEY_F1           = 0xffbe
KEY_F2           = 0xffbf
KEY_F3           = 0xffc0
KEY_F4           = 0xffc1
KEY_F5           = 0xffc2
KEY_F6           = 0xffc3
KEY_F7           = 0xffc4
KEY_F8           = 0xffc5
KEY_F9           = 0xffc6
KEY_F10          = 0xffc7
KEY_F11          = 0xffc8
KEY_F12          = 0xffc9
KEY_F13          = 0xFFCA
KEY_F14          = 0xFFCB
KEY_F15          = 0xFFCC
KEY_F16          = 0xFFCD
KEY_F17          = 0xFFCE
KEY_F18          = 0xFFCF
KEY_F19          = 0xFFD0
KEY_F20          = 0xFFD1
KEY_ShiftLeft    = 0xffe1
KEY_ShiftRight   = 0xffe2
KEY_ControlLeft  = 0xffe3
KEY_ControlRight = 0xffe4
KEY_MetaLeft     = 0xffe7
KEY_MetaRight    = 0xffe8
KEY_AltLeft      = 0xffe9
KEY_AltRight     = 0xffea

KEY_Scroll_Lock  = 0xFF14
KEY_Sys_Req      = 0xFF15
KEY_Num_Lock     = 0xFF7F
KEY_Caps_Lock    = 0xFFE5
KEY_Pause        = 0xFF13
KEY_Super_L      = 0xFFEB
KEY_Super_R      = 0xFFEC
KEY_Hyper_L      = 0xFFED
KEY_Hyper_R      = 0xFFEE


keymap = {
    16777219: KEY_BackSpace,
    16777217: KEY_Tab, 
    16777220: KEY_Return, 
    16777216: KEY_Escape, 
    16777222: KEY_Insert, 
    16777223: KEY_Delete, 
    16777232: KEY_Home, 
    16777233: KEY_End, 
    16777238: KEY_PageUp, 
    16777239: KEY_PageDown, 
    16777234: KEY_Left, 
    16777235: KEY_Up, 
    16777236: KEY_Right, 
    16777237: KEY_Down, 
    16777264: KEY_F1,
    16777265: KEY_F2,
    16777266: KEY_F3,
    16777267: KEY_F4,
    16777268: KEY_F5,
    16777269: KEY_F6,
    16777270: KEY_F7,
    16777271: KEY_F8,
    16777272: KEY_F9,
    16777273: KEY_F10,
    16777274: KEY_F11,
    16777275: KEY_F12,
    16777276: KEY_F13,
    16777277: KEY_F14,
    16777278: KEY_F15,
    16777279: KEY_F16,
    16777280: KEY_F17,
    16777281: KEY_F18,
    16777282: KEY_F19,
    16777283: KEY_F20,

    16777254: KEY_Scroll_Lock,
    16777226: KEY_Sys_Req,
    16777253: KEY_Num_Lock,
    16777252: KEY_Caps_Lock,
    16777224: KEY_Pause,
    16777299: KEY_Super_L,
    16777300: KEY_Super_R,
    16777302: KEY_Hyper_L,
    16777303: KEY_Hyper_R}

#---------#
## Linux ##
#---------#
class x11_Mouse:
    def __init__(self):
        self.display   = Display( )
        
    def press(self, x, y, button=1):
        self.move(x, y)
        fake_input(self.display, X.ButtonPress, button_ids[button])
        self.display.sync( )

    def release(self, x, y, button=1):
        self.move(x, y)
        fake_input(self.display, X.ButtonRelease, button_ids[button])
        self.display.sync( )

    def move(self, x, y):
        #if (x, y) != self.position( ):
        fake_input(self.display, X.MotionNotify, x=x, y=y)
        self.display.sync( )

    def position(self):
        pos = self.display.screen( ).root.query_pointer( )._data
        return pos['root_x'], pos['root_y']

    def screen_size(self):
        width  = self.display.screen( ).width_in_pixels
        height = self.display.screen( ).height_in_pixels
        return width, heightwe

class x11_Keyboard: 
    def __init__(self):
        self.display = Display( )

    def press(self, key):
        keycode = CustomCodes[key]
        fake_input(self.window(), X.KeyPress, keycode)
        self.display.sync( )

    def release(self, key):
        keycode = CustomCodes[key]
        fake_input(self.window(), X.KeyRelease, keycode)
        self.display.sync( )

    def window(self):
        return self.display.get_input_focus( )._data['focus']


#------------#
## Mac OS X ##
#------------#
class PyMouse:
    def press(self, x, y, button=1):
        event = CGEventCreateMouseEvent(None,
                                        pressID[button],
                                        (x, y),
                                        button - 1)
        CGEventPost(kCGHIDEventTap, event)

    def release(self, x, y, button=1):
        event = CGEventCreateMouseEvent(None,
                                        releaseID[button],
                                        (x, y),
                                        button - 1)
        CGEventPost(kCGHIDEventTap, event)

    def move(self, x, y):
        move = CGEventCreateMouseEvent(None, kCGEventMouseMoved, (x, y), 0)
        CGEventPost(kCGHIDEventTap, move)

    def drag(self, x, y):
        drag = CGEventCreateMouseEvent(None, kCGEventLeftMouseDragged, (x, y), 0)
        CGEventPost(kCGHIDEventTap, drag)

    def position(self):
        loc = NSEvent.mouseLocation()
        return loc.x, CGDisplayPixelsHigh(0) - loc.y

    def screen_size(self):
        return CGDisplayPixelsWide(0), CGDisplayPixelsHigh(0)

class mac_Keyboard:
    def press(self, key):
        pass

    def release(self, key):
        pass

    def window(self):
        pass


#-----------#
## Windows ##
#-----------#
class win_Mouse:
    def press(self, x, y, button=1):
        buttonAction = 2 ** ((2 * button) - 1)
        self.move(x, y)
        win32api.mouse_event(buttonAction, x, y)

    def release(self, x, y, button=1):
        buttonAction = 2 ** ((2 * button))
        self.move(x, y)
        win32api.mouse_event(buttonAction, x, y)

    def move(self, x, y):
        windll.user32.SetCursorPos(x, y)

    def position(self):
        pt = POINT()
        windll.user32.GetCursorPos(byref(pt))
        return pt.x, pt.y

    def screen_size(self):
        width = windll.user32.GetSystemMetrics(0)
        height = windll.user32.GetSystemMetrics(1)
        return width, height

class win_Keyboard:
    def press(self, key):
        pass

    def release(self, key):
        pass

    def window(self):
        pass


#----------------------------------------------------------------#
## inherit the appropriate category based on system type,       ##
## so just needed import Mouse and Keyboard in our application, ##
#----------------------------------------------------------------# 
if platform == 'lin':
    class Mouse(x11_Mouse): pass
    class Keyboard(x11_Keyboard): pass

elif platform == 'mac':
    class Mouse(mac_Mouse):pass
    class Keyboard(mac_Keyboard): pass

elif platform == 'win':
    class Mouse(win_Mouse): pass
    class Keyboard(win_Keyboard): pass
