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
        public bint isCollidedHorizontally
        bint __surfaceCollision
        public bint isDead

        public float yOffset
        public float width
        public float height
        public float prevDistanceWalkedModified
        public float distanceWalkedModified
        public bint _canTriggerWalking
        public float _fallDistance
        int __nextStepDistance
        public float lastTickPosX
        public float lastTickPosY
        public float lastTickPosZ
        float __ySize
        public float stepHeight
        bint __noClip
        float __entityCollisionReduction
        public object _rand
        public int ticksExisted
        public int fireResistance
        public int fire

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
