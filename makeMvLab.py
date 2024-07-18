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

def main():
    parser = argparse.ArgumentParser(description="""create script to mv files
        example usage:
        makeMvLab.py mv.zsh -f a.py b.py ;
        makeMvLab.py mv.zsh -f a.py b.py -c file.zip (this creates check.zsh that will make file.zip) ;
        makeMvLab.py mv.zsh -d GradingDirectory -f a.py b.py (by default GradingDirectory is the last path in CWD)
    """)
    parser.add_argument('-d', '--dest', dest='dest', type=str, default=None, help='destination directory to put subdirectories and files in')
    parser.add_argument('scriptName', type=str, help='name of the script to create such as mv.zsh')
    parser.add_argument('-f', nargs='+', dest='files', help='files to find and move')
    parser.add_argument('-c', nargs='*', dest='checkFiles', help='files for check.zsh to use')

    args = parser.parse_args()
    dest = args.dest
    if dest is None:
        dest = os.getcwd().split(os.sep)[-1]

    filename = args.scriptName
    # insert mv if not first two characters
    if filename[:2] != 'mv':
        filename = f"mv{filename[0].upper()}{filename[1:]}"
    
    # if filename does not end with .zsh abort
    if filename.split(".")[-1] != "zsh":
        print("you probably forgot to enter the filename you wanted for the script so stopping to avoid overwriting your program files")
        print("makeMvLab.py mvScriptName.zsh [source files]")
        return

    files = []
    for f in args.files:
        lastSlash = f.rfind("/")
        if lastSlash != -1:
            f = f[lastSlash+1:]
        files.append(f)

    checkFiles = args.checkFiles
    if checkFiles is None or len(checkFiles) == 0:
        checkFiles = files

    files = ' '.join(files)
    with open(filename, 'w') as outfile:
        print("#!/bin/zsh\n", file=outfile)
        print(f"mvlab.py ../{dest} {files} help.txt", file=outfile)
    os.system(f"chmod 755 {filename}")

    files = ' '.join(checkFiles)
    filename = f"check{filename[2:]}"
    with open(filename, 'w') as outfile:
        print("#!/bin/zsh\n", file=outfile)
        print(f"maketest.py -a {' '.join(checkFiles)}", file=outfile)
    os.system(f"chmod 755 {filename}")

    cmd = f"""#!/bin/zsh

PATH=$HOME/src/FileLabs:$HOME/Scripts:/usr/local/bin:$PATH
. $HOME/Scripts/functions.zsh

# get directory of this script
SCRIPTDIR=`dirname $0:A`
cdSubDir {dest}

run_dir.py $SCRIPTDIR/run.zsh *
"""

    with open('rd.zsh', 'w') as outfile:
        print(cmd, file=outfile)
    os.system("chmod 755 rd.zsh")

# ----------------------------------------------------------------------

main()
