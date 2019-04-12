# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""


import re
from setuptools import setup


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('hurtlocker/hurtlocker.py').read(),
    re.M
    ).group(1)


with open("README.rst", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(
    name = "hurtlocker",
    packages = ["hurtlocker"],
    entry_points = {
        "console_scripts": ['hurtlocker = hurtlocker.hurtlocker:main']
        },
    version = version,
    description = "A sadistic lockscreen that requires you to go for a run.",
    long_description = long_descr,
    author = "Chris Glass",
    author_email = "tribaal@gmail.com",
    url = "nope",
    )
