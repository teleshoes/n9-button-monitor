#!/bin/sh
project="n9-button-monitor"

/scratchbox/login -d $HOME find -maxdepth 1 -name $project*.deb -delete
/scratchbox/login -d $HOME find -maxdepth 1 -name $project*.changes -delete
/scratchbox/login -d $HOME find -maxdepth 1 -name $project*.dsc -delete
/scratchbox/login -d $HOME find -maxdepth 1 -name $project*.gz -delete

/scratchbox/login -d $HOME/$project dpkg-buildpackage

deb=`/scratchbox/login -d $HOME find -maxdepth 1 -name $project*.deb`
echo copying $deb from sbox $HOME to $HOME/$project
/scratchbox/login -d $HOME cp $deb $HOME/$project
