print("Starting setup...")

import board
import digitalio
import time
from adafruit_debouncer import Debouncer

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

from adafruit_hid.mouse import Mouse

class KeyChord:
    def __init__(self, match, result, releasekey = True):
        '''
        match: tuple of pins (0, 1)
        result: key Keycode.C
        '''
        self.match = sorted(match)
        self.result = result
        self.releasekey = releasekey

    def isAMatch(self, chord):
        return self.match == chord

    def playResult(self):
        for key in self.result:
            keyboard.press(key)  # "Press"...
        if self.releasekey:
            keyboard.release_all()  # ..."Release"!

class MultiChord:
    def __init__(self, match, result):
        '''
        match: tuple of pins (0, 1)
        result: code ConsumerControlCode.BRIGHTNESS_DECREMENT
        '''
        self.match = sorted(match)
        self.result = result

    def isAMatch(self, chord):
        return self.match == chord

    def playResult(self):
        for code in self.result:
            consumer_control.press(code)  # "Press"...
        consumer_control.release()  # ..."Release"!

class MouseChord:
    def __init__(self, match, result):
        '''
        match: tuple of pins (0, 1)
        result: code Mouse.LEFT_BUTTON
        '''
        self.match = sorted(match)
        self.result = result

    def isAMatch(self, chord):
        return self.match == chord

    def playResult(self):
        for code in self.result:
            mouse.click(code)  # "Press"...

class MouseMove:
    def __init__(self, match, result):
        '''
        match: tuple of pins (0, 1)
        result: movement (x=-100, y=0, wheel=0)
        '''
        self.match = sorted(match)
        self.result = result

    def isAMatch(self, chord):
        return self.match == chord

    def playResult(self):
        mouse.move(x=self.result[0], y=self.result[1], wheel=self.result[2])  # "Move"...

print("Defining key mapping...")
keypress_pins = [
    board.GP28,  board.GP27,  board.GP26, board.GP22,
    board.GP21,  board.GP20,  board.GP19, board.GP18,
]

chords = [
    # base layer chords
    [
        KeyChord((0,), (Keycode.A,)),
        KeyChord((1,), (Keycode.R,)),
        KeyChord((2,), (Keycode.T,)),
        KeyChord((3,), (Keycode.S,)),
        KeyChord((4,), (Keycode.E,)),
        KeyChord((5,), (Keycode.Y,)),
        KeyChord((6,), (Keycode.I,)),
        KeyChord((7,), (Keycode.O,)),

        KeyChord((4, 7), (Keycode.B,)),
        KeyChord((4, 5), (Keycode.C,)),
        KeyChord((0, 1, 2), (Keycode.D,)),
        KeyChord((0, 1), (Keycode.F,)),
        KeyChord((1, 2), (Keycode.G,)),
        KeyChord((4, 6), (Keycode.H,)),
        KeyChord((2, 3), (Keycode.J,)),
        KeyChord((5, 7), (Keycode.K,)),
        KeyChord((4, 5, 6), (Keycode.L,)),
        KeyChord((5, 6, 7), (Keycode.M,)),
        KeyChord((6, 7), (Keycode.N,)),
        KeyChord((4, 6, 7), (Keycode.P,)),
        KeyChord((0, 2, 3), (Keycode.Q,)),
        KeyChord((5, 6), (Keycode.U,)),
        KeyChord((1, 3), (Keycode.V,)),
        KeyChord((0, 3), (Keycode.W,)),
        KeyChord((1, 2, 3), (Keycode.X,)),
        KeyChord((0, 1, 2, 3), (Keycode.Z,)),

        KeyChord((0, 4), (Keycode.ENTER,)),
        KeyChord((0, 5, 6), (Keycode.QUOTE,)),
        KeyChord((0, 5), (Keycode.PERIOD,)),
        KeyChord((0, 6), (Keycode.COMMA,)),
        KeyChord((0, 7), (Keycode.FORWARD_SLASH,)),
        KeyChord((2, 6), (Keycode.SHIFT, Keycode.ONE,)),
        KeyChord((4, 5, 6, 7), (Keycode.SPACE,)),
        KeyChord((4, 1), (Keycode.BACKSPACE,)),
        KeyChord((1, 6), (Keycode.DELETE,)),

        KeyChord((0, 1, 7), (Keycode.ESCAPE,)),
        KeyChord((0, 1, 2, 7), (Keycode.TAB,)),
        KeyChord((4, 3), (Keycode.CONTROL,), False),
        KeyChord((5, 3), (Keycode.GUI,), False),
        KeyChord((6, 3), (Keycode.ALT,), False),
        KeyChord((4, 1, 2, 3), (Keycode.SHIFT,), False),
        #KeyChord((1, 5), (Keycode.SHIFT,)), # no idea what this means
        #KeyChord((0, 5, 6, 7), (Keycode.CAPS_LOCK,)), # doesnt want to work
        #Chord((1, 2, 5, 6), (Keycode.NO,)),  # no standard us code for bluetooth
    ],
 
    #parenLayer
    [
        KeyChord((1,), (Keycode.SHIFT, Keycode.NINE,)),
        KeyChord((2,), (Keycode.SHIFT, Keycode.ZERO,)),
        KeyChord((3,), (Keycode.SHIFT, Keycode.LEFT_BRACKET,)),
        KeyChord((5,), (Keycode.LEFT_BRACKET,)),
        KeyChord((6,), (Keycode.RIGHT_BRACKET,)),
        KeyChord((7,), (Keycode.SHIFT, Keycode.RIGHT_BRACKET,)),
    ],

    #numberlayer
    [
        KeyChord((0,), (Keycode.ONE,)),
        KeyChord((1,), (Keycode.TWO,)),
        KeyChord((2,), (Keycode.THREE,)),
        KeyChord((4,), (Keycode.FOUR,)),
        KeyChord((5,), (Keycode.FIVE,)),
        KeyChord((6,), (Keycode.SIX,)),
        KeyChord((0,1), (Keycode.SEVEN,)),
        KeyChord((1,2), (Keycode.EIGHT,)),
        KeyChord((4,5), (Keycode.NINE,)),
        KeyChord((5,6), (Keycode.ZERO,)),
    ],

    #symbollayer
    [
        KeyChord((0,), (Keycode.SHIFT, Keycode.ONE)),
        KeyChord((1,), (Keycode.BACKSLASH,)),
        KeyChord((2,), (Keycode.SEMICOLON,)),
        KeyChord((3,), (Keycode.GRAVE_ACCENT,)),
        KeyChord((5,), (Keycode.SHIFT, Keycode.FORWARD_SLASH,)),
        KeyChord((6,), (Keycode.MINUS,)),
        KeyChord((7,), (Keycode.EQUALS,)),
    ],

    #multimedialayer
    [
        MultiChord((0,), (ConsumerControlCode.PLAY_PAUSE,)),
        KeyChord((1,), (Keycode.INSERT,)),
        MultiChord((2,), (ConsumerControlCode.VOLUME_INCREMENT,)),
        KeyChord((4,), (Keycode.RIGHT_SHIFT,)),
        KeyChord((5,), (Keycode.PRINT_SCREEN,)),
        MultiChord((6,), (ConsumerControlCode.VOLUME_DECREMENT,)),
    ],

    #mouselayer
    [
        MouseChord((0,), (Mouse.LEFT_BUTTON,)),
        MouseMove((1,), (0, -20, 0)), #up
        MouseChord((2,), (Mouse.RIGHT_BUTTON,)),
        MouseMove((3,), (0, 0, 10)), #scroll away
        MouseMove((4,), (-20, 0, 0)), #left
        MouseMove((5,), (0, 20, 0)), #down
        MouseMove((6,), (20, 0, 0)), #right
        MouseMove((7,), (0, 0, -10)), #scroll toward
    ],

    #navlayer
    [
        KeyChord((0,), (Keycode.HOME,)),
        KeyChord((1,), (Keycode.UP_ARROW,)),
        KeyChord((2,), (Keycode.END,)),
        KeyChord((3,), (Keycode.PAGE_UP,)),
        KeyChord((4,), (Keycode.LEFT_ARROW,)),
        KeyChord((5,), (Keycode.DOWN_ARROW,)),
        KeyChord((6,), (Keycode.RIGHT_ARROW,)),
        KeyChord((7,), (Keycode.PAGE_DOWN,)),
    ],
]
print("Doing final configuration...")
mouselockchord = (0,2,5)
navlockchord = (1,4,6)

