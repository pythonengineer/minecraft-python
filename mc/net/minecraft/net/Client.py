from mc.net.minecraft.comm.SocketConnection import SocketConnection
from mc.net.minecraft.net.ConnectionThread import ConnectionThread
from mc.net.minecraft.net import Packets
from mc.net.minecraft.gui.ErrorScreen import ErrorScreen
import traceback

class Client:
    levelBuffer = None
    serverConnection = None
    processData = False
    connected = False
    players = {}

    def __init__(self, minecraft, ip, port, username, mpPass):
        self.minecraft = minecraft
        self.minecraft.hideScreen = True
        ConnectionThread(self, ip, port, username, mpPass, minecraft).start()

    def sendTileUpdated(self, x, y, z, editMode, paintTexture):
        self.serverConnection.sendPacket(Packets.PLACE_OR_REMOVE_TILE, [x, y, z, editMode, paintTexture])

    def handleException(self, e):
        self.serverConnection.disconnect()
        self.minecraft.setScreen(ErrorScreen('Disconnected!', str(e)))
        print(traceback.format_exc())

    def isConnected(self):
        return self.serverConnection and self.serverConnection.connected

    def getUsernames(self):
        players = []
        players.append(self.minecraft.user.name)
        for player in self.players.values():
            players.append(player.name)

        return players
