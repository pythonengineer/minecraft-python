import pyglet
import math

class SoundPlayer:
    player = None
    listener = None
    entity = None
    enabled = True
    supported = True

    def __init__(self):
        try:
            import pyogg
            return
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
                    self.supported = False
            else:
                print('FFMPEG is additionally missing. Audio is not supported.')
                self.supported = False

    def setListener(self, listener, partialTick):
        if not listener:
            return

        yaw = listener.yRotO + (listener.yRot - listener.yRotO) * partialTick
        x = listener.xo + (listener.x - listener.xo) * partialTick
        y = listener.yo + (listener.y - listener.yo) * partialTick
        z = listener.zo + (listener.z - listener.zo) * partialTick
        lookX = -math.sin(math.radians(-yaw) - math.pi)
        lookY = 0.0
        lookZ = -math.cos(math.radians(-yaw) - math.pi)
        upX = 0.0
        upY = 0.0
        upZ = 0.0
        self.listener.position = (x, y, z)
        self.listener.forward_orientation = (lookX, lookY, lookZ)
        self.listener.up_orientation = (upX, upY, upZ)

    def play(self, sound, soundPos):
        if not self.enabled or not self.supported:
            return

        dist = 16.0
        if sound.volume > 1.0:
            dist *= sound.volume

        self.player.max_distance = dist
        self.player.position = (soundPos.x, soundPos.y, soundPos.z)
        self.player.pitch = sound.pitch
        self.player.volume = sound.volume
        self.player.seek(0.0)
        self.player.queue(sound.stream)
        if self.player.playing:
            self.player.next_source()
        self.player.play()
