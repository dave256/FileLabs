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
#if [ -d $DIR/test ]; then
#    /bin/cp -f $DIR/test/test*.py .
#    testExists=true
#fi

# ln -s ~/Downloads/graphics.py .

echo -e "my test\\n" > mytest
echo -e "your test\\n" > yourtest
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
    
    parser = argparse.ArgumentParser(description='make run.zsh based on files')
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
    testOut = []
    outputCount = 1

    if len(files) == 1 and (files[0] == "zip" or files[0][-4:] == ".zip"):
        runLines = r"""
unzip -o Archive.zip
/bin/rm -rf __MACOSX Archive.zip-save
# copy all files with .swift extension to current directory
find . -type f -name "*.swift" -exec cp {} . \;
/bin/rm -f EmptyWidthStacks.swift EqualWidthStacks.swift SwiftUIHelpers.swift
cat sep grade.txt > new_grade        
"""
        catCmd = "cat sep grade.txt > new_grade"
    else:
        for f in files:
            extension = pathlib.Path(f).suffix[1:]
            if extension == "py":
                testName = f"test_{f}"
                testPath = None
                # look for unit test files
                for path in (".", "test", '..', '../test'):
                    localPath = f"{path}/{testName}"
                    if os.path.exists(localPath):
                        testPath = localPath
                        break
                if testPath is not None:
                    myTestName = f"myTest{f[0].upper() + f[1:]}"
                    cmd = f'/bin/cp $DIR/{testPath} {myTestName}'
                    runLines.append(cmd)
                    cmd = f'python3 {myTestName} |& > test{count}.txt | cat'
                    runLines.append(cmd)
                    testOut.append(f"test{count}.txt")
                # run student submission with two different inputs
                cmd = f'echo -e "" | python3 {f} |& > out{outputCount}.txt | cat\necho -e "" | python3 {f} |& > out{outputCount + 1}.txt | cat'
                outputCount += 2


            elif extension == "swift":
                cmd = f'swift {f} |& > out{outputCount}.txt | cat'
                outputCount += 1

            elif extension == "cpp":
                exe = f.split('.')[0]
                cmd = f"clang++ -std=c++20 -o {exe} {f} |& > com{count}.txt | cat"
                runLines.append(cmd)
                cmd = f"./{exe} |& > out{count}.txt | cat"
                outputCount += 1
            runLines.append(cmd)
            count += 1

        runLines = "\n".join(runLines)

        catCmd = []
        if len(testOut) > 0:
            catCmd.append("sep mytest blank")
            for i, s in enumerate(testOut):
                if i == 0:
                    catCmd.append(s)
                else:
                    catCmd.append(f"sep {s}")
        for i in range(1, outputCount):
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