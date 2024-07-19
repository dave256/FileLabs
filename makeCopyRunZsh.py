#!/usr/bin/env python3

# ----------------------------------------------------------------------
# makeCopyRunZsh.py
# Dave Reed
# 07/18/2024
# ----------------------------------------------------------------------

import argparse
import os
import os.path
import shutil
import pathlib

preScript = f"""#!/bin/zsh

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

echo -e "my test\\n" > mytest
echo -e "your test\\n" > yourtest
echo -e "\\ntest\\n" > test
echo -e "\\ndiff\\n" > diff
"""

postScript = """
##################################################

cat_messages_grade.sh
cleanup.sh
/bin/rm -f compile.txt diff test mytest yourtest
"""


def main():
    if os.path.exists("run.zsh"):
        print("run.zsh already exists; delete it if you want this script to create it")
        return

    parser = argparse.ArgumentParser(description='creates a run.zsh file that creates a copy.zsh file to copy files to a project directory for unit testing')
    parser.add_argument('-d', '--dest', help='destination directory to copy files to')
    parser.add_argument('-s', '--skip', action="store_true", default=False, help='skip running rmmain.py')
    parser.add_argument('files', type=str, nargs='+')

    args = parser.parse_args()

    files = []
    for f in args.files:
        lastSlash = f.rfind("/")
        if lastSlash != -1:
            f = f[lastSlash + 1:]
        files.append(f)

    # copy source files and test files (and file with "Tests" as part of filename)
    sourceFiles = list(filter(lambda f: not ("Tests" in f), files))
    testFiles = list(filter(lambda f: ("Tests" in f), files))

    joinedFiles = " ".join(files)
    sourceFiles = " ".join(sourceFiles)
    testFiles = " ".join(testFiles)

    runLines = []
    if not args.skip:
        runLines.append(f'rmmain.py {joinedFiles}')

    # remove extra spaces and make certain it ends in a slash
    dest = args.dest.strip()
    if dest[-1] != "/":
        dest += "/"

    if len(testFiles) > 0:
        # change to location where Swift package has its Tests files
        testDest = dest.replace("/Sources/", "/Tests/")
        testDest = testDest[:-1] + "Tests/"
        runLines.append(f'echo -e "/bin/cp -f {sourceFiles} {dest}; /bin/cp -f {testFiles} {testDest}" > copy.zsh')
    else:
        runLines.append(f'echo -e "/bin/cp -f {sourceFiles} {dest}" > copy.zsh')

    runLines.append("chmod 755 copy.zsh")
    runLines = "\n".join(runLines)

    with open("run.zsh", 'w') as outfile:
        print(preScript, file=outfile)
        print(runLines, file=outfile)
        print(postScript, file=outfile)
    os.system(f"chmod 755 run.zsh")

# ----------------------------------------------------------------------


if __name__ == "__main__":
    main()
