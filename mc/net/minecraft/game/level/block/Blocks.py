from mc.net.minecraft.game.level.block.Block import Block
from mc.net.minecraft.game.level.block.BlockFalling import BlockFalling
from mc.net.minecraft.game.level.block.BlockFluid import BlockFluid
from mc.net.minecraft.game.level.block.BlockStationary import BlockStationary
from mc.net.minecraft.game.level.block.BlockBookshelf import BlockBookshelf
from mc.net.minecraft.game.level.block.BlockSponge import BlockSponge
from mc.net.minecraft.game.level.block.BlockMushroom import BlockMushroom
from mc.net.minecraft.game.level.block.BlockPlants import BlockPlants
from mc.net.minecraft.game.level.block.BlockGlass import BlockGlass
from mc.net.minecraft.game.level.block.BlockGrass import BlockGrass
from mc.net.minecraft.game.level.block.BlockDirt import BlockDirt
from mc.net.minecraft.game.level.block.BlockLeaves import BlockLeaves
from mc.net.minecraft.game.level.block.BlockTorch import BlockTorch
from mc.net.minecraft.game.level.block.BlockLog import BlockLog
from mc.net.minecraft.game.level.block.BlockOre import BlockOre
from mc.net.minecraft.game.level.block.BlockOreBlock import BlockOreBlock
from mc.net.minecraft.game.level.block.BlockStep import BlockStep
from mc.net.minecraft.game.level.block.BlockStone import BlockStone
from mc.net.minecraft.game.level.block.BlockTNT import BlockTNT
from mc.net.minecraft.game.level.block.BlockSapling import BlockSapling
from mc.net.minecraft.game.level.block.StepSound import StepSound
from mc.net.minecraft.game.level.material.Material import Material

