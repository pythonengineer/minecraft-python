from pyglet import media

class SoundPoolEntry:

    def __init__(self, name, url):
        self.soundName = name
        self.soundUrl = url
        self.stream = media.load(url, streaming=False)
