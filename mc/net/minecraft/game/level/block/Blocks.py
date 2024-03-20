from mc.net.minecraft.game.level.block.Block import Block
from mc.net.minecraft.game.level.block.BlockSand import BlockSand
from mc.net.minecraft.game.level.block.BlockFluid import BlockFluid
from mc.net.minecraft.game.level.block.BlockStationary import BlockStationary
from mc.net.minecraft.game.level.block.BlockBookshelf import BlockBookshelf
from mc.net.minecraft.game.level.block.BlockSponge import BlockSponge
from mc.net.minecraft.game.level.block.BlockMushroom import BlockMushroom
from mc.net.minecraft.game.level.block.BlockFlower import BlockFlower
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

        self.stone = BlockStone(self, 1, 1).setResistance(1.0)
        self.stone.blockIsDropped = False

        self.grass = BlockGrass(self).setResistance(0.6)
        self.dirt = BlockDirt(self).setResistance(0.5)
        self.cobblestone = Block(self, 4, 16).setResistance(1.5)
        self.cobblestone.blockIsDropped = False
        self.planks = Block(self, 5, 4).setResistance(1.5)
        self.sapling = BlockSapling(self, 6).setResistance(0.0)
        self.bedrock = Block(self, 7, 17).setResistance(999.0)
        self.bedrock.blockIsDropped = False

        self.waterMoving = BlockFluid(self, 8, Material.water).setResistance(100.0).setLightOpacity(2)
        self.waterStill = BlockStationary(self, 9, Material.water).setResistance(100.0).setLightOpacity(2)

        self.lavaMoving = BlockFluid(self, 10, Material.lava).setResistance(0.0).setLightValue(0.8).setLightOpacity(255)
        self.lavaStill = BlockStationary(self, 11, Material.lava).setResistance(100.0).setLightValue(0.8).setLightOpacity(255)

        self.sand = BlockSand(self, 12, 18).setResistance(0.5)
        self.gravel = BlockSand(self, 13, 19).setResistance(0.6)

        self.oreGold = BlockOre(self, 14, 32).setResistance(3.0)
        self.oreGold.blockIsDropped = False
        self.oreIron = BlockOre(self, 15, 33).setResistance(3.0)
        self.oreIron.blockIsDropped = False
        self.oreCoal = BlockOre(self, 16, 34).setResistance(3.0)
        self.oreCoal.blockIsDropped = False

        self.log = BlockLog(self).setResistance(2.5)
        self.leaves = BlockLeaves(self).setResistance(0.2).setLightOpacity(1)

        self.sponge = BlockSponge(self).setResistance(0.6)
        self.glass = BlockGlass(self).setResistance(0.3)

        self.clothRed = Block(self, 21, 64).setResistance(0.8)
        self.clothOrange = Block(self, 22, 65).setResistance(0.8)
        self.clothYellow = Block(self, 23, 66).setResistance(0.8)
        self.clothChartreuse = Block(self, 24, 67).setResistance(0.8)
        self.clothGreen = Block(self, 25, 68).setResistance(0.8)
        self.clothSpringGreen = Block(self, 26, 69).setResistance(0.8)
        self.clothCyan = Block(self, 27, 70).setResistance(0.8)
        self.clothCapri = Block(self, 28, 71).setResistance(0.8)
        self.clothUltramarine = Block(self, 29, 72).setResistance(0.8)
        self.clothViolet = Block(self, 30, 73).setResistance(0.8)
        self.clothPurple = Block(self, 31, 74).setResistance(0.8)
        self.clothMagenta = Block(self, 32, 75).setResistance(0.8)
        self.clothRose = Block(self, 33, 76).setResistance(0.8)
        self.clothDarkGray = Block(self, 34, 77).setResistance(0.8)
        self.clothGray = Block(self, 35, 78).setResistance(0.8)
        self.clothWhite = Block(self, 36, 79).setResistance(0.8)

        self.plantYellow = BlockFlower(self, 37, 13).setResistance(0.0)
        self.plantRed = BlockFlower(self, 38, 12).setResistance(0.0)

        self.mushroomBrown = BlockMushroom(self, 39, 29).setResistance(0.0)
        self.mushroomRed = BlockMushroom(self, 40, 28).setResistance(0.0)

        self.goldBlock = BlockOreBlock(self, 41, 40).setResistance(3.0)
        self.goldBlock.blockIsDropped = False
        self.ironBlock = BlockOreBlock(self, 42, 39).setResistance(5.0)
        self.ironBlock.blockIsDropped = False

        self.stairDouble = BlockStep(self, 43, True).setResistance(2.0)
        self.stairDouble.blockIsDropped = False
        self.stairSingle = BlockStep(self, 44, False).setResistance(2.0)
        self.stairSingle.blockIsDropped = False

        self.brick = Block(self, 45, 7).setResistance(2.0)
        self.brick.blockIsDropped = False

        self.tnt = BlockTNT(self).setResistance(0.0)

        self.bookShelf = BlockBookshelf(self).setResistance(1.5)

        self.cobblestoneMossy = Block(self, 48, 36).setResistance(1.0)
        self.cobblestoneMossy.blockIsDropped = False
        self.obsidian = BlockStone(self, 49, 37).setResistance(10.0)
        self.obsidian.blockIsDropped = False

        self.torch = BlockTorch(self).setResistance(0.0).setLightValue(1.0)

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
                                 self.ironBlock, self.stairDouble, self.stairSingle,
                                 self.brick, self.tnt, self.bookShelf, self.cobblestoneMossy,
                                 self.obsidian, self.torch]

blocks = Blocks()
