#!/bin/zsh

PATH=$HOME/src/FileLabs:$PATH
. ~/.zshenv

extractLabs.py $1
/bin/mv -f $1 $1.processed
