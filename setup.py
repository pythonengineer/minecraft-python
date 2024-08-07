from setuptools import setup, find_packages
from setuptools.extension import Extension
from Cython.Build import cythonize
from glob import glob

import numpy

flags = {'define_macros': [('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION')]}

extensions = [
    Extension(name='mc.JavaUtils',
              sources=['mc/JavaUtils.pyx'],
              include_dirs=[numpy.get_include()], **flags),
    Extension(name='mc.net.minecraft.game.entity.Entity',
              sources=['mc/net/minecraft/game/entity/Entity.pyx'],
              include_dirs=[numpy.get_include()], **flags),
    Extension(name='mc.net.minecraft.game.entity.EntityLiving',
              sources=['mc/net/minecraft/game/entity/EntityLiving.pyx'],
              include_dirs=[numpy.get_include()], **flags),
    Extension(name='mc.net.minecraft.game.entity.AILiving',
              sources=['mc/net/minecraft/game/entity/AILiving.pyx'],
              include_dirs=[numpy.get_include()], **flags),
    Extension(name='mc.net.minecraft.game.physics.AxisAlignedBB',
              sources=['mc/net/minecraft/game/physics/AxisAlignedBB.pyx'], **flags),
    Extension(name='mc.net.minecraft.client.gui.FontRenderer',
              sources=['mc/net/minecraft/client/gui/FontRenderer.pyx'], **flags),
    Extension(name='mc.net.minecraft.client.render.Frustum',
              sources=['mc/net/minecraft/client/render/Frustum.pyx'],
              include_dirs=[numpy.get_include()], **flags),
    Extension(name='mc.net.minecraft.client.render.WorldRenderer',
              sources=['mc/net/minecraft/client/render/WorldRenderer.pyx'],
              include_dirs=[numpy.get_include()], **flags),
    Extension(name='mc.net.minecraft.client.render.Tessellator',
              sources=['mc/net/minecraft/client/render/Tessellator.pyx'],
              include_dirs=[numpy.get_include()], **flags),
    Extension(name='mc.net.minecraft.client.render.RenderBlocks',
              sources=['mc/net/minecraft/client/render/RenderBlocks.pyx'],
              include_dirs=[numpy.get_include()], **flags),
    Extension(name='mc.net.minecraft.client.render.RenderGlobal',
              sources=['mc/net/minecraft/client/render/RenderGlobal.pyx'],
              include_dirs=[numpy.get_include()], **flags),
    Extension(name='mc.net.minecraft.client.render.texture.TextureFX',
              sources=['mc/net/minecraft/client/render/texture/TextureFX.pyx'], **flags),
    Extension(name='mc.net.minecraft.client.render.texture.TextureFlamesFX',
              sources=['mc/net/minecraft/client/render/texture/TextureFlamesFX.pyx'],
              include_dirs=[numpy.get_include()], **flags),
    Extension(name='mc.net.minecraft.client.render.texture.TextureGearsFX',
              sources=['mc/net/minecraft/client/render/texture/TextureGearsFX.pyx'],
              include_dirs=[numpy.get_include()], **flags),
    Extension(name='mc.net.minecraft.client.render.texture.TextureLavaFX',
              sources=['mc/net/minecraft/client/render/texture/TextureLavaFX.pyx'],
              include_dirs=[numpy.get_include()], **flags),
    Extension(name='mc.net.minecraft.client.render.texture.TextureWaterFX',
              sources=['mc/net/minecraft/client/render/texture/TextureWaterFX.pyx'],
              include_dirs=[numpy.get_include()], **flags),
    Extension(name='mc.net.minecraft.client.render.texture.TextureWaterFlowFX',
              sources=['mc/net/minecraft/client/render/texture/TextureWaterFlowFX.pyx'],
              include_dirs=[numpy.get_include()], **flags),
    Extension(name='mc.net.minecraft.client.effect.EntityFX',
              sources=['mc/net/minecraft/client/effect/EntityFX.pyx'],
              include_dirs=[numpy.get_include()], **flags),
    Extension(name='mc.net.minecraft.game.level.World',
              sources=['mc/net/minecraft/game/level/World.pyx'],
              include_dirs=[numpy.get_include()], **flags),
    Extension(name='mc.net.minecraft.game.level.EntityMap',
              sources=['mc/net/minecraft/game/level/EntityMap.pyx'],
              include_dirs=[numpy.get_include()], **flags),
    Extension(name='mc.net.minecraft.game.level.EntityMapSlot',
              sources=['mc/net/minecraft/game/level/EntityMapSlot.pyx'],
              include_dirs=[numpy.get_include()], **flags),
    Extension(name='mc.net.minecraft.game.level.generator.LevelGenerator',
              sources=['mc/net/minecraft/game/level/generator/LevelGenerator.pyx'],
              include_dirs=[numpy.get_include()], **flags),
    Extension(name='mc.net.minecraft.game.level.generator.noise.NoiseGeneratorDistort',
              sources=['mc/net/minecraft/game/level/generator/noise/NoiseGeneratorDistort.pyx'], **flags),
    Extension(name='mc.net.minecraft.game.level.generator.noise.NoiseGeneratorOctaves',
              sources=['mc/net/minecraft/game/level/generator/noise/NoiseGeneratorOctaves.pyx'],
              include_dirs=[numpy.get_include()], **flags),
    Extension(name='mc.net.minecraft.game.level.generator.noise.NoiseGeneratorPerlin',
              sources=['mc/net/minecraft/game/level/generator/noise/NoiseGeneratorPerlin.pyx'],
              include_dirs=[numpy.get_include()], **flags),
    Extension(name='mc.net.minecraft.game.level.block.Block',
              sources=['mc/net/minecraft/game/level/block/Block.pyx'],
              include_dirs=[numpy.get_include()], **flags),
    Extension(name='mc.net.minecraft.game.level.block.BlockFluid',
              sources=['mc/net/minecraft/game/level/block/BlockFluid.pyx'],
              include_dirs=[numpy.get_include()], **flags),
    Extension(name='mc.net.minecraft.game.level.block.BlockFlowing',
              sources=['mc/net/minecraft/game/level/block/BlockFlowing.pyx'],
              include_dirs=[numpy.get_include()], **flags),
    Extension(name='mc.net.minecraft.game.level.block.BlockFire',
              sources=['mc/net/minecraft/game/level/block/BlockFire.pyx'],
              include_dirs=[numpy.get_include()], **flags),
]

setup(
    name='minecraft-python',
    version='0.31.20100131',
    author='pythonengineer',
    description='A project that seeks to recreate every old Minecraft version in Python using Pyglet and Cython.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='BSD',
    url='https://github.com/pythonengineer/minecraft-python',
    download_url='https://pypi.org/project/minecraft-python',
    project_urls={
        'Source': 'https://github.com/pythonengineer/minecraft-python',
        'Tracker': 'https://github.com/pythonengineer/minecraft-python/issues',
    },
    python_requires='>=3.9',
    keywords='minecraft pyglet cython sandbox game classic',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Games/Entertainment',
    ],
    exclude_package_data={
        '': ['*.c', '*.html', '*.pyc'],
    },
    package_data={
        '': ['*.png', '*.ogg', '*.md3', '*.MD3', '*.dll'],
    },
    packages=find_packages(),
    ext_modules=cythonize(extensions, annotate=False, language_level=3),
    include_package_data=True,
    zip_safe=False,
)
