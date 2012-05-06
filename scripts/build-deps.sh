#!/bin/sh
echo; echo; echo will complain about emacsen-common and cmake-data
echo; echo
/scratchbox/login apt-get install build-essential cmake

echo; echo; echo should fix install issues
echo; echo
/scratchbox/login apt-get install cmake-data
/scratchbox/login apt-get install cmake
