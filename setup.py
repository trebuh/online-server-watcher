#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
from setuptools import setup, find_packages
 
setup(
    name='online_watcher',
    version='0.0.1',
    author='Trebuh',
    author_email='trebuh@users.noreply.github.com',
    description='Sends a text if servers are available at Online',
    long_description=open('README.adoc').read(),
    url='https://github.com/trebuh/online-server-watcher',
    packages=find_packages(),
    install_requires=["requests", "html5lib", "bs4"],
    include_package_data=True,
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
            'online-watcher=online_watcher.__main__:main',
        ],
    },
)
