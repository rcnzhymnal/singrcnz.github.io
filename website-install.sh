#!/bin/bash
# This script sets up python2.7 so that it can run website.py

wget https://bootstrap.pypa.io/pip/2.7/get-pip.py
python2 get-pip.py
python2 -m pip install future
rm get-pip.py
