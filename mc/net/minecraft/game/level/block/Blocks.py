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
        self.isBlockContainer = [False] * 256
        self.lightValue = [0] * 256

        self.stone = BlockStone(self, 1, 1).setHardness(1.0)

        self.grass = BlockGrass(self).setHardness(0.6)
        self.dirt = BlockDirt(self).setHardness(0.5)
        self.cobblestone = Block(self, 4, 16).setHardness(1.5)
        self.planks = Block(self, 5, 4).setHardness(1.5)
        self.sapling = BlockSapling(self, 6).setHardness(0.0)
        self.bedrock = Block(self, 7, 17).setHardness(999.0)

        self.waterMoving = BlockFluid(self, 8, Material.water).setHardness(100.0).setLightOpacity(2)
        self.waterStill = BlockStationary(self, 9, Material.water).setHardness(100.0).setLightOpacity(2)

        self.lavaMoving = BlockFluid(self, 10, Material.lava).setHardness(0.0).setLightValue(0.8)
        self.lavaStill = BlockStationary(self, 11, Material.lava).setHardness(100.0).setLightValue(0.8)

        self.sand = BlockSand(self, 12, 18).setHardness(0.5)
        self.gravel = BlockSand(self, 13, 19).setHardness(0.6)

        self.oreGold = BlockOre(self, 14, 32).setHardness(3.0)
        self.oreIron = BlockOre(self, 15, 33).setHardness(3.0)
        self.oreCoal = BlockOre(self, 16, 34).setHardness(3.0)

        self.log = BlockLog(self).setHardness(2.5)
        self.leaves = BlockLeaves(self).setHardness(0.2).setLightOpacity(1)

        self.sponge = BlockSponge(self).setHardness(0.6)
        self.glass = BlockGlass(self).setHardness(0.3)

        self.clothRed = Block(self, 21, 64).setHardness(0.8)
        self.clothOrange = Block(self, 22, 65).setHardness(0.8)
        self.clothYellow = Block(self, 23, 66).setHardness(0.8)
        self.clothChartreuse = Block(self, 24, 67).setHardness(0.8)
        self.clothGreen = Block(self, 25, 68).setHardness(0.8)
        self.clothSpringGreen = Block(self, 26, 69).setHardness(0.8)
        self.clothCyan = Block(self, 27, 70).setHardness(0.8)
        self.clothCapri = Block(self, 28, 71).setHardness(0.8)
        self.clothUltramarine = Block(self, 29, 72).setHardness(0.8)
        self.clothViolet = Block(self, 30, 73).setHardness(0.8)
        self.clothPurple = Block(self, 31, 74).setHardness(0.8)
        self.clothMagenta = Block(self, 32, 75).setHardness(0.8)
        self.clothRose = Block(self, 33, 76).setHardness(0.8)
        self.clothDarkGray = Block(self, 34, 77).setHardness(0.8)
        self.clothGray = Block(self, 35, 78).setHardness(0.8)
        self.clothWhite = Block(self, 36, 79).setHardness(0.8)

        self.plantYellow = BlockFlower(self, 37, 13).setHardness(0.0)
        self.plantRed = BlockFlower(self, 38, 12).setHardness(0.0)

        self.mushroomBrown = BlockMushroom(self, 39, 29).setHardness(0.0)
        self.mushroomRed = BlockMushroom(self, 40, 28).setHardness(0.0)

        self.goldBlock = BlockOreBlock(self, 41, 40).setHardness(3.0)
        self.ironBlock = BlockOreBlock(self, 42, 39).setHardness(5.0)

        self.stairDouble = BlockStep(self, 43, True).setHardness(2.0)
        self.stairSingle = BlockStep(self, 44, False).setHardness(2.0)

        self.brick = Block(self, 45, 7).setHardness(2.0)

        self.tnt = BlockTNT(self).setHardness(0.0)

        self.bookShelf = BlockBookshelf(self).setHardness(1.5)

        self.cobblestoneMossy = Block(self, 48, 36).setHardness(1.0)
        self.obsidian = BlockStone(self, 49, 37).setHardness(10.0)

        self.torch = BlockTorch(self).setHardness(0.0).setLightValue(1.0)

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
