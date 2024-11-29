#!/usr/bin/env python3

# ----------------------------------------------------------------------
# makeCreateScripts.py
# Dave Reed
# 07/18/2024
# ----------------------------------------------------------------------

import argparse
import os
import os.path
import sys

def main():
    parser = argparse.ArgumentParser(description="""makes various grading scripts
        example usage:
 makeCreateScripts.py -f ../../BlackjackCards/Sources/BlackjackCards/BlackjackHand.swift ../../BlackjackCards/Tests/BlackjackCardsTests/BlackjackHandXCTests.swift --copy /Users/dreed/Capital/CS261/gitsrc/BlackjackCards/Sources/BlackjackCards/
    """)

    parser.add_argument('-m', '--mv', dest='mv', type=str, default='mv.zsh', help='name of mv.zsh script')
    parser.add_argument('--copy', dest='copyDest', type=str, default=None, help='destination directory for copy.zsh script')
    parser.add_argument('-f', nargs='+', dest='files', help='files to find and move')
    parser.add_argument('-c', nargs='*', dest='checkFiles', help='files for check.zsh to use')
    args = parser.parse_args()

    files = ' '.join(args.files)
    checkFiles = args.checkFiles
    if checkFiles is None or len(checkFiles) == 0:
        checkFiles = files
    else:
        checkFiles = ' '.join(args.checkFiles)

    with open("createScripts.zsh", "w") as outfile:
        print("#!/bin/zsh", file=outfile)
        print(file=outfile)
        cmd = os.path.basename(sys.argv[0])
        print(f'# {cmd} {" ".join(sys.argv[1:])}', file=outfile)
        print(file=outfile)

        mvLine = f'makeMvLab.py {args.mv} -f {files} -c {checkFiles}'
        print(mvLine, file=outfile)
        if args.copyDest is not None:
            copyLine = f'makeCopyRunZsh.py -d {args.copyDest} {files}'
            print(copyLine, file=outfile)
        print(f'makeCPScripts.py {files}', file=outfile)

    os.system("chmod 755 createScripts.zsh")

# ----------------------------------------------------------------------


if __name__ == "__main__":
    main()
    