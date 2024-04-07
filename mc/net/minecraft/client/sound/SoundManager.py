from mc.net.minecraft.client.sound.SoundPool import SoundPool

import collections
import traceback
import pyglet
import math
import os

class SoundManager:
    CHANNELS = 28
    players = collections.deque([pyglet.media.Player() for _ in range(CHANNELS)],
                                maxlen=CHANNELS)
    listener = pyglet.media.get_audio_driver().get_listener()
    __musicStream = None
    __supported = True
    __soundPoolSounds = SoundPool()
    __soundPoolMusic = SoundPool()
    __latestSoundID = 0

    def loadSoundSettings(self):
        try:
            import pyogg
        except:
            print('PyOGG is not available. PyOGG is recommended for audio support.')
            gstreamer = False
            if pyglet.compat_platform.startswith('linux'):
                try:
                    from gi.repository import Gst, GLib
                except:
                    pass
                else:
                    gstreamer = True

            if pyglet.media.have_ffmpeg():
                print('Using FFMPEG codec instead.')
            else:
                if pyglet.compat_platform.startswith('linux'):
                    if gstreamer:
                        print('Using gst-python audio library.')
                    else:
                        print('Alternate codecs FFMPEG and gst-python are also missing. Audio is not supported.')
                        self.__supported = False
                else:
                    print('FFMPEG is additionally missing. Audio is not supported.')
                    self.__supported = False

        if not self.__supported:
            return

        for root, dirs, files in os.walk(os.path.join(pyglet.resource.get_script_home(), os.path.sep.join(pyglet.resource.path))):
            for fileName in files:
                if fileName[-4:] != '.ogg':
                    continue

                folder = os.path.basename(root)
                if folder == 'music':
                    self.addMusic(fileName, os.path.join(root, fileName))
                else:
                    self.addSound(os.path.join(folder, fileName).replace('\\', '/'),
                                  os.path.join(root, fileName))

    def closeMinecraft(self):
        if self.__musicStream and self.__musicStream._source:
            self.__musicStream.pause()
            self.__musicStream = None
        for player in self.players:
            player.delete()

    def addSound(self, sound, file):
        self.__soundPoolSounds.getFolder(sound, file)

    def addMusic(self, music, file):
        self.__soundPoolMusic.getFolder(music, file)
        if self.__supported and (not self.__musicStream or not self.__musicStream._source) and \
           self.__soundPoolMusic.numberOfSoundPoolEntries == 3:
            entry = self.__soundPoolMusic.getRandomSoundFromSoundPool('calm')
            self.__musicStream = pyglet.media.load(entry.soundUrl).play()

    def setListener(self, listener, partialTick):
        if not listener:
            return

        pitch = listener.prevRotationPitch + (listener.rotationPitch - listener.prevRotationPitch) * partialTick
        yaw = listener.prevRotationYaw + (listener.rotationYaw - listener.prevRotationYaw) * partialTick
        x = listener.prevPosX + (listener.posX - listener.prevPosX) * partialTick
        y = listener.prevPosY + (listener.posY - listener.prevPosY) * partialTick
        z = listener.prevPosZ + (listener.posZ - listener.prevPosZ) * partialTick
        upX = math.sin(-yaw * (math.pi / 180.0) - math.pi)
        upY = math.cos(-pitch * (math.pi / 180.0))
        upZ = math.cos(-yaw * (math.pi / 180.0) - math.pi)
        lookX = upX * upY
        lookY = math.sin(-pitch * (math.pi / 180.0))
        lookZ = upZ * upY
        upX *= lookY
        upZ *= lookY
        self.listener.position = (x, y, z)
        self.listener.forward_orientation = (lookX, lookY, lookZ)
        self.listener.up_orientation = (upX, upY, upZ)

    def playSoundAtPos(self, sound, x, y, z, volume, pitch):
        entry = self.__soundPoolSounds.getRandomSoundFromSoundPool(sound)
        if not entry or not self.__supported or not self.players:
            return

        self.__latestSoundID = (self.__latestSoundID + 1) % 256

        xd = x - self.listener.position[0]
        yd = y - self.listener.position[1]
        zd = z - self.listener.position[2]
        distanceFromListener = math.sqrt(xd * xd + yd * yd + zd * zd)
        distOrRoll = 16.0
        if distanceFromListener <= 0:
            gain = 1.0
        elif distanceFromListener >= distOrRoll:
            gain = 0.0
        else:
            gain = 1.0 - (distanceFromListener / distOrRoll)

        if gain > 1.0:
            gain = 1.0
        if gain < 0.0:
            gain = 0.0

        player = self.players[0]
        player.min_distance = 0.0
        player.max_distance = distOrRoll
        player.position = (x, y, z)
        player.cone_orientation = (0, 0, 0)
        player.cone_outer_gain = 0.0
        player.pitch = pitch
        player.volume = gain * volume
        player.seek(0.0)
        player.queue(entry.stream)
        if player.playing:
            player.next_source()
        else:
            player.play()
            try: player._audio_player.alsource.rolloff_factor = 0.0
            except: pass
        self.players.rotate()

    def playSound(self, sound, volume, pitch):
        entry = self.__soundPoolSounds.getRandomSoundFromSoundPool(sound)
        if not entry or not self.__supported or not self.players:
            return

        self.__latestSoundID = (self.__latestSoundID + 1) % 256

        player = self.players[0]
        player.min_distance = 0.0
        player.max_distance = 100000000.
        player.position = (0.0, 0.0, 0.0)
        player.cone_orientation = (0, 0, 0)
        player.cone_outer_gain = 0.0
        player.pitch = 1.0
        player.volume = 1.0
        player.seek(0.0)
        player.queue(entry.stream)
        if player.playing:
            player.next_source()
        else:
            player.play()
            try: player._audio_player.alsource.rolloff_factor = 0.0
            except: pass
        self.players.rotate()
