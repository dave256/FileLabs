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
    joinedFiles = " ".join(files)
    runLines = []
    if not args.skip:
        runLines.append(f'rmmain.py {joinedFiles}')
    runLines.append(f'echo -e "/bin/cp -f {joinedFiles} {args.dest}" > copy.zsh')
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
