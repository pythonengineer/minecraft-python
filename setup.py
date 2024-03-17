from setuptools import setup, find_packages
from setuptools.extension import Extension
from Cython.Build import cythonize
from glob import glob

extensions = [
    Extension(name='mc.cCompatibilityShims',
              sources=['mc/cCompatibilityShims.pyx']),
    Extension(name='mc.net.minecraft.Entity',
              sources=['mc/net/minecraft/Entity.pyx']),
    Extension(name='mc.net.minecraft.mob.Mob',
              sources=['mc/net/minecraft/mob/Mob.pyx']),
    Extension(name='mc.net.minecraft.mob.ai.BasicAI',
              sources=['mc/net/minecraft/mob/ai/BasicAI.pyx']),
    Extension(name='mc.net.minecraft.phys.AABB',
              sources=['mc/net/minecraft/phys/AABB.pyx']),
    Extension(name='mc.net.minecraft.renderer.Frustum',
              sources=['mc/net/minecraft/renderer/Frustum.pyx']),
    Extension(name='mc.net.minecraft.renderer.Chunk',
              sources=['mc/net/minecraft/renderer/Chunk.pyx']),
    Extension(name='mc.net.minecraft.renderer.Tesselator',
              sources=['mc/net/minecraft/renderer/Tesselator.pyx']),
    Extension(name='mc.net.minecraft.renderer.texture.DynamicTexture',
              sources=['mc/net/minecraft/renderer/texture/DynamicTexture.pyx']),
    Extension(name='mc.net.minecraft.renderer.texture.LavaTexture',
              sources=['mc/net/minecraft/renderer/texture/LavaTexture.pyx']),
    Extension(name='mc.net.minecraft.renderer.texture.WaterTexture',
              sources=['mc/net/minecraft/renderer/texture/WaterTexture.pyx']),
    Extension(name='mc.net.minecraft.particle.Particle',
              sources=['mc/net/minecraft/particle/Particle.pyx']),
    Extension(name='mc.net.minecraft.particle.SmokeParticle',
              sources=['mc/net/minecraft/particle/SmokeParticle.pyx']),
    Extension(name='mc.net.minecraft.level.Level',
              sources=['mc/net/minecraft/level/Level.pyx']),
    Extension(name='mc.net.minecraft.level.BlockMap',
              sources=['mc/net/minecraft/level/BlockMap.pyx']),
    Extension(name='mc.net.minecraft.level.Slot',
              sources=['mc/net/minecraft/level/Slot.pyx']),
    Extension(name='mc.net.minecraft.level.levelgen.LevelGen',
              sources=['mc/net/minecraft/level/levelgen/LevelGen.pyx']),
    Extension(name='mc.net.minecraft.level.levelgen.synth.Distort',
              sources=['mc/net/minecraft/level/levelgen/synth/Distort.pyx']),
    Extension(name='mc.net.minecraft.level.levelgen.synth.PerlinNoise',
              sources=['mc/net/minecraft/level/levelgen/synth/PerlinNoise.pyx']),
    Extension(name='mc.net.minecraft.level.levelgen.synth.ImprovedNoise',
              sources=['mc/net/minecraft/level/levelgen/synth/ImprovedNoise.pyx']),
    Extension(name='mc.net.minecraft.level.liquid.Liquid',
              sources=['mc/net/minecraft/level/liquid/Liquid.pyx']),
    Extension(name='mc.net.minecraft.level.tile.Tile',
              sources=['mc/net/minecraft/level/tile/Tile.pyx']),
    Extension(name='mc.net.minecraft.level.tile.Tiles',
              sources=['mc/net/minecraft/level/tile/Tiles.pyx']),
    Extension(name='mc.net.minecraft.level.tile.FallingTile',
              sources=['mc/net/minecraft/level/tile/FallingTile.pyx']),
    Extension(name='mc.net.minecraft.level.tile.Flower',
              sources=['mc/net/minecraft/level/tile/Flower.pyx']),
    Extension(name='mc.net.minecraft.level.tile.LiquidTile',
              sources=['mc/net/minecraft/level/tile/LiquidTile.pyx']),
]

setup(
    name='minecraft-python',
    version='0.30',
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
    python_requires='>=3.6',
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
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Games/Entertainment',
    ],
    exclude_package_data={
        '': ['*.c', '*.html', '*.pyc'],
    },
    package_data={
        '': ['*.png', '*.ogg'],
    },
    packages=find_packages(),
    ext_modules=cythonize(extensions, annotate=False, language_level=3),
    include_package_data=True,
    zip_safe=False,
)
