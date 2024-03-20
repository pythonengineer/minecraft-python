from threading import Thread
from base64 import b64decode
from io import BytesIO
from PIL import Image

import urllib.request
import json

def getTextureInfo(properties):
    for prop in properties:
        if prop['name'] == 'textures':
            return json.loads(b64decode(prop['value'], validate=True).decode('utf-8'))

class ThreadDownloadSkin(Thread):

    def __init__(self, mc):
        super().__init__()
        self.__mc = mc

    def run(self):
        if not self.__mc.session:
            return

        username = self.__mc.session.username
        if not username:
            return

        try:
            with urllib.request.urlopen(f'https://api.mojang.com/users/profiles/minecraft/{username}') as r:
                if r.code != 200:
                    return

                userId = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))['id']

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

            with urllib.request.urlopen(skinUrl) as r:
                if r.code != 200:
                    return
        except:
            pass
