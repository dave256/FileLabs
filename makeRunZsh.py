#!/usr/bin/env python3

# ----------------------------------------------------------------------
# makeMvLab.py
# Dave Reed
# 07/23/2020
# ----------------------------------------------------------------------

import argparse
import os
import os.path
import shutil
import pathlib

preScript=f"""#!/bin/zsh

PATH=$HOME/src/FileLabs:$HOME/Scripts:/usr/local/bin:$PATH
DIR=`dirname ${{(%):-%x}}`

# make certain file exists
if [ ! -f grade.txt ]; then
    touch grade.txt
fi

make_sep.sh
if [ -d $DIR/test ]; then
    /bin/cp -f $DIR/test/test*.py .
    testExists=true
fi

echo -e "\\ntest\\n" > test
echo -e "\\ndiff\\n" > diff
"""

postScript="""
##################################################

cat_messages_grade.sh
cleanup.sh
/bin/rm -f compile.txt diff test mytest yourtest
"""


def main():
    
    if os.path.exists("run.zsh"):
        print("run.zsh already exists; delete it if you want this script to create it")
        return
    
    parser = argparse.ArgumentParser(description='create script to mv files')
    parser.add_argument('files', type=str, nargs='+')

    args = parser.parse_args()

    files = []
    for f in args.files:
        lastSlash = f.rfind("/")
        if lastSlash != -1:
            f = f[lastSlash+1:]
        files.append(f)
    
    runLines = []
    count = 1
    for f in files:
        extension = pathlib.Path(f).suffix[1:]
        if extension == "py":
            cmd = f"echo -e "" | python3 {f} |& > out{count}.txt | cat"
        elif extension == "swift":
            cmd = f"swift {f} |& > out{count}.txt | cat"
        
        runLines.append(cmd)
        count += 1
    
    runLines = "\n".join(runLines)
    
    catCmd = []
    for i in range(1, count):
        catCmd.append(f"sep out{i}.txt")
        
    catCmd = f'cat {" ".join(catCmd)} sep grade.txt > new_grade'
    
    with open("run.zsh", 'w') as outfile:
        print(preScript, file=outfile)
        print(runLines, file=outfile)
        print(catCmd, file=outfile)
        print(postScript, file=outfile)
    os.system(f"chmod 755 run.zsh")


# ----------------------------------------------------------------------

main()