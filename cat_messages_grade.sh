#!/bin/bash

if [ ! -f new_grade ]; then
    /bin/mv -f grade.txt new_grade
fi

if [ -f messages.txt ]; then
    make_sep.sh
    /bin/rm -f new_grade2
    cat sep messages.txt new_grade > new_grade2
else
    mv new_grade new_grade2
fi

/bin/mv -f new_grade2 grade.txt
