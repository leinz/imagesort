# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os


def read(fname, skiplines=0):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        lines = f.readlines()[skiplines:]
        return ''.join(lines)


setup(
    name="imagesort",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'ExifRead>=1.4.0',
    ],
    include_package_data=True,

    author="Børge Lanes",
    author_email="borge.lanes@gmail.com",
    description=('Organize images according to exif date metadata.'),
    long_description=read("README.rst", 7),
    license="MIT",
    keywords="media",
    url="https://github.com/leinz/imagesort",

    entry_points={
        'console_scripts': [
            'imagesort = imagesort.imagesort:main',
        ]
    },

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Multimedia',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)
