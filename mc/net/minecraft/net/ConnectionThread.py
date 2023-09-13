from mc.net.minecraft.comm.SocketConnection import SocketConnection
from mc.net.minecraft.gui.ErrorScreen import ErrorScreen
from mc.net.minecraft.net import Packets
from threading import Thread

class ConnectionThread(Thread):

    def __init__(self, networkClient, ip, port, username, mpPass, minecraft):
        super().__init__()
        self.__networkClient = networkClient
        self.__ip = ip
        self.__port = port
        self.__username = username
        self.__mpPass = mpPass
        self.__minecraft = minecraft

    def run(self):
        try:
            connection = SocketConnection(self.__ip, self.__port)
            self.__networkClient.serverConnection = connection
            connection.client = self.__networkClient
            connection.sendPacket(Packets.LOGIN, [7, self.__username, self.__mpPass, 0])
            self.__networkClient.processData = True
        except ConnectionRefusedError:
            self.__minecraft.hideScreen = False
            self.__minecraft.networkClient = None
            self.__minecraft.setScreen(ErrorScreen('Failed to connect', 'You failed to connect to the server. It\'s probably down!'))
            self.__networkClient.processData = False