# The keyboard object!
time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)
consumer_control = ConsumerControl(usb_hid.devices)
mouse = Mouse(usb_hid.devices)

# Make all pin objects inputs with pullups
switches = []
for pin in keypress_pins:
    key_pin = digitalio.DigitalInOut(pin)
    key_pin.direction = digitalio.Direction.INPUT
    key_pin.pull = digitalio.Pull.UP
    switches.append(Debouncer(key_pin))


chord = ()
layer_hold_time = 0.25
current_layer = 0

startTime = time.monotonic()
layering = False

held_keys = 0
chording = False

print("Setup complete. Get CLACK-A-LACK-ING!")
while True: #main loop

    #update all the switch states
    for switch in switches:
        switch.update()
        if switch.fell:
            i = switches.index(switch)
            startTime = time.monotonic()
            chording = True
            chord = chord + (i,)
            held_keys += 1
        if switch.rose:
            held_keys -= 1

    #if a chord is in progress
    if chording:
        if held_keys == 0:
            pressedChord = sorted(chord)
            for chord in chords[current_layer]:
                if chord.isAMatch(pressedChord):
                    chord.playResult()
                    break

            #check for mouse/nav lock
            if pressedChord == sorted(mouselockchord): #mouselock
                if current_layer != 5:
                    current_layer = 5
                    print("Seting layer to", current_layer)
                else:
                    current_layer = 0
                    print("Seting layer to", current_layer)
            if pressedChord == sorted(navlockchord): #navlock
                if current_layer != 6:
                    current_layer = 6
                    print("Seting layer to", current_layer)
                else:
                    current_layer = 0
                    print("Seting layer to", current_layer)

            chord = ()
            chording = False

        #if currently using a layer
        if held_keys == 1 and layering:
            pressedChord = sorted(chord)
            for chord in chords[current_layer]:
                if chord.isAMatch(pressedChord):
                    chord.playResult()
                    break

            chord = ()
            chording = False

    #check if a layer is instead being attempted
    if held_keys == 1 and chording == True and time.monotonic() - startTime > layer_hold_time:
        # layer button has been held long enough
        layering = True
        if chord == (0,):
            current_layer = 1
            print("Seting layer to", current_layer)
        if chord == (3,):
            current_layer = 2
            print("Seting layer to", current_layer)
        if chord == (4,):
            current_layer = 3
            print("Seting layer to", current_layer)
        if chord == (7,):
            current_layer = 4
            print("Seting layer to", current_layer)
        chord = ()

    #and stop layering when the button's released
    if layering and held_keys == 0:
        layering = False
        current_layer = 0
        print("Seting layer to", current_layer)

    time.sleep(0.01)
