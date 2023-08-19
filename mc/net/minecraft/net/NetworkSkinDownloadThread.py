from threading import Thread
from base64 import b64decode
from io import BytesIO
from PIL import Image

import urllib.request
import traceback
import json

def getTextureInfo(properties):
    for prop in properties:
        if prop['name'] == 'textures':
            return json.loads(b64decode(prop['value'], validate=True).decode('utf-8'))

class NetworkSkinDownloadThread(Thread):

    def __init__(self, player):
        super().__init__()
        self.__player = player

    def run(self):
        username = self.__player.name

        try:
            with urllib.request.urlopen(f'https://api.mojang.com/users/profiles/minecraft/{username}') as r:
                if r.code != 200:
                    print('Failed to load texture for', username)
                    return

                userId = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))['id']

            with urllib.request.urlopen(f'https://sessionserver.mojang.com/session/minecraft/profile/{userId}') as r:
                if r.code != 200:
                    print('Failed to load texture for', username)
                    return

                userInfo = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))

            textureInfo = getTextureInfo(userInfo['properties'])
            if not textureInfo:
                print('Failed to load texture for', username)
                return

            try:
                skinUrl = textureInfo['textures']['SKIN']['url']
            except:
                print('Failed to load texture for', username)
                print(traceback.format_exc())
                return

            with urllib.request.urlopen(skinUrl) as r:
                if r.code != 200:
                    print('Failed to load texture for', username)
                    return

                print('Loading texture for', username)
                self.__player.newTexture = Image.open(BytesIO(r.read())).convert('RGBA')
        except:
            print('Failed to load texture for', username)
            print(traceback.format_exc())
