# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""


import re
from setuptools import setup


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('stravalocker/stravalocker.py').read(),
    re.M
    ).group(1)


with open("README.rst", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(
    name = "stravalocker",
    packages = ["stravalocker"],
    entry_points = {
        "console_scripts": ['stravalocker = stravalocker.stravalocker:main']
        },
    version = version,
    description = "Python command line application bare bones template.",
    long_description = long_descr,
    author = "Chris Glass",
    author_email = "tribaal@gmail.com",
    url = "nope",
    )
