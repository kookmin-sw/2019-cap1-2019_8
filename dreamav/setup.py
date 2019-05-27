import glob
import os
from setuptools import setup, find_packages

from dreamav.__init__ import __ROOT__

def get_requirements():
    ret = []
    with open("./requirements.txt", "r") as f:
        for line in f.readlines():
            ret.append(line.strip())

    return ret


requires = get_requirements()
setup(
    name = 'dreamav',
    version = '0.2.7',
    description = "This package is for detecting malicious document",
    author = ["Damin Moon", "Kihwan Kim", "HyunSeok Kim", "Hyeri Jung", "Yuhan Bang"],
    author_email = "vmfn0401@gmail.com",
    license = "MIT",
    url = "https://github.com/kookmin-sw/2019-cap1-2019_8",
    packages=find_packages(),
    package_data = {
        "util": ["util/model/*"],
        "": ["*"]
    },
    zip_safe=False,
    setup_requires=requires,
    entry_points = {
        'console_scripts': [
            'dreamav = dreamav.__main__:main'
        ]
    })
