#!/bin/zsh

PATH=$HOME/src/FileLabs:$PATH
. ~/.GradeA

extractLabs.py $1
/bin/mv -f $1 $1.processed
