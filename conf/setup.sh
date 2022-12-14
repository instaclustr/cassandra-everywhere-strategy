#!/bin/bash

sudo apt-get update
sudo apt-get --allow-downgrades --allow-remove-essential --allow-change-held-packages install libev4 libev-dev

pip3.9 install ccm && wget https://github.com/smiklosovic/ccm-extensions/archive/refs/heads/master.zip && unzip master.zip && cd ccm-extensions-master && python3.9 setup.py install
