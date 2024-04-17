from mc.net.minecraft.client.sound.SoundPoolEntry import SoundPoolEntry

import random

class SoundPool:

    def __init__(self):
        self.__nameToSoundPoolEntriesMapping = {}
        self.numberOfSoundPoolEntries = 0

    def addSound(self, soundUrl, file):
        try:
            sound = soundUrl[0:-4].replace('/', '.')
            while sound[-1].isdigit():
                sound = sound[0:-1]

            if sound not in self.__nameToSoundPoolEntriesMapping:
                self.__nameToSoundPoolEntriesMapping[sound] = []

            entry = SoundPoolEntry(soundUrl, file)
            self.__nameToSoundPoolEntriesMapping[sound].append(entry)
            self.numberOfSoundPoolEntries += 1
            return entry
        except Exception as e:
            raise RuntimeError(e)

    def getRandomSoundFromSoundPool(self, name):
        entries = self.__nameToSoundPoolEntriesMapping.get(name)
        return entries[int(random.random() * len(entries))] if entries else None
