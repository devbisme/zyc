#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import sys
from setuptools import setup, find_packages

__author__ = "Dave Vandenbout"
__email__ = "devbisme@xess.com"
__version__ = "1.0.0"

if "sdist" in sys.argv[1:]:
    with open("zyc/pckg_info.py", "w") as f:
        for name in ["__version__", "__author__", "__email__"]:
            f.write("{} = '{}'\n".format(name, locals()[name]))

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "skidl >= 0.0.27",
    "kinparse >= 0.1.0",
    'enum34; python_version < "3.0"',
    "wxpython >= 4.0.7",
    "pykicad",
]

setup_requirements = []

test_requirements = []

setup(
    author=__author__,
    author_email=__email__,
    version=__version__,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Manufacturing",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
    ],
    description="A GUI for searching and selecting parts and footprints for use in SKiDL.",
    entry_points={"gui_scripts": ["zyc = zyc.zyc:main"]},
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="zyc",
    name="zyc",
    packages=find_packages(include=["zyc"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/devbisme/zyc",
    project_urls={
        "Documentation": "https://devbisme.github.io/zyc",
        "Source": "https://github.com/devbisme/zyc",
        "Changelog": "https://github.com/devbisme/zyc/blob/master/HISTORY.rst",
        "Tracker": "https://github.com/devbisme/zyc/issues",
    },
    zip_safe=False,
)
