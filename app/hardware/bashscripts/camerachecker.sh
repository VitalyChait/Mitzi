#!/bin/bash

v4l2-ctl --list-devices | grep -A1 'Camera' | awk NR==2{print} | { read; echo "${REPLY#${REPLY%?}}";}
