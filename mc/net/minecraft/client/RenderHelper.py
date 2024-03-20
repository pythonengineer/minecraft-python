from mc.net.minecraft.game.physics.Vec3D import Vec3D
from mc.CompatibilityShims import BufferUtils
from pyglet import gl

class RenderHelper:
    __colorBuffer = BufferUtils.createFloatBuffer(16)

    @staticmethod
    def disableStandardItemLighting():
        gl.glDisable(gl.GL_LIGHTING)
        gl.glDisable(gl.GL_LIGHT0)
        gl.glDisable(gl.GL_LIGHT1)
        gl.glDisable(gl.GL_COLOR_MATERIAL)

    @staticmethod
    def enableStandardItemLighting():
        gl.glEnable(gl.GL_LIGHTING)
        gl.glEnable(gl.GL_LIGHT0)
        gl.glEnable(gl.GL_LIGHT1)
        gl.glEnable(gl.GL_COLOR_MATERIAL)
        gl.glColorMaterial(gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT_AND_DIFFUSE)
        x = 0.4
        y = 0.6
        z = 0.8
        gl.glLightModelf(gl.GL_LIGHT_MODEL_LOCAL_VIEWER, 1.0)
        vec = Vec3D(-0.4, 1.0, 1.0)
        RenderHelper.__setColorBuffer(vec.xCoord, vec.yCoord, vec.zCoord,
                                      0.0).glLightfv(gl.GL_LIGHT0, gl.GL_POSITION)
        RenderHelper.__setColorBuffer(y, y, y, 1.0).glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE)
        RenderHelper.__setColorBuffer(0.0, 0.0, 0.0, 1.0).glLightfv(gl.GL_LIGHT0, gl.GL_AMBIENT)
        RenderHelper.__setColorBuffer(z, z, z, 1.0).glLightfv(gl.GL_LIGHT0, gl.GL_SPECULAR)
        gl.glShadeModel(gl.GL_SMOOTH)
        RenderHelper.__setColorBuffer(x, x, x, 1.0).glLightModelfv(gl.GL_LIGHT_MODEL_AMBIENT)

    @staticmethod
    def __setColorBuffer(a, b, c, d):
        RenderHelper.__colorBuffer.clear()
        RenderHelper.__colorBuffer.put(a).put(b).put(c).put(d)
        RenderHelper.__colorBuffer.flip()
        return RenderHelper.__colorBuffer
