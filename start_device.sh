#!/bin/bash

source tankvenv/bin/activate

trap "kill 0" EXIT

esphome run mopeka_ble.yaml > output.txt 2>&1 &
python guiScript.py &

wait
