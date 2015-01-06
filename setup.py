# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name="imagesort",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'ExifRead>=1.4.0',
    ],

    author="Børge Lanes",
    author_email="borge.lanes@gmail.com",
    description=("Sort images according to date from exif metadata"),
    license="MIT",
    keywords="media",
    entry_points={
        'console_scripts': [
            'imagesort = imagesort.imagesort:main',
        ]
    }
)
