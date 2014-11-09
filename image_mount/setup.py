#!/usr/bin/env python3

import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "image_mount",
    version = "0.0.1",
    author = "Thammi",
    author_email = "thammi@chaossource.net",
    description = ("Create mount commands for disk images"),
    license = "GPLv3",
    keywords = "linux mount",
    url = "https://github.com/thammi/stuff",
    packages=['image_mount'],
    long_description=read('README.md'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
    ],
    entry_points={
        'console_scripts': [
            'image_mount = image_mount.image_mount:main',
            ],
        },
)

