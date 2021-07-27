#!/bin/bash

whereis pip
whereis wget
whereis zip
whereis unzip
whereis python

pip3.9 install ccm && wget https://github.com/zegelin/ccm-extensions/archive/refs/heads/master.zip && unzip master.zip && cd ccm-extensions-master && python3.9 setup.py install