#!/bin/bash

PATH=/Users/dreed/bin:/usr/local/bin:$PATH

if [ ! -f grade.txt-save ]
then
    cp grade.txt grade.txt-save
fi

echo "" > blank
echo "#######################################################" > pound
cat blank pound blank > sep

