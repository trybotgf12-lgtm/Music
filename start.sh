#!/bin/sh
node /opt/bgutil/server/build/main.js &
sleep 3
python3 main.py
