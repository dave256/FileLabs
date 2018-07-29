#!/usr/bin/env python3

# ----------------------------------------------------------------------
# missing.py
# Dave Reed
# 12/27/2017
# ----------------------------------------------------------------------

import sys, os, glob
import argparse

from findFiles import *

# ----------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='check for missing files in directories')
    parser.add_argument('-d', '--dryrun', dest='dryrun', action='store_true', help='dryrun - do not rename files')
    parser.add_argument('-n', '--no-messages', dest='messages', action='store_false', help='write messages.txt with info')
    parser.add_argument('files', type=str, nargs='+')
    parser.set_defaults(dryrun=False, messages=True)
    args = parser.parse_args()

    dirs = glob.glob('*')
    for d in dirs:
        if os.path.isdir(d):
            matches, missing, extra = findFilesInDirectory(d, args.files)
            renameFiles(d, matches, missing, extra, args.messages, args.dryrun)

# ----------------------------------------------------------------------

if __name__ == '__main__':
    main()
