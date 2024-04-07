from mc.net.minecraft.client.KeyBinding import KeyBinding
from pyglet import window

import pathlib
import sys
import os

if 'win' in sys.platform:
    metaKeys = (window.key.LWINDOWS, window.key.RWINDOWS)
elif 'mac' in sys.platform or 'darwin' in sys.platform:
    metaKeys = (window.key.LOPTION, window.key.ROPTION)
else:
    metaKeys = (window.key.LMETA, window.key.RMETA)

_KEYS = {
    1: window.key.ESCAPE,
    2: window.key._1,
    3: window.key._2,
    4: window.key._3,
    5: window.key._4,
    6: window.key._5,
    7: window.key._6,
    8: window.key._7,
    9: window.key._8,
    10: window.key._9,
    11: window.key._0,
    12: window.key.MINUS,
    13: window.key.EQUAL,
    14: window.key.BACKSPACE,
    15: window.key.TAB,
    16: window.key.Q,
    17: window.key.W,
    18: window.key.E,
    19: window.key.R,
    20: window.key.T,
    21: window.key.Y,
    22: window.key.U,
    23: window.key.I,
    24: window.key.O,
    25: window.key.P,
    26: window.key.BRACKETLEFT,
    27: window.key.BRACKETRIGHT,
    28: window.key.RETURN,
    29: window.key.LCTRL,
    30: window.key.A,
    31: window.key.S,
    32: window.key.D,
    33: window.key.F,
    34: window.key.G,
    35: window.key.H,
    36: window.key.J,
    37: window.key.K,
    38: window.key.L,
    39: window.key.SEMICOLON,
    40: window.key.APOSTROPHE,
    41: window.key.GRAVE,
    42: window.key.LSHIFT,
    43: window.key.BACKSLASH,
    44: window.key.Z,
    45: window.key.X,
    46: window.key.C,
    47: window.key.V,
    48: window.key.B,
    49: window.key.N,
    50: window.key.M,
    51: window.key.COMMA,
    52: window.key.PERIOD,
    53: window.key.SLASH,
    54: window.key.RSHIFT,
    55: window.key.ASTERISK,
    56: window.key.LALT,
    57: window.key.SPACE,
    58: window.key.CAPSLOCK,
    59: window.key.F1,
    60: window.key.F2,
    61: window.key.F3,
    62: window.key.F4,
    63: window.key.F5,
    64: window.key.F6,
    65: window.key.F7,
    66: window.key.F8,
    67: window.key.F9,
    68: window.key.F10,
    69: window.key.NUMLOCK,
    70: window.key.SCROLLLOCK,
    71: window.key.NUM_7,
    72: window.key.NUM_8,
    73: window.key.NUM_9,
    74: window.key.NUM_SUBTRACT,
    75: window.key.NUM_4,
    76: window.key.NUM_5,
    77: window.key.NUM_6,
    78: window.key.NUM_ADD,
    79: window.key.NUM_1,
    80: window.key.NUM_2,
    81: window.key.NUM_3,
    82: window.key.NUM_0,
    83: window.key.NUM_DECIMAL,
    87: window.key.F11,
    88: window.key.F12,
    100: window.key.F13,
    101: window.key.F14,
    102: window.key.F15,
    103: window.key.F16,
    104: window.key.F17,
    105: window.key.F18,
    113: window.key.F19,
    141: window.key.NUM_EQUAL,
    145: window.key.AT,
    146: window.key.COLON,
    147: window.key.UNDERSCORE,
    156: window.key.NUM_ENTER,
    157: window.key.RCTRL,
    179: window.key.COMMA,
    181: window.key.NUM_DIVIDE,
    183: window.key.SYSREQ,
    184: window.key.RALT,
    196: window.key.FUNCTION,
    197: window.key.PAUSE,
    199: window.key.HOME,
    200: window.key.UP,
    201: window.key.NUM_PRIOR,
    203: window.key.LEFT,
    205: window.key.RIGHT,
    207: window.key.END,
    208: window.key.DOWN,
    209: window.key.NUM_NEXT,
    210: window.key.INSERT,
    211: window.key.DELETE,
    218: window.key.CLEAR,
    219: metaKeys[0],
    220: metaKeys[1]
}
_GL_KEYS = {v: k for k, v in _KEYS.items()}

