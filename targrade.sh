#!/bin/bash

if [ -d "Grade" ]; then
    cd Grade
fi

find . | grep part|grep -E "(html|ksh|ATT.*\.htm)" | xargs /bin/rm
find . | grep __MACOSX | xargs /bin/rm -rf
find . | grep -E "ATT.*\.htm" | xargs /bin/rm
find . | grep -E "ATT.*\.txt" | xargs /bin/rm

cd ..
tar zcvf Grade.tar.gz Grade
cd Grade
