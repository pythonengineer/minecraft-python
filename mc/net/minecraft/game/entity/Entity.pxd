# cython: language_level=3

from mc.net.minecraft.game.physics.AxisAlignedBB cimport AxisAlignedBB
from mc.net.minecraft.game.level.World cimport World

cdef class Entity:

    cdef:
        public float posX
        public float posY
        public float posZ
        public float prevPosX
        public float prevPosY
        public float prevPosZ
        public float motionX
        public float motionY
        public float motionZ
        public float rotationYaw
        public float rotationPitch
        public float prevRotationYaw
        public float prevRotationPitch

        public World _worldObj
        public AxisAlignedBB boundingBox
        public bint onGround
        public bint horizontalCollision
        bint __collision
        public bint isDead

        public float yOffset
        float __bbWidth
        public float bbHeight
        public float prevDistanceWalkedModified
        public float distanceWalkedModified
        public bint _makeStepSound
        public float _fallDistance
        int __nextStep
        public float lastTickPosX
        public float lastTickPosY
        public float lastTickPosZ
        float __ySize
        public float stepHeight
        bint __noClip
        float __entityCollisionReduction
        public object _rand
        public int ticksExisted

    cpdef onEntityUpdate(self)
    cpdef bint isOffsetPositionInLiquid(self, float xa, float ya, float za)
    cpdef moveEntity(self, float x, float y, float z)
    cdef _fall(self, float distance)
    cdef bint handleWaterMovement(self)
    cdef bint handleLavaMovement(self)
    cpdef moveFlying(self, float xa, float za, float speed)
    cpdef float getBrightness(self)
    cdef applyEntityCollision(self, entity)
    cpdef bint shouldRender(self, vec)
    cdef bint shouldRenderAtSqrDistance(self, float d)
