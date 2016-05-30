#!/usr/bin/env python3
# coding: utf-8
"""
    This program monitors the availability of a given list of servers
    provided by Online (https://www.online.net).
    When a watched server is available, it sends a text using the API
    provided by Free (French mobile provider https://mobile.free.fr/)
"""

from .core import OnlineWatcher

