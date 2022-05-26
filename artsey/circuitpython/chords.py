
class KeyChord:
    def __init__(self, keyboard, match, result, releasekey = True):
        '''
        match: tuple of pins (0, 1)
        result: key Keycode.C
        '''
        self.match = sorted(match)
        self.result = result
        self.releasekey = releasekey
        self.keyboard = keyboard

    def isAMatch(self, chord):
        return self.match == chord

    def playResult(self):
        for key in self.result:
            self.keyboard.press(key)  # "Press"...
        if self.releasekey:
            self.keyboard.release_all()  # ..."Release"!

class MultiChord:
    def __init__(self, consumer_control, match, result):
        '''
        match: tuple of pins (0, 1)
        result: code ConsumerControlCode.BRIGHTNESS_DECREMENT
        '''
        self.match = sorted(match)
        self.result = result
        self.consumer_control = consumer_control

    def isAMatch(self, chord):
        return self.match == chord

    def playResult(self):
        for code in self.result:
            self.consumer_control.press(code)  # "Press"...
        self.consumer_control.release()  # ..."Release"!

class MouseChord:
    def __init__(self, mouse, match, result):
        '''
        match: tuple of pins (0, 1)
        result: code Mouse.LEFT_BUTTON
        '''
        self.match = sorted(match)
        self.result = result
        self.mouse = mouse

    def isAMatch(self, chord):
        return self.match == chord

    def playResult(self):
        for code in self.result:
            self.mouse.click(code)  # "Press"...

class MouseMove:
    def __init__(self, mouse, match, result):
        '''
        match: tuple of pins (0, 1)
        result: movement (x=-100, y=0, wheel=0)
        '''
        self.match = sorted(match)
        self.result = result
        self.mouse = mouse

    def isAMatch(self, chord):
        return self.match == chord

    def playResult(self):
        self.mouse.move(x=self.result[0], y=self.result[1], wheel=self.result[2])  # "Move"...