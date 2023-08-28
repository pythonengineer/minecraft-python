from mc.net.minecraft.gui.ErrorScreen import ErrorScreen
from mc.net.minecraft.net.NetworkPlayer import NetworkPlayer
from mc.net.minecraft.net.Packet import Packet, DataTypes
from mc.net.minecraft.net import Packets
from mc.net.minecraft.level.Level import Level
from mc.net.minecraft.level.LevelIO import LevelIO
from mc.CompatibilityShims import ByteArrayInputStream, ByteArrayOutputStream, BufferUtils
import traceback
import socket
import gzip

class SocketConnection:
    readBuffer = BufferUtils.createByteBuffer(1048576)
    writeBuffer = BufferUtils.createByteBuffer(1048576)
    manager = None
    __initialized = False
    __stringPacket = bytearray(64)

    def __init__(self, server, port):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((server, port))
        self.__socket.setblocking(False)
        self.connected = True
        self.readBuffer.clear()
        self.writeBuffer.clear()
        self.__socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 0)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)
        self.__socket.settimeout(0)

    def disconnect(self):
        try:
            if self.writeBuffer.position() > 0:
                self.writeBuffer.flip()
                self.__socket.write(self.writeBuffer)
                self.writeBuffer.compact()
        except:
            pass

        self.connected = False

        try:
            self.__socket.close()
        except:
            pass

        self.__socket = None

    def processData(self):
        try:
            self.readBuffer.put(self.__socket.recv(self.readBuffer.remaining()))
        except:
            pass

        i1 = 0
        while self.readBuffer.position() > 0 and i1 + 1 != 100:
            i1 += 1
            self.readBuffer.flip()
            b2 = self.readBuffer.get(0)
            packet = Packet.PACKETS[b2]
            if not packet:
                raise IOError('Bad command: ' + str(b2))

            if self.readBuffer.remaining() < packet.size + 1:
                self.readBuffer.compact()
                break

            self.readBuffer.get()
            data = [None] * len(packet.fields)

            for i, field in enumerate(packet.fields):
                data[i] = self.read(field)

            if self.manager.processData:
                if packet == Packets.LOGIN:
                    self.manager.minecraft.loadingScreen.beginLevelLoading(data[1].decode())
                    self.manager.minecraft.loadingScreen.levelLoadUpdate(data[2].decode())
                    self.manager.minecraft.player.userType = data[3]
                elif packet == Packets.LEVEL_INITIALIZE:
                    self.manager.minecraft.setLevel(None)
                    self.manager.levelBuffer = ByteArrayOutputStream()
                elif packet == Packets.LEVEL_DATA_CHUNK:
                    s13 = data[0]
                    b5 = data[1]
                    b6 = data[2]
                    self.manager.minecraft.loadingScreen.setLoadingProgress()
                    self.manager.levelBuffer.write(b5, 0, s13)
                elif packet == Packets.LEVEL_FINALIZE:
                    try:
                        self.manager.levelBuffer.close()
                    except Exception as e:
                        print(traceback.format_exc())

                    b14 = LevelIO.loadBlocks(ByteArrayInputStream(gzip.decompress(self.manager.levelBuffer.toByteArray())))
                    self.manager.levelBuffer = None
                    s18 = data[0]
                    s21 = data[1]
                    s17 = data[2]
                    level = Level()
                    level.setNetworkMode(True)
                    level.setDataLegacy(s18, s21, s17, b14)
                    self.manager.minecraft.setLevel(level)
                    self.manager.minecraft.hideGui = False
                    self.manager.connected = True
                elif packet == Packets.SET_TILE:
                    if self.manager.minecraft.level:
                        self.manager.minecraft.level.netSetTile(int(data[0]), int(data[1]),
                                                                int(data[2]), data[3])
                elif packet == Packets.PLAYER_JOIN:
                    b15 = data[0]
                    string19 = data[1].decode()
                    s18 = data[2]
                    s21 = data[3]
                    s24 = data[4]
                    b8 = data[5]
                    b9 = data[6]
                    if b15 not in self.manager.players:
                        if b15 >= 0:
                            networkPlayer = NetworkPlayer(self.manager.minecraft, b15, string19, s18, s21, s24, (-b8 * 360) / 256.0, (b9 * 360) / 256.0)
                            self.manager.players[b15] = networkPlayer
                            self.manager.minecraft.level.entities.add(networkPlayer)
                        else:
                            self.manager.minecraft.level.setSpawnPos(s18 // 32, s21 // 32, s24 // 32, b8 * 320 / 256)
                            self.manager.minecraft.player.moveTo(s18 / 32.0, s21 / 32.0, s24 / 32.0, (b8 * 360) / 256.0, (b9 * 360) / 256.0)
                elif packet == Packets.PLAYER_TELEPORT:
                    b15 = data[0]
                    s17 = data[1]
                    s18 = data[2]
                    s21 = data[3]
                    b25 = data[4]
                    b8 = data[5]
                    networkPlayer = self.manager.players.get(b15)
                    if b15 < 0:
                        self.manager.minecraft.player.moveTo(s17 / 32.0, s18 / 32.0, s21 / 32.0, float(b25 * 360) / 256.0, float(b8 * 360) / 256.0)
                    elif networkPlayer:
                        networkPlayer.teleport(s17, s18, s21, float(-b25 * 360) / 256.0, float(b8 * 360) / 256.0)
                elif packet == Packets.PLAYER_MOVE_AND_ROTATE:
                    b15 = data[0]
                    b23 = data[1]
                    b22 = data[2]
                    b6 = data[3]
                    b25 = data[4]
                    b8 = data[5]
                    networkPlayer = self.manager.players.get(b15)
                    if b15 >= 0 and networkPlayer:
                        networkPlayer.queue(b23, b22, b6, float(-b25 * 360) / 256.0, float(b8 * 360) / 256.0)
                elif packet == Packets.PLAYER_ROTATE:
                    b15 = data[0]
                    b23 = data[1]
                    b22 = data[2]
                    networkPlayer = self.manager.players.get(b15)
                    if b15 >= 0 and networkPlayer:
                        networkPlayer.queue(float(-b23 * 360) / 256.0, float(b22 * 360) / 256.0)
                elif packet == Packets.PLAYER_MOVE:
                    b15 = data[0]
                    b23 = data[1]
                    b22 = data[2]
                    b6 = data[3]
                    networkPlayer = self.manager.players.get(b15)
                    if b15 >= 0 and networkPlayer:
                        networkPlayer.queue(b23, b22, b6)
                elif packet == Packets.PLAYER_DISCONNECT:
                    b15 = data[0]
                    if b15 in self.manager.players:
                        networkPlayer = self.manager.players.pop(b15)
                        if b15 >= 0 and networkPlayer:
                            networkPlayer.clear()
                            self.manager.minecraft.level.entities.remove(networkPlayer)
                elif packet == Packets.CHAT_MESSAGE:
                    b15 = data[0]
                    string19 = data[1].decode()
                    if b15 < 0:
                        self.manager.minecraft.hud.addChatMessage('&e' + string19)
                    else:
                        self.manager.players.get(b15)
                        self.manager.minecraft.hud.addChatMessage(string19)
                elif packet == Packets.KICK_PLAYER:
                    self.manager.minecraft.setScreen(ErrorScreen('Connection lost', data[0].decode()))
                    self.disconnect()

            if not self.connected:
                break

            self.readBuffer.compact()

        if self.writeBuffer.position() > 0:
            self.writeBuffer.flip()
            data = bytearray(self.writeBuffer.remaining())
            self.writeBuffer.get(data)
            self.__socket.send(data)
            self.writeBuffer.compact()

    def sendPacket(self, packet, values):
        if self.connected:
            self.writeBuffer.put(packet.id)

            for i, value in enumerate(values):
                field = packet.fields[i]
                if self.connected:
                    try:
                        if field == DataTypes.Long:
                            self.writeBuffer.putLong(value)
                        elif field == DataTypes.Integer:
                            self.writeBuffer.putInt(value)
                        elif field == DataTypes.Short:
                            self.writeBuffer.putShort(value)
                        elif field == DataTypes.Byte:
                            self.writeBuffer.put(value)
                        elif field == DataTypes.Double:
                            self.writeBuffer.putDouble(value)
                        elif field == DataTypes.Float:
                            self.writeBuffer.putFloat(value)
                        elif field != DataTypes.String:
                            if field == DataTypes.Bytes:
                                b9 = bytearray(value)
                                if len(value) < 1024:
                                    b9 = bytearray(1024)
                                    for n, v in enumerate(value):
                                        b9[n] = v

                                self.writeBuffer.put(b9)
                        else:
                            b9 = value.encode('utf-8')
                            self.__stringPacket = bytearray([32]) * 64

                            for i10 in range(64):
                                if i10 >= len(b9):
                                    break

                                self.__stringPacket[i10] = b9[i10]

                            for i10 in range(len(b9), 64):
                                self.__stringPacket[i10] = 32

                            self.writeBuffer.put(self.__stringPacket)
                    except Exception as e:
                        self.manager.disconnect(e)

    def read(self, field):
        if not self.connected:
            return None
        else:
            try:
                if field == DataTypes.Long:
                    return self.readBuffer.getLong()
                elif field == DataTypes.Integer:
                    return self.readBuffer.getInt()
                elif field == DataTypes.Short:
                    return self.readBuffer.getShort()
                elif field == DataTypes.Byte:
                    return self.readBuffer.get()
                elif field == DataTypes.Double:
                    return self.readBuffer.getDouble()
                elif field == DataTypes.Float:
                    return self.readBuffer.getFloat()
                elif field == DataTypes.String:
                    self.readBuffer.get(self.__stringPacket)
                    return bytes(self.__stringPacket).strip()
                elif field == DataTypes.Bytes:
                    b4 = bytearray(1024)
                    self.readBuffer.get(b4)
                    return b4
                else:
                    return None
            except Exception as e:
                self.manager.disconnect(e)
                return None
