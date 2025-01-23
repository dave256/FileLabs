#!/usr/bin/env python3

# ----------------------------------------------------------------------
# makeCPScripts.py
# Dave Reed
# 07/23/2020
# ----------------------------------------------------------------------

import argparse
import os
import os.path
import shutil

def main():
    parser = argparse.ArgumentParser(description='''create CodePost upload and download scripts;
if submitting Archive.zip, can just use makeCPScripts -a to upload all source files''')
    parser.add_argument('-l', '--labName', dest='labName', type=str, default=None,
                        help='lab name for CodePost')
    parser.add_argument('-c', '--course', dest='course', type=str, default=None,
                        help='course name for CodePost')
    parser.add_argument('-a', '--all-source-files', dest='allSource', action='store_true', default=False,)
    parser.add_argument('files', type=str, nargs='*')

    args = parser.parse_args()
    pathComponents = os.getcwd().split(os.sep)
    labName = args.labName
    if labName is None:
        labName = pathComponents[-1]
    course = args.course
    if course is None:
        for c in pathComponents:
            if c[:2] == "CS" and c[2:5].isdigit():
                course = c
                break
    if course is None:
        course = input("enter course name: ")

    # handle files from command line with / by just using last path component
    files = []
    for f in args.files:
        lastSlash = f.rfind("/")
        if lastSlash != -1:
            f = f[lastSlash + 1:]
        files.append(f)
    files = ' '.join(files)

    allFilesOption = args.allSource
    if allFilesOption:
        # if no files provided save the Archive.zip in created cleanup.zsh
        if len(files) == 0:
            files = "Archive.zip"

        cmd = f"""#!/bin/zsh

PATH=$HOME/src/FileLabs:$HOME/Scripts:/usr/local/bin:$PATH
. $HOME/Scripts/functions.zsh
# get directory of this script
SCRIPTDIR=`dirname $0:A`

cdSubDir {labName}

cpMakeAssignment.py -c {course} -p 100 {labName} $SCRIPTDIR/rubric.txt
cpUploadFilesForAssignment.py -c {course} -a {labName} --all-source-files help.txt
"""
        filename = "cpUpload.zsh"
        with open(filename, 'w') as outfile:
            print(cmd, file=outfile)
        os.system(f"chmod 755 {filename}")

        cmd = f"""#!/bin/zsh

PATH=$HOME/src/FileLabs:$HOME/Scripts:/usr/local/bin:$PATH
. $HOME/Scripts/functions.zsh
# get directory of this script
SCRIPTDIR=`dirname $0:A`

cdSubDir {labName}

cpDownloadRubricAndComments.py -c {course} -a {labName} --all-source-files
"""
        filename = "cpDownload.zsh"
        with open(filename, 'w') as outfile:
            print(cmd, file=outfile)
        os.system(f"chmod 755 {filename}")
    else:
        cmd = f"""#!/bin/zsh

PATH=$HOME/src/FileLabs:$HOME/Scripts:/usr/local/bin:$PATH
. $HOME/Scripts/functions.zsh
# get directory of this script
SCRIPTDIR=`dirname $0:A`

cdSubDir {labName}

cpMakeAssignment.py -c {course} -p 100 {labName} $SCRIPTDIR/rubric.txt
cpUploadFilesForAssignment.py -c {course} -a {labName} {files}
"""
        filename = "cpUpload.zsh"
        with open(filename, 'w') as outfile:
            print(cmd, file=outfile)
        os.system(f"chmod 755 {filename}")

        cmd = f"""#!/bin/zsh

PATH=$HOME/src/FileLabs:$HOME/Scripts:/usr/local/bin:$PATH
. $HOME/Scripts/functions.zsh
# get directory of this script
SCRIPTDIR=`dirname $0:A`

cdSubDir {labName}

cpDownloadRubricAndComments.py -c {course} -a {labName} {files}
"""
        filename = "cpDownload.zsh"
        with open(filename, 'w') as outfile:
            print(cmd, file=outfile)
        os.system(f"chmod 755 {filename}")

    cmd = f"""#!/bin/zsh

PATH=$HOME/src/FileLabs:$HOME/Scripts:/usr/local/bin:$PATH
. $HOME/Scripts/functions.zsh
# get directory of this script
SCRIPTDIR=`dirname $0:A`

cdSubDir {labName}

dirDeleteAllBut.py {files}
"""
    filename = "cleanup.zsh"
    with open(filename, 'w') as outfile:
        print(cmd, file=outfile)
    os.system(f"chmod 755 {filename}")

# ----------------------------------------------------------------------

main()