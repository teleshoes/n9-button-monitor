#!/bin/sh
project="n9-button-monitor"
dir=$HOME/Code/$project
mnt=/scratchbox/users/$USER/home/$USER/$project

if ! mount | grep "$project on $mnt"; then
  sudo /scratchbox/sbin/sbox_ctl start
  sudo /scratchbox/sbin/sbox_sync

  mkdir -p $mnt
  sudo mount -o bind $dir $mnt
fi


/scratchbox/login -d $HOME find -maxdepth 2 -name $project*.deb -delete
/scratchbox/login -d $HOME find -maxdepth 2 -name $project*.changes -delete
/scratchbox/login -d $HOME find -maxdepth 2 -name $project*.dsc -delete
/scratchbox/login -d $HOME find -maxdepth 2 -name $project*.gz -delete

/scratchbox/login -d $HOME/$project dpkg-buildpackage

deb=`/scratchbox/login -d $HOME find -maxdepth 1 -name $project*.deb`
echo copying $deb from sbox $HOME to $HOME/$project
/scratchbox/login -d $HOME cp $deb $HOME/$project
