#!/bin/sh
project="n9-button-monitor"
dir="$HOME/$project/build"
/scratchbox/login mkdir -p $dir
/scratchbox/login -d $dir cmake ..