class Blocks:

    def __init__(self):
        self.blocksList = [None] * 256
        self.tickOnLoad = [False] * 256
        self.opaqueCubeLookup = [False] * 256
        self.lightOpacity = [0] * 256
        self.canBlockGrass = [False] * 256
        self.isBlockFluid = [False] * 256
        self.lightValue = [0] * 256

        self.soundPowderFootstep = StepSound('stone', 1.0, 1.0)
        self.soundWoodFootstep = StepSound('wood', 1.0, 1.0)
        self.soundGravelFootstep = StepSound('gravel', 1.0, 1.0)
        self.soundGrassFootstep = StepSound('grass', 1.0, 1.0)
        self.soundStoneFootstep = StepSound('stone', 1.0, 1.0)
        self.soundMetalFootstep = StepSound('stone', 1.0, 1.5)

        self.stone = BlockStone(self, 1, 1).setHardness(1.0)
        self.stone.blockIsDropped = False
        self.stone.stepSound = self.soundStoneFootstep

        self.grass = BlockGrass(self, 2).setHardness(0.6)
        self.grass.stepSound = self.soundGrassFootstep

        self.dirt = BlockDirt(self, 3, 2).setHardness(0.5)
        self.dirt.stepSound = self.soundGravelFootstep
        self.cobblestone = Block(self, 4, 16).setHardness(1.5)
        self.cobblestone.blockIsDropped = False
        self.cobblestone.stepSound = self.soundStoneFootstep
        self.planks = Block(self, 5, 4).setHardness(1.5)
        self.planks.stepSound = self.soundWoodFootstep
        self.sapling = BlockSapling(self, 6, 15).setHardness(0.0)
        self.sapling.stepSound = self.soundGrassFootstep
        self.bedrock = Block(self, 7, 17).setHardness(999.0)
        self.bedrock.blockIsDropped = False
        self.bedrock.stepSound = self.soundStoneFootstep

        self.waterMoving = BlockFluid(self, 8, Material.water).setHardness(100.0).setLightOpacity(2)
        self.waterStill = BlockStationary(self, 9, Material.water).setHardness(100.0).setLightOpacity(2)

        self.lavaMoving = BlockFluid(self, 10, Material.lava).setHardness(0.0).setLightValue(0.8).setLightOpacity(255)
        self.lavaStill = BlockStationary(self, 11, Material.lava).setHardness(100.0).setLightValue(0.8).setLightOpacity(255)

        self.sand = BlockFalling(self, 12, 18).setHardness(0.5)
        self.sand.stepSound = self.soundGravelFootstep
        self.gravel = BlockFalling(self, 13, 19).setHardness(0.6)
        self.gravel.stepSound = self.soundGravelFootstep

        self.oreGold = BlockOre(self, 14, 32).setHardness(3.0)
        self.oreGold.blockIsDropped = False
        self.oreGold.stepSound = self.soundStoneFootstep
        self.oreIron = BlockOre(self, 15, 33).setHardness(3.0)
        self.oreIron.blockIsDropped = False
        self.oreIron.stepSound = self.soundStoneFootstep
        self.oreCoal = BlockOre(self, 16, 34).setHardness(3.0)
        self.oreCoal.blockIsDropped = False
        self.oreCoal.stepSound = self.soundStoneFootstep

        self.log = BlockLog(self, 17).setHardness(2.5)
        self.log.stepSound = self.soundWoodFootstep
        self.leaves = BlockLeaves(self, 18, 22).setHardness(0.2).setLightOpacity(1)
        self.leaves.stepSound = self.soundGrassFootstep

        self.sponge = BlockSponge(self, 19).setHardness(0.6)
        self.sponge.stepSound = self.soundGrassFootstep
        self.glass = BlockGlass(self, 20, 49, False).setHardness(0.3)
        self.glass.stepSound = self.soundMetalFootstep

        self.clothRed = Block(self, 21, 64).setHardness(0.8)
        self.clothRed.stepSound = self.soundGrassFootstep
        self.clothOrange = Block(self, 22, 65).setHardness(0.8)
        self.clothOrange.stepSound = self.soundGrassFootstep
        self.clothYellow = Block(self, 23, 66).setHardness(0.8)
        self.clothYellow.stepSound = self.soundGrassFootstep
        self.clothChartreuse = Block(self, 24, 67).setHardness(0.8)
        self.clothChartreuse.stepSound = self.soundGrassFootstep
        self.clothGreen = Block(self, 25, 68).setHardness(0.8)
        self.clothGreen.stepSound = self.soundGrassFootstep
        self.clothSpringGreen = Block(self, 26, 69).setHardness(0.8)
        self.clothSpringGreen.stepSound = self.soundGrassFootstep
        self.clothCyan = Block(self, 27, 70).setHardness(0.8)
        self.clothCyan.stepSound = self.soundGrassFootstep
        self.clothCapri = Block(self, 28, 71).setHardness(0.8)
        self.clothCapri.stepSound = self.soundGrassFootstep
        self.clothUltramarine = Block(self, 29, 72).setHardness(0.8)
        self.clothUltramarine.stepSound = self.soundGrassFootstep
        self.clothViolet = Block(self, 30, 73).setHardness(0.8)
        self.clothViolet.stepSound = self.soundGrassFootstep
        self.clothPurple = Block(self, 31, 74).setHardness(0.8)
        self.clothPurple.stepSound = self.soundGrassFootstep
        self.clothMagenta = Block(self, 32, 75).setHardness(0.8)
        self.clothMagenta.stepSound = self.soundGrassFootstep
        self.clothRose = Block(self, 33, 76).setHardness(0.8)
        self.clothRose.stepSound = self.soundGrassFootstep
        self.clothDarkGray = Block(self, 34, 77).setHardness(0.8)
        self.clothDarkGray.stepSound = self.soundGrassFootstep
        self.clothGray = Block(self, 35, 78).setHardness(0.8)
        self.clothGray.stepSound = self.soundGrassFootstep
        self.clothWhite = Block(self, 36, 79).setHardness(0.8)
        self.clothWhite.stepSound = self.soundGrassFootstep

        self.plantYellow = BlockPlants(self, 37, 13).setHardness(0.0)
        self.plantYellow.stepSound = self.soundGrassFootstep
        self.plantRed = BlockPlants(self, 38, 12).setHardness(0.0)
        self.plantRed.stepSound = self.soundGrassFootstep

        self.mushroomBrown = BlockMushroom(self, 39, 29).setHardness(0.0)
        self.mushroomBrown.stepSound = self.soundGrassFootstep
        self.mushroomRed = BlockMushroom(self, 40, 28).setHardness(0.0)
        self.mushroomRed.stepSound = self.soundGrassFootstep

        self.goldBlock = BlockOreBlock(self, 41, 40).setHardness(3.0)
        self.goldBlock.blockIsDropped = False
        self.goldBlock.stepSound = self.soundMetalFootstep
        self.ironBlock = BlockOreBlock(self, 42, 39).setHardness(5.0)
        self.ironBlock.blockIsDropped = False
        self.ironBlock.stepSound = self.soundMetalFootstep

        self.slabDouble = BlockStep(self, 43, True).setHardness(2.0)
        self.slabDouble.blockIsDropped = False
        self.slabDouble.stepSound = self.soundStoneFootstep
        self.stairSingle = BlockStep(self, 44, False).setHardness(2.0)
        self.stairSingle.blockIsDropped = False
        self.stairSingle.stepSound = self.soundStoneFootstep

        self.brick = Block(self, 45, 7).setHardness(2.0)
        self.brick.blockIsDropped = False
        self.brick.stepSound = self.soundStoneFootstep

        self.tnt = BlockTNT(self, 46, 8).setHardness(0.0)
        self.tnt.stepSound = self.soundGrassFootstep

        self.bookshelf = BlockBookshelf(self, 47, 35).setHardness(1.5)
        self.bookshelf.stepSound = self.soundWoodFootstep

        self.cobblestoneMossy = Block(self, 48, 36).setHardness(1.0)
        self.cobblestoneMossy.blockIsDropped = False
        self.cobblestoneMossy.stepSound = self.soundStoneFootstep
        self.obsidian = BlockStone(self, 49, 37).setHardness(10.0)
        self.obsidian.blockIsDropped = False
        self.obsidian.stepSound = self.soundStoneFootstep

        self.torch = BlockTorch(self, 50, 80).setHardness(0.0).setLightValue(1.0)
        self.torch.stepSound = self.soundWoodFootstep

        self.blocksList[1:50] = [self.stone, self.grass, self.dirt, self.cobblestone, self.planks,
                                 self.sapling, self.bedrock, self.waterMoving, self.waterStill,
                                 self.lavaMoving, self.lavaStill, self.sand, self.gravel, self.oreGold,
                                 self.oreIron, self.oreCoal, self.log, self.leaves, self.sponge,
                                 self.glass, self.clothRed, self.clothOrange, self.clothYellow,
                                 self.clothChartreuse, self.clothGreen, self.clothSpringGreen,
                                 self.clothCyan, self.clothCapri, self.clothUltramarine,
                                 self.clothViolet, self.clothPurple, self.clothMagenta,
                                 self.clothRose, self.clothDarkGray, self.clothGray,
                                 self.clothWhite, self.plantYellow, self.plantRed,
                                 self.mushroomBrown, self.mushroomRed, self.goldBlock,
                                 self.ironBlock, self.slabDouble, self.stairSingle,
                                 self.brick, self.tnt, self.bookshelf, self.cobblestoneMossy,
                                 self.obsidian, self.torch]

blocks = Blocks()
