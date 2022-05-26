print("Starting setup...")

import board
import digitalio
import time
from adafruit_debouncer import Debouncer

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

from adafruit_hid.mouse import Mouse
from chords import KeyChord, MouseChord, MouseMove, MultiChord

print("Defining key mapping...")
keypress_pins = [
    board.GP28,  board.GP27,  board.GP26, board.GP22,
    board.GP21,  board.GP20,  board.GP19, board.GP18,
]

# The keyboard object!
time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems
kb = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)
m = Mouse(usb_hid.devices)

# The Artsey buttons are layed out like so:
# +------+---+---+---+---+
# |  RP  | 0 | 1 | 2 | 3 |
# |  PI  +---+---+---+---+
# |  CO  | 4 | 5 | 6 | 7 |
# +------+---+---+---+---+

# Define new chords by adding a new line to any layer list like so:
# ChordType(inputType, (pin, ...), (result, ...)),
# where ChordType = KeyChord for normal keyboard buttons, MouseChord for mouse buttons,
#                   MouseMove for mouse movements and MultiChord for multimedia buttons
#       inputType = kb (keyboard for KeyChords), cc (consumerControl for MultiChord), m (mouse for mouse stuff)
#       pin = one or more pins (comma seperated) that make up the chord
#       result = the result of pressing the chord, Keycode (for keyboard buttons, these can be chained together), 
#                   ConsumerControlCode (for multimedia buttons, also chainable),
#                   Mouse (for mouse buttons) or
#                   h, v, wheel values for mouse movement
#
# For example:
# KeyChord(kb, (0,), (Keycode.A,)),         # Pressing the top left button results in keyboard 'A' button being pressed
# KeyChord(kb, (0, 1, 2), (Keycode.D,)),    # Pressing the first 3 buttons on the top row results in keyboard button 'D'
# KeyChord(kb, (2, 6), (Keycode.SHIFT, Keycode.ONE,)),      # This results in '!' by having both SHIFT and the number 1 be pressed
# MultiChord(cc, (0,), (ConsumerControlCode.PLAY_PAUSE,)),  # Results in multimedia button Play/Pause press
# MouseChord(m, (0,), (Mouse.LEFT_BUTTON,)),                # Results in the left mouse button being clicked
# MouseMove(m, (4,), (-20, 0, 0)),             # Moves the mouse 20 pixels to the left. Negative numbers for up/left/scrolldown

