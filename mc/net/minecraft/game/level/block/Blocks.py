from mc.net.minecraft.game.level.block.Block import Block
from mc.net.minecraft.game.level.block.BlockSand import BlockSand
from mc.net.minecraft.game.level.block.BlockFire import BlockFire
from mc.net.minecraft.game.level.block.BlockFlowing import BlockFlowing
from mc.net.minecraft.game.level.block.BlockStationary import BlockStationary
from mc.net.minecraft.game.level.block.BlockBookshelf import BlockBookshelf
from mc.net.minecraft.game.level.block.BlockWorkbench import BlockWorkbench
from mc.net.minecraft.game.level.block.BlockSponge import BlockSponge
from mc.net.minecraft.game.level.block.BlockMushroom import BlockMushroom
from mc.net.minecraft.game.level.block.BlockChest import BlockChest
from mc.net.minecraft.game.level.block.BlockFlower import BlockFlower
from mc.net.minecraft.game.level.block.BlockGlass import BlockGlass
from mc.net.minecraft.game.level.block.BlockGrass import BlockGrass
from mc.net.minecraft.game.level.block.BlockGears import BlockGears
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
from mc.net.minecraft.game.level.block.BlockSource import BlockSource
from mc.net.minecraft.game.level.block.StepSound import StepSound
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

        self.soundPowderFootstep = StepSound('stone', 1.0, 1.0)
        self.soundWoodFootstep = StepSound('wood', 1.0, 1.0)
        self.soundGravelFootstep = StepSound('gravel', 1.0, 1.0)
        self.soundGrassFootstep = StepSound('grass', 1.0, 1.0)
        self.soundStoneFootstep = StepSound('stone', 1.0, 1.0)
        self.soundMetalFootstep = StepSound('stone', 1.0, 1.5)

        self.stone = BlockStone(self, 1, 1).setHardness(1.0).setResistance(10.0)
        self.stone.stepSound = self.soundStoneFootstep

        self.grass = BlockGrass(self, 2).setHardness(0.6)
        self.grass.stepSound = self.soundGrassFootstep

        self.dirt = BlockDirt(self, 3, 2).setHardness(0.5)
        self.dirt.stepSound = self.soundGravelFootstep
        self.cobblestone = Block(self, 4, 16).setHardness(1.5).setResistance(10.0)
        self.cobblestone.stepSound = self.soundStoneFootstep
        self.planks = Block(self, 5, 4).setHardness(1.5).setResistance(5.0)
        self.planks.stepSound = self.soundWoodFootstep
        self.sapling = BlockSapling(self, 6, 15).setHardness(0.0)
        self.sapling.stepSound = self.soundGrassFootstep
        self.bedrock = Block(self, 7, 17).setHardness(999.0).setResistance(6000000.0)
        self.bedrock.stepSound = self.soundStoneFootstep

        self.waterMoving = BlockFlowing(self, 8, Material.water).setHardness(100.0).setLightOpacity(4)
        self.waterStill = BlockStationary(self, 9, Material.water).setHardness(100.0).setLightOpacity(2)

        self.lavaMoving = BlockFlowing(self, 10, Material.lava).setHardness(0.0).setLightValue(1.0).setLightOpacity(255)
        self.lavaStill = BlockStationary(self, 11, Material.lava).setHardness(100.0).setLightValue(1.0).setLightOpacity(255)

        self.sand = BlockSand(self, 12, 18).setHardness(0.5)
        self.sand.stepSound = self.soundGravelFootstep
        self.gravel = BlockSand(self, 13, 19).setHardness(0.6)
        self.gravel.stepSound = self.soundGravelFootstep

        self.oreGold = BlockOre(self, 14, 32).setHardness(3.0).setResistance(5.0)
        self.oreGold.stepSound = self.soundStoneFootstep
        self.oreIron = BlockOre(self, 15, 33).setHardness(3.0).setResistance(5.0)
        self.oreIron.stepSound = self.soundStoneFootstep
        self.oreCoal = BlockOre(self, 16, 34).setHardness(3.0).setResistance(5.0)
        self.oreCoal.stepSound = self.soundStoneFootstep

        self.wood = BlockLog(self, 17).setHardness(2.5)
        self.wood.stepSound = self.soundWoodFootstep
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

        self.plantYellow = BlockFlower(self, 37, 13).setHardness(0.0)
        self.plantYellow.stepSound = self.soundGrassFootstep
        self.plantRed = BlockFlower(self, 38, 12).setHardness(0.0)
        self.plantRed.stepSound = self.soundGrassFootstep
        self.mushroomBrown = BlockMushroom(self, 39, 29).setHardness(0.0)
        self.mushroomBrown.stepSound = self.soundGrassFootstep
        self.mushroomRed = BlockMushroom(self, 40, 28).setHardness(0.0)
        self.mushroomRed.stepSound = self.soundGrassFootstep

        self.blockGold = BlockOreBlock(self, 41, 40).setHardness(3.0).setResistance(10.0)
        self.blockGold.stepSound = self.soundMetalFootstep
        self.blockSteel = BlockOreBlock(self, 42, 39).setHardness(5.0).setResistance(10.0)
        self.blockSteel.stepSound = self.soundMetalFootstep

        self.stairDouble = BlockStep(self, 43, True).setHardness(2.0).setResistance(10.0)
        self.stairDouble.stepSound = self.soundStoneFootstep
        self.stairSingle = BlockStep(self, 44, False).setHardness(2.0).setResistance(10.0)
        self.stairSingle.stepSound = self.soundStoneFootstep

        self.brick = Block(self, 45, 7).setHardness(2.0).setResistance(10.0)
        self.brick.stepSound = self.soundStoneFootstep

        self.tnt = BlockTNT(self, 46, 8).setHardness(0.0)
        self.tnt.stepSound = self.soundGrassFootstep

        self.bookShelf = BlockBookshelf(self, 47, 35).setHardness(1.5)
        self.bookShelf.stepSound = self.soundWoodFootstep

        self.cobblestoneMossy = Block(self, 48, 36).setHardness(1.0)
        self.cobblestoneMossy.stepSound = self.soundStoneFootstep
        self.obsidian = BlockStone(self, 49, 37).setHardness(10.0).setResistance(10.0)
        self.obsidian.stepSound = self.soundStoneFootstep

        self.torch = BlockTorch(self, 50, 80).setHardness(0.0).setLightValue(14.0 / 16.0)
        self.torch.stepSound = self.soundWoodFootstep
        self.fire = BlockFire(self, 51, 31).setHardness(0.0).setLightValue(1.0)
        self.fire.stepSound = self.soundWoodFootstep

        self.waterSource = BlockSource(self, 52, self.waterMoving.blockID).setHardness(0.0)
        self.waterSource.stepSound = self.soundWoodFootstep
        self.blocksList[52] = self.waterSource
        self.lavaSource = BlockSource(self, 53, self.lavaMoving.blockID).setHardness(0.0)
        self.lavaSource.stepSound = self.soundWoodFootstep
        self.blocksList[53] = self.lavaSource

        self.chest = BlockChest(self, 54).setHardness(2.5)
        self.chest.stepSound = self.soundWoodFootstep

        self.cog = BlockGears(self, 55, 62).setHardness(0.5)
        self.cog.stepSound = self.soundMetalFootstep

        self.oreDiamond = BlockOre(self, 56, 50).setHardness(3.0).setResistance(5.0)
        self.oreDiamond.stepSound = self.soundStoneFootstep
        self.blockDiamond = BlockOreBlock(self, 57, 104).setHardness(5.0).setResistance(10.0)
        self.blockDiamond.stepSound = self.soundMetalFootstep

        self.workbench = BlockWorkbench(self, 58).setHardness(2.5)
        self.workbench.stepSound = self.soundWoodFootstep

blocks = Blocks()
