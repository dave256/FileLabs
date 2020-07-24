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
    parser = argparse.ArgumentParser(description='create script to mv files')
    parser.add_argument('-d', '--dest', dest='dest', type=str, default=None, help='destination directory to put subdirectories and files in')
    parser.add_argument('scriptName', type=str)
    parser.add_argument('files', type=str, nargs='+')

    args = parser.parse_args()
    dest = args.dest
    if dest is None:
        dest = os.getcwd().split(os.sep)[-1]

    files = ' '.join(args.files)

    filename = args.scriptName
    with open(filename, 'w') as outfile:
        print("#!/bin/zsh\n", file=outfile)
        print(f"mvlab.py ../{dest} {files} help.txt", file=outfile)
    os.system(f"chmod 755 {filename}")

    filename = f"check{filename[2:]}"
    with open(filename, 'w') as outfile:
        print("#!/bin/zsh\n", file=outfile)
        print(f"maketest.py -a {files}", file=outfile)
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