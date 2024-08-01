# cython: language_level=3

cimport cython

from mc.net.minecraft.game.level.World cimport World
from mc.net.minecraft.client.render.RenderBlocks cimport RenderBlocks
from mc.net.minecraft.client.render.Tessellator cimport Tessellator
from mc.JavaUtils cimport IntBuffer

@cython.final
cdef class RenderGlobal:

    cdef:
        object __mc
        object __renderEngine
        World __worldObj
        IntBuffer __renderIntBuffer
        Tessellator __t

        list __worldRenderersToUpdate
        list __sortedWorldRenderers
        list __worldRenderers

        RenderBlocks __globalRenderBlocks

        int[50000] __chunkBuffer
        int __cloudOffsetX
        float __prevSortX
        float __prevSortY
        float __prevSortZ

        public float damagePartialTime

        int __glGenList
        int __glRenderListBase

        int __renderChunksWide
        int __renderChunksTall
        int __renderChunksDeep

    cdef __markBlocksForUpdate(self, int x0, int y0, int z0, int x1, int y1, int z1)
    cdef markBlockAndNeighborsNeedsUpdate(self, int x, int y, int z)
    cdef markBlockRangeNeedsUpdate(self, int x0, int y0, int z0,
                                   int x1, int y1, int z1)
