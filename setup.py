from setuptools import setup, find_packages
from setuptools.extension import Extension
from Cython.Build import cythonize
from glob import glob

extensions = [
    Extension(name='mc.net.minecraft.level.Frustum',
              sources=['mc/net/minecraft/level/Frustum.pyx']),
    Extension(name='mc.net.minecraft.level.Chunk',
              sources=['mc/net/minecraft/level/Chunk.pyx']),
    Extension(name='mc.net.minecraft.level.Tesselator',
              sources=['mc/net/minecraft/level/Tesselator.pyx']),
    Extension(name='mc.net.minecraft.level.Level',
              sources=['mc/net/minecraft/level/Level.pyx']),
    Extension(name='mc.net.minecraft.level.Tile',
              sources=['mc/net/minecraft/level/Tile.pyx']),
    Extension(name='mc.net.minecraft.level.Tiles',
              sources=['mc/net/minecraft/level/Tiles.pyx']),
]

setup(
    name='minecraft-python',
    version='132328',
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
    packages=find_packages(),
    ext_modules=cythonize(extensions, annotate=False, language_level=3),
    zip_safe=False,
)