chords = [
    # base layer chords
    [
        KeyChord(kb, (0,), (Keycode.A,)),
        KeyChord(kb, (1,), (Keycode.R,)),
        KeyChord(kb, (2,), (Keycode.T,)),
        KeyChord(kb, (3,), (Keycode.S,)),
        KeyChord(kb, (4,), (Keycode.E,)),
        KeyChord(kb, (6,), (Keycode.I,)),
        KeyChord(kb, (7,), (Keycode.O,)),
        KeyChord(kb, (5,), (Keycode.Y,)),

        KeyChord(kb, (4, 7), (Keycode.B,)),
        KeyChord(kb, (4, 5), (Keycode.C,)),
        KeyChord(kb, (0, 1, 2), (Keycode.D,)),
        KeyChord(kb, (0, 1), (Keycode.F,)),
        KeyChord(kb, (1, 2), (Keycode.G,)),
        KeyChord(kb, (4, 6), (Keycode.H,)),
        KeyChord(kb, (2, 3), (Keycode.J,)),
        KeyChord(kb, (5, 7), (Keycode.K,)),
        KeyChord(kb, (4, 5, 6), (Keycode.L,)),
        KeyChord(kb, (5, 6, 7), (Keycode.M,)),
        KeyChord(kb, (6, 7), (Keycode.N,)),
        KeyChord(kb, (4, 6, 7), (Keycode.P,)),
        KeyChord(kb, (0, 2, 3), (Keycode.Q,)),
        KeyChord(kb, (5, 6), (Keycode.U,)),
        KeyChord(kb, (1, 3), (Keycode.V,)),
        KeyChord(kb, (0, 3), (Keycode.W,)),
        KeyChord(kb, (1, 2, 3), (Keycode.X,)),
        KeyChord(kb, (0, 1, 2, 3), (Keycode.Z,)),

        KeyChord(kb, (0, 4), (Keycode.ENTER,)),
        KeyChord(kb, (0, 5, 6), (Keycode.QUOTE,)),
        KeyChord(kb, (0, 5), (Keycode.PERIOD,)),
        KeyChord(kb, (0, 6), (Keycode.COMMA,)),
        KeyChord(kb, (0, 7), (Keycode.FORWARD_SLASH,)),
        KeyChord(kb, (2, 6), (Keycode.SHIFT, Keycode.ONE,)),
        KeyChord(kb, (4, 5, 6, 7), (Keycode.SPACE,)),
        KeyChord(kb, (4, 1), (Keycode.BACKSPACE,)),
        KeyChord(kb, (1, 6), (Keycode.DELETE,)),

        KeyChord(kb, (0, 1, 7), (Keycode.ESCAPE,)),
        KeyChord(kb, (0, 1, 2, 7), (Keycode.TAB,)),
        KeyChord(kb, (4, 3), (Keycode.CONTROL,), False),
        KeyChord(kb, (5, 3), (Keycode.GUI,), False),
        KeyChord(kb, (6, 3), (Keycode.ALT,), False),
        KeyChord(kb, (4, 1, 2, 3), (Keycode.SHIFT,), False),
        #KeyChord(kb, (1, 5), (Keycode.SHIFT,)), # no idea what this means
        #KeyChord(kb, (0, 5, 6, 7), (Keycode.CAPS_LOCK,)), # doesnt want to work
        #KeyChord(kb, (1, 2, 5, 6), (Keycode.NO,)),  # no standard us code for bluetooth
    ],
 
    #parenLayer
    [
        KeyChord(kb, (1,), (Keycode.SHIFT, Keycode.NINE,)),
        KeyChord(kb, (2,), (Keycode.SHIFT, Keycode.ZERO,)),
        KeyChord(kb, (3,), (Keycode.SHIFT, Keycode.LEFT_BRACKET,)),
        KeyChord(kb, (5,), (Keycode.LEFT_BRACKET,)),
        KeyChord(kb, (6,), (Keycode.RIGHT_BRACKET,)),
        KeyChord(kb, (7,), (Keycode.SHIFT, Keycode.RIGHT_BRACKET,)),
    ],

    #numberlayer
    [
        KeyChord(kb, (0,), (Keycode.ONE,)),
        KeyChord(kb, (1,), (Keycode.TWO,)),
        KeyChord(kb, (2,), (Keycode.THREE,)),
        KeyChord(kb, (4,), (Keycode.FOUR,)),
        KeyChord(kb, (5,), (Keycode.FIVE,)),
        KeyChord(kb, (6,), (Keycode.SIX,)),
        KeyChord(kb, (0,1), (Keycode.SEVEN,)),
        KeyChord(kb, (1,2), (Keycode.EIGHT,)),
        KeyChord(kb, (4,5), (Keycode.NINE,)),
        KeyChord(kb, (5,6), (Keycode.ZERO,)),
    ],

    #symbollayer
    [
        KeyChord(kb, (0,), (Keycode.SHIFT, Keycode.ONE)),
        KeyChord(kb, (1,), (Keycode.BACKSLASH,)),
        KeyChord(kb, (2,), (Keycode.SEMICOLON,)),
        KeyChord(kb, (3,), (Keycode.GRAVE_ACCENT,)),
        KeyChord(kb, (5,), (Keycode.SHIFT, Keycode.FORWARD_SLASH,)),
        KeyChord(kb, (6,), (Keycode.MINUS,)),
        KeyChord(kb, (7,), (Keycode.EQUALS,)),
    ],

    #multimedialayer
    [
        MultiChord(cc, (0,), (ConsumerControlCode.PLAY_PAUSE,)),
        KeyChord(kb, (1,), (Keycode.INSERT,)),
        MultiChord(cc, (2,), (ConsumerControlCode.VOLUME_INCREMENT,)),
        KeyChord(kb, (4,), (Keycode.RIGHT_SHIFT,)),
        KeyChord(kb, (5,), (Keycode.PRINT_SCREEN,)),
        MultiChord(cc, (6,), (ConsumerControlCode.VOLUME_DECREMENT,)),
    ],

    #mouselayer
    [
        MouseChord(m, (0,), (Mouse.LEFT_BUTTON,)),
        MouseMove(m, (1,), (0, -20, 0)), #up
        MouseChord(m, (2,), (Mouse.RIGHT_BUTTON,)),
        MouseMove(m, (3,), (0, 0, 10)), #scroll away
        MouseMove(m, (4,), (-20, 0, 0)), #left
        MouseMove(m, (5,), (0, 20, 0)), #down
        MouseMove(m, (6,), (20, 0, 0)), #right
        MouseMove(m, (7,), (0, 0, -10)), #scroll toward
    ],

    #navlayer
    [
        KeyChord(kb, (0,), (Keycode.HOME,)),
        KeyChord(kb, (1,), (Keycode.UP_ARROW,)),
        KeyChord(kb, (2,), (Keycode.END,)),
        KeyChord(kb, (3,), (Keycode.PAGE_UP,)),
        KeyChord(kb, (4,), (Keycode.LEFT_ARROW,)),
        KeyChord(kb, (5,), (Keycode.DOWN_ARROW,)),
        KeyChord(kb, (6,), (Keycode.RIGHT_ARROW,)),
        KeyChord(kb, (7,), (Keycode.PAGE_DOWN,)),
    ],
]
print("Doing final configuration...")
mouselockchord = (0,2,5)
navlockchord = (1,4,6)

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
