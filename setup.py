#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from setuptools import setup, find_packages
 
import online_watcher
 
setup(
    name=online_watcher.__title__,
    version=online_watcher.__version__,
    packages=find_packages(),
    author=online_watcher.__author__,
    author_email="trebuh@users.noreply.github.com",
    description="Sends a text if servers are available at Online",
    long_description=open('README.adoc').read(),
    install_requires=["requests", "html5lib", "bs4"],
    include_package_data=True,
    url=online_watcher.__repo__,
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Internet",
    ],
    entry_points = {
        'console_scripts': [
            'online-watcher=online_watcher.online_watcher:main',
        ],
    },
)