class GameSettings:
    __RENDER_DISTANCES = ('FAR', 'NORMAL', 'SHORT', 'TINY')
    __music = True
    __sound = True
    invertMouse = False
    showFPS = False
    renderDistance = 0
    viewBobbing = True
    anaglyph = False
    limitFramerate = False
    numberOfOptions = 8

    def __init__(self, mc, file):
        self.keyBindForward = KeyBinding('Forward', window.key.W)
        self.keyBindLeft = KeyBinding('Left', window.key.A)
        self.keyBindBack = KeyBinding('Back', window.key.S)
        self.keyBindRight = KeyBinding('Right', window.key.D)
        self.keyBindJump = KeyBinding('Jump', window.key.SPACE)
        self.keyBindInventory = KeyBinding('Inventory', window.key.I)
        self.keyBindDrop = KeyBinding('Drop', window.key.Q)
        self.keyBindChat = KeyBinding('Chat', window.key.T)
        self.keyBindToggleFog = KeyBinding('Toggle fog', window.key.F)
        self.keyBindSave = KeyBinding('Save location', window.key.RETURN)
        self.keyBindLoad = KeyBinding('Load location', window.key.R)
        self.keyBindings = [self.keyBindForward, self.keyBindLeft, self.keyBindBack,
                            self.keyBindRight, self.keyBindJump, self.keyBindDrop,
                            self.keyBindInventory, self.keyBindChat, self.keyBindToggleFog,
                            self.keyBindSave, self.keyBindLoad]
        self.__mc = mc
        self.__optionsFile = (pathlib.Path(file) / 'options.txt').resolve()
        self.__loadOptions()

    def setKeyBindingString(self, i):
        return self.keyBindings[i].keyDescription + ': ' + window.key.symbol_string(self.keyBindings[i].keyCode)

    def setKeyBinding(self, i, key):
        self.keyBindings[i].keyCode = key
        self.__saveOptions()

    def setOptionValue(self, option, arg):
        if option == 0:
            self.__music = not self.__music
        elif option == 1:
            self.__sound = not self.__sound
        elif option == 2:
            self.invertMouse = not self.invertMouse
        elif option == 3:
            self.showFPS = not self.showFPS
        elif option == 4:
            self.renderDistance = self.renderDistance + arg & 3
        elif option == 5:
            self.viewBobbing = not self.viewBobbing
        elif option == 6:
            self.anaglyph = not self.anaglyph
            self.__mc.renderEngine.refreshTextures()
        elif option == 7:
            self.limitFramerate = not self.limitFramerate

        self.__saveOptions()

    def setOptionString(self, option):
        if option == 0:
            return 'Music: ' + ('ON' if self.__music else 'OFF')
        elif option == 1:
            return 'Sound: ' + ('ON' if self.__sound else 'OFF')
        elif option == 2:
            return 'Invert mouse: ' + ('ON' if self.invertMouse else 'OFF')
        elif option == 3:
            return 'Show FPS: ' + ('ON' if self.showFPS else 'OFF')
        elif option == 4:
            return 'Render distance: ' + GameSettings.__RENDER_DISTANCES[self.renderDistance]
        elif option == 5:
            return 'View bobbing: ' + ('ON' if self.viewBobbing else 'OFF')
        elif option == 6:
            return '3d anaglyph: ' + ('ON' if self.anaglyph else 'OFF')
        elif option == 7:
            return 'Limit framerate: ' + ('ON' if self.limitFramerate else 'OFF')

        return ''

    def __loadOptions(self):
        try:
            if self.__optionsFile.exists():
                with open(self.__optionsFile, 'r') as f:
                    lines = f.read()
                    for line in lines.split('\n'):
                        split = line.split(':')
                        if split[0] == 'music':
                            self.__music = split[1] == 'true'
                        elif split[0] == 'sound':
                            self.__sound = split[1] == 'true'
                        elif split[0] == 'invertYMouse':
                            self.invertMouse = split[1] == 'true'
                        elif split[0] == 'showFrameRate':
                            self.showFPS = split[1] == 'true'
                        elif split[0] == 'viewDistance':
                            self.renderDistance = int(split[1])
                        elif split[0] == 'bobView':
                            self.viewBobbing = split[1] == 'true'
                        elif split[0] == 'anaglyph3d':
                            self.anaglyph = split[1] == 'true'
                        elif split[0] == 'limitFramerate':
                            self.limitFramerate = split[1] == 'true'

                        for binding in self.keyBindings:
                            if split[0] == 'key_' + binding.keyDescription:
                                binding.keyCode = _KEYS[int(split[1])]
        except Exception as e:
            print('Failed to load options:', e)

    def __saveOptions(self):
        try:
            with open(self.__optionsFile, 'w+') as f:
                f.write('music:' + ('true' if self.__music else 'false') + '\n')
                f.write('sound:' + ('true' if self.__sound else 'false') + '\n')
                f.write('invertYMouse:' + ('true' if self.invertMouse else 'false') + '\n')
                f.write('showFrameRate:' + ('true' if self.showFPS else 'false') + '\n')
                f.write('viewDistance:' + str(self.renderDistance) + '\n')
                f.write('bobView:' + ('true' if self.viewBobbing else 'false') + '\n')
                f.write('anaglyph3d:' + ('true' if self.anaglyph else 'false') + '\n')
                f.write('limitFramerate:' + ('true' if self.limitFramerate else 'false') + '\n')

                for binding in self.keyBindings:
                    f.write('key_' + binding.keyDescription + ':' + str(_GL_KEYS[binding.keyCode]) + '\n')
        except Exception as e:
            print('Failed to save options:', e)
