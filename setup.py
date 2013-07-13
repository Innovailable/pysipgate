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
    name = "pysipgate",
    version = "0.1.0",
    author = "Thammi",
    author_email = "thammi@chaossource.net",
    description = ("Client for the Sipgate API"),
    license = "GPLv3",
    keywords = "sipgate",
    url = "https://github.com/thammi/pysipgate",
    packages=['pysipgate'],
    data_files=[('img', ['img/phone_icon.png'])],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Topic :: Communications :: Telephony",
    ],
    entry_points={
        'console_scripts': [
            'pysipgate = pysipgate.main:main',
            ],
        },
)

