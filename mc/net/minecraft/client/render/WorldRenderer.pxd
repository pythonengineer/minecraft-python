# cython: language_level=3

cimport cython

from mc.net.minecraft.client.render.Frustum cimport Frustum
from mc.net.minecraft.client.render.Tessellator cimport Tessellator
from mc.net.minecraft.client.render.RenderBlocks cimport RenderBlocks
from mc.net.minecraft.game.level.block.Block cimport Block
from mc.net.minecraft.game.level.World cimport World
from mc.net.minecraft.game.physics.AxisAlignedBB cimport AxisAlignedBB

@cython.final
cdef class WorldRenderer:

    cdef:
        World __worldObj
        Tessellator __t
        RenderBlocks __renderBlocks
        AxisAlignedBB __rendererBoundingBox

        int __glRenderList

        int __posX
        int __posY
        int __posZ

        int __sizeWidth
        int __sizeHeight
        int __sizeDepth

        int __posXPlus
        int __posYPlus
        int __posZPlus

        bint[2] __skipRenderPass
        public bint isInFrustum
        public bint needsUpdate

    cdef updateRenderer(self)
    cpdef float distanceToEntitySquared(self, player)
    cdef __setDontDraw(self)
    cdef getGLCallListForPass(self, int* chunkBuffer, int startingIndex, int renderPass)
    cdef updateInFrustum(self, Frustum frustum)
