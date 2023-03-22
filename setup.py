# -*- coding: utf-8 -*-

import codecs
import os
from setuptools import setup, find_packages

# these things are needed for the README.md show on pypi (if you dont need delete it)
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

# you need to change all these
VERSION = '0.0.2'
DESCRIPTION = 'This is a great library'
LONG_DESCRIPTION = 'wies_library This is a great library'

setup(
    name="wies_library",
    version=VERSION,
    author='zhengduoduo',
    author_email='1512945835@qq.com',
    url='https://github.com/wieszheng/Cprint',
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[
        'loguru==0.6.0','edge-tts',
    ],
    keywords=['python','windows','mac','linux'],
    license='MIT',
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
