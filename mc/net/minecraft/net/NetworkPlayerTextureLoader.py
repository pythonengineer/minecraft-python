from threading import Thread
from base64 import b64decode
from io import BytesIO
from PIL import Image

import urllib.request
import random
import time
import json

def getTextureInfo(properties):
    for prop in properties:
        if prop['name'] == 'textures':
            return json.loads(b64decode(prop['value'], validate=True).decode('utf-8'))

class NetworkPlayerTextureLoader(Thread):

    def __init__(self, player):
        super().__init__()
        self.__player = player

    def run(self):
        username = self.__player.name

        try:
            time.sleep(random.randint(1, 7))
            with urllib.request.urlopen(f'https://api.mojang.com/users/profiles/minecraft/{username}') as r:
                if r.code != 200:
                    return

                userId = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))['id']

            time.sleep(random.randint(2, 3))
            with urllib.request.urlopen(f'https://sessionserver.mojang.com/session/minecraft/profile/{userId}') as r:
                if r.code != 200:
                    return

                userInfo = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))

            textureInfo = getTextureInfo(userInfo['properties'])
            if not textureInfo:
                return

            try:
                skinUrl = textureInfo['textures']['SKIN']['url']
            except:
                return

            time.sleep(random.randint(2, 4))
            with urllib.request.urlopen(skinUrl) as r:
                if r.code != 200:
                    return

                self.__player.newTexture = Image.open(BytesIO(r.read())).convert('RGBA')
        except:
            pass
