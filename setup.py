#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="peerly",
    version="0.1.0",
    description="Peerly is a p2p stuff indexer",
    author="Marti Zamora",
    license="MIT",
    url="https://github.com/z4m0/peerly",
    packages=find_packages(),
    install_requires=["gevent-socketio","peerlyDB"],
    #scripts=['peerly']
)
