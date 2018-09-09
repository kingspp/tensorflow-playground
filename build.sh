#!/bin/bash

sudo pkill -f python
nohup python3 tfplay.py -r "$1".py | tee build.out