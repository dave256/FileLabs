#!/usr/bin/env python3.6

# ----------------------------------------------------------------------
# mvlab.py
# Dave Reed
# 12/27/2017
# ----------------------------------------------------------------------

import argparse
import os.path
import glob

from findFiles import *

# ----------------------------------------------------------------------

def makeDirectoryIfDoesNotExist(s):
    if not os.path.exists(s):
        os.mkdir(s)
    else:
        if not os.path.isdir(s):
            print(f"{s} exists but is not a directory")

# ----------------------------------------------------------------------

def makeDirectoryAtDestinationIfDoesNotExist(dest, s):
    dest = os.path.expanduser(dest)
    fullPath = os.path.join(dest, s)
    makeDirectoryIfDoesNotExist(fullPath)

# ----------------------------------------------------------------------

def moveFilesFromSourceToDestination(source, destination, files, overwrite=False, dryRun=False):

    files = list(files)
    if not dryRun:
        files.extend(['messages.txt', 'grade.txt', 'grade-save.txt'])
    for f in files:
        fullSource = os.path.join(source, f)
        fullDest = os.path.join(destination, f)
        sourceExists = os.path.exists(fullSource)
        destExists = os.path.exists(fullDest)
        if sourceExists:
            if destExists and not overwrite:
                print(f'{fullDest} exists and overwrite not specified')
            else:
                os.rename(fullSource, fullDest)
        elif f not in ('messages.txt', 'grade.txt', 'grade-save.txt'):
            print(f'{fullSource} does not exist')
        

# ----------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='move files in directories of source directory to subdirectories in destination folder')
    parser.add_argument('-s', '--source', default='.', help="source directory")
    parser.add_argument('-o', '--overwrite', dest='overwrite', help='overwrite existing files')
    parser.add_argument('-d', '--dryrun', dest='dryrun', action='store_true', help='dryrun - do not rename files')
    parser.add_argument('-n', '--no-messages', dest='messages', action='store_false', help='write messages.txt with info')
    parser.add_argument('dest', type=str, metavar="destination-directory", help="destination directory to put subdirectories and files in")
    parser.add_argument('files', type=str, nargs='+')
    parser.set_defaults(dryrun=False, overwrite=False, messages=True)
    args = parser.parse_args()
    
    makeDirectoryIfDoesNotExist(args.dest)

    os.chdir(args.source)
    studentDirs = [s for s in glob.glob('*') if os.path.isdir(s)]
    for d in studentDirs:
        # first fix any naming issues
        matches, missing, extra = findFilesInDirectory(d, args.files)
        renameFiles(d, matches, missing, extra, args.dryrun, args.dryrun)
        
        # now move files
        makeDirectoryAtDestinationIfDoesNotExist(args.dest, d)
        sourceDir = os.path.join(args.source, d)
        destDir = os.path.join(args.dest, d)
        
        moveFilesFromSourceToDestination(sourceDir, destDir, args.files, args.overwrite)

# ----------------------------------------------------------------------

if __name__ == '__main__':
    main()
