from mc.net.minecraft.sound.SoundInfo import SoundInfo
from mc.CompatibilityShims import getMillis
from pyglet import media

import traceback
import random
import math

class SoundManager:
    sounds = {}
    __music = {}
    random = random.Random()
    lastMusic = getMillis() + 60000

    def getAudioInfo(self, sound, volume, pitch):
        l = self.sounds.get(sound)
        if l:
            return SoundInfo(l[math.floor(self.random.random() * len(l))], pitch, volume)
        else:
            return None

    def registerSound(self, file, sound):
        try:
            sound = sound[0:-4].replace('/', '.')
            while sound[-1].isdigit():
                sound = sound[0:-1]

            stream = media.load(file, streaming=False)
            soundInfo = self.sounds.get(sound)
            if not soundInfo:
                soundInfo = []
                self.sounds[sound] = soundInfo

            self.sounds[sound].append(stream)
        except:
            print(traceback.format_exc())

    def registerMusic(self, file, music):
        music = music[0:-4].replace('/', '.')
        while music[-1].isdigit():
            music = music[0:-1]

        soundInfo = self.__music.get(music)
        if not soundInfo:
            soundInfo = []
            self.__music[music] = soundInfo

        self.__music[music].append(file)

    def playMusic(self, soundPlayer, music):
        l = self.__music.get(music)

        if l and soundPlayer.enabled and soundPlayer.supported:
            file = l[math.floor(self.random.random() * len(l))]
            media.load(file).play()
            return True
        else:
            return False
