# cython: language_level=3

from mc.net.minecraft.phys.AABB cimport AABB
from mc.net.minecraft.level.Level cimport Level

cdef class Entity:

    cdef:
        public float x
        public float y
        public float z
        public float xo
        public float yo
        public float zo
        public float xd
        public float yd
        public float zd
        public float yRot
        public float xRot
        public float yRotO
        public float xRotO

        public Level level
        public AABB bb
        public bint onGround
        public bint horizontalCollision
        public bint collision
        public bint slide
        public bint removed

        public float heightOffset
        public float bbWidth
        public float bbHeight
        public float walkDistO
        public float walkDist
        public bint makeStepSound
        public float fallDistance
        int __nextStep
        public object blockMap
        public float xOld
        public float yOld
        public float zOld
        public int textureId
        public float ySlideOffset
        public float footSize
        public bint noPhysics
        public float pushthrough
        public bint hovered

    cpdef tick(self)
    cpdef bint isFree(self, float xa, float ya, float za)
    cpdef move(self, float x, float y, float z)
    cdef _causeFallDamage(self, float distance)
    cdef bint isInWater(self)
    cdef bint isInLava(self)
    cpdef moveRelative(self, float xa, float za, float speed)
    cpdef float getBrightness(self, float a)
    cpdef render(self, textures, float translation)
    cdef push(self, entity)
    cdef bint shouldRender(self, vec)
    cdef bint shouldRenderAtSqrDistance(self, float d)
