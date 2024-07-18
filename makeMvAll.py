#!/usr/bin/env python3

# ----------------------------------------------------------------------
# makeMvAll.py
# Dave Reed
# 07/18/2024
# ----------------------------------------------------------------------

import argparse
import os
import os.path
import shutil

def main():
    parser = argparse.ArgumentParser(description='create script to mv files')
    parser.add_argument('-d', '--dest', dest='dest', type=str, default=None, help='destination directory to put subdirectories and files in')
    parser.add_argument('-s', '--script', dest='scriptName', type=str, default='mv.zsh', help='name of script to create')
    parser.add_argument('checkFiles', type=str, nargs='*')
    

    args = parser.parse_args()
    dest = args.dest
    if dest is None:
        dest = os.getcwd().split(os.sep)[-1]

    filename = args.scriptName
    # insert mv if not first two characters
    if filename[:2] != 'mv':
        filename = f"mv{filename[0].upper()}{filename[1:]}"
    
    # if filename does not end with .zsh abort
    if filename[-4:] != ".zsh":
        filename += ".zsh"

    with open(filename, 'w') as outfile:
        print("#!/bin/zsh\n", file=outfile)
        print(f"mvlab.py ../{dest} -a", file=outfile)
    os.system(f"chmod 755 {filename}")

    files = args.checkFiles
    if len(files) > 0:
        files = ' '.join(files)
        filename = f"check.zsh"
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