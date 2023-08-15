import math

import pyglet
from pyglet import gl as opengl
from pyglet import window, canvas, clock, compat_platform

from mc.net.minecraft.Timer import Timer
from mc.net.minecraft.Player import Player
from mc.net.minecraft.HitResult import HitResult
from mc.net.minecraft.level.Chunk import Chunk
from mc.net.minecraft.level.Level import Level
from mc.net.minecraft.level.LevelRenderer import LevelRenderer
from mc.CompatibilityShims import BufferUtils, gluPerspective, getMillis


pyglet.options['debug_gl'] = False


class Vec3:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Minecraft(window.Window):
    FULLSCREEN_MODE = False
    col = 920330
    fogColor = ((col >> 16 & 0xFF) / 255.0, (col >> 8 & 0xFF) / 255.0, (col & 0xFF) / 255.0, (col & 0xFF) / 255.0, 1.0)
    timer = Timer(60.0)
    hitResult = None
    running = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fr = 0.5
        fg = 0.8
        fb = 1.0

        opengl.glEnable(opengl.GL_TEXTURE_2D)
        opengl.glShadeModel(opengl.GL_SMOOTH)
        opengl.glClearColor(fr, fg, fb, 0.0)
        opengl.glClearDepth(1.0)
        opengl.glEnable(opengl.GL_DEPTH_TEST)
        opengl.glDepthFunc(opengl.GL_LEQUAL)

        opengl.glMatrixMode(opengl.GL_PROJECTION)
        opengl.glLoadIdentity()
        opengl.glMatrixMode(opengl.GL_MODELVIEW)

        self.level = Level(256, 256, 64)
        self.levelRenderer = LevelRenderer(self.level)
        self.player = Player(self.level)

        self.set_exclusive_mouse(True)

    def destroy(self):
        self.level.save()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == window.mouse.RIGHT:
            if self.hitResult:
                self.level.setTile(self.hitResult.x, self.hitResult.y, self.hitResult.z, 0)
        elif button == window.mouse.LEFT:
            if self.hitResult:
                x = self.hitResult.x
                y = self.hitResult.y
                z = self.hitResult.z

                if self.hitResult.f == 0: y -= 1
                if self.hitResult.f == 1: y += 1
                if self.hitResult.f == 2: z -= 1
                if self.hitResult.f == 3: z += 1
                if self.hitResult.f == 4: x -= 1
                if self.hitResult.f == 5: x += 1
                self.level.setTile(x, y, z, 1)

    def on_mouse_motion(self, x, y, dx, dy):
        self.player.turn(dx, dy)

    def on_activate(self):
        # Remove this hack when the window boundary issue is fixed upstream:
        if compat_platform == 'win32':
            self._update_clipped_cursor()

    def on_key_press(self, symbol, modifiers):
        if symbol == window.key.R:
            self.player.resetPos()
        elif symbol in (window.key.UP, window.key.W):
            self.player.upPressed = True
        elif symbol in (window.key.DOWN, window.key.S):
            self.player.downPressed = True
        elif symbol in (window.key.LEFT, window.key.A):
            self.player.leftPressed = True
        elif symbol in (window.key.RIGHT, window.key.D):
            self.player.rightPressed = True
        elif symbol in (window.key.SPACE, window.key.LWINDOWS, window.key.LMETA):
            self.player.spacePressed = True
        elif symbol == window.key.RETURN:
            self.level.save()
        elif symbol == window.key.ESCAPE:
            self.running = False

    def on_key_release(self, symbol, modifiers):
        if symbol in (window.key.UP, window.key.W):
            self.player.upPressed = False
        elif symbol in (window.key.DOWN, window.key.S):
            self.player.downPressed = False
        elif symbol in (window.key.LEFT, window.key.A):
            self.player.leftPressed = False
        elif symbol in (window.key.RIGHT, window.key.D):
            self.player.rightPressed = False
        elif symbol in (window.key.SPACE, window.key.LWINDOWS, window.key.LMETA):
            self.player.spacePressed = False

    def on_draw(self):
        self.clear()
        self.timer.advanceTime()
        for i in range(self.timer.ticks):
            self.tick()
        self.render(self.timer.a)

    def run(self):
        self.__chunk = Chunk(None, 0, 0, 0, 0, 0, 0, True)

        display = canvas.Display()
        screen = display.get_default_screen()
        locationX = screen.width // 2 - self.width // 2
        locationY = screen.height // 2 - self.height // 2
        self.set_location(locationX, locationY)
        self.set_visible(True)

        lastTime = getMillis()
        frames = 0
        while self.running:
            clock.tick()
            self.dispatch_events()
            self.dispatch_event('on_draw')
            self.flip()

            frames += 1
            while getMillis() >= lastTime + 1000:
                print(str(frames) + ' fps, ' + str(self.__chunk.updates) + ' chunk updates')
                self.__chunk.updates = 0
                lastTime += 1000
                frames = 0

        self.destroy()

    def tick(self):
        self.player.tick()

    def moveCameraToPlayer(self, a):
        opengl.glTranslatef(0.0, 0.0, -0.3)
        opengl.glRotatef(self.player.xRot, 1.0, 0.0, 0.0)
        opengl.glRotatef(self.player.yRot, 0.0, 1.0, 0.0)

        x = self.player.xo + (self.player.x - self.player.xo) * a
        y = self.player.yo + (self.player.y - self.player.yo) * a
        z = self.player.zo + (self.player.z - self.player.zo) * a
        opengl.glTranslatef(-x, -y, -z)

    def setupCamera(self, a):
        opengl.glMatrixMode(opengl.GL_PROJECTION)
        opengl.glLoadIdentity()
        gluPerspective(70.0, self.width / self.height, 0.05, 1000.0)
        opengl.glMatrixMode(opengl.GL_MODELVIEW)
        opengl.glLoadIdentity()
        self.moveCameraToPlayer(a)

    def pick(self, a):
        xRot = self.player.xRotO + (self.player.xRot - self.player.xRotO) * a
        yRot = self.player.yRotO + (self.player.yRot - self.player.yRotO) * a
        x = self.player.xo + (self.player.x - self.player.xo) * a
        y = self.player.yo + (self.player.y - self.player.yo) * a
        z = self.player.zo + (self.player.z - self.player.zo) * a

        vec1 = Vec3(x, y, z)
        y1 = math.cos((-yRot) * math.pi / 180.0 + math.pi)
        y2 = math.sin((-yRot) * math.pi / 180.0 + math.pi)
        x1 = math.cos((-xRot) * math.pi / 180.0)
        x2 = math.sin((-xRot) * math.pi / 180.0)
        x = (y2 * x1) * 5.0
        y = x2 * 5.0
        z = (y1 * x1) * 5.0
        vec2 = Vec3(vec1.x + x, vec1.y + y, vec1.z + z)
        self.hitResult = self.level.clip(vec1, vec2)

    def render(self, a):
        self.pick(a)

        opengl.glClear(opengl.GL_COLOR_BUFFER_BIT | opengl.GL_DEPTH_BUFFER_BIT)
        self.setupCamera(a)

        opengl.glEnable(opengl.GL_CULL_FACE)
        opengl.glEnable(opengl.GL_FOG)
        opengl.glFogi(opengl.GL_FOG_MODE, opengl.GL_VIEWPORT_BIT)
        opengl.glFogf(opengl.GL_FOG_DENSITY, 0.2)
        opengl.glFogfv(opengl.GL_FOG_COLOR, (opengl.GLfloat * 4)(self.fogColor[0], self.fogColor[1],
                                                     self.fogColor[2], self.fogColor[3]))

        opengl.glDisable(opengl.GL_FOG)
        self.levelRenderer.render(self.player, 0)
        opengl.glEnable(opengl.GL_FOG)
        self.levelRenderer.render(self.player, 1)
        opengl.glDisable(opengl.GL_TEXTURE_2D)

        if self.hitResult:
            self.levelRenderer.renderHit(self.hitResult)

        opengl.glDisable(opengl.GL_FOG)
