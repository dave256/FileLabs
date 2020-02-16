#!/usr/bin/env python3

# ----------------------------------------------------------------------
# mvlab.py
# Dave Reed
# 12/27/2017
# ----------------------------------------------------------------------

import argparse
import os.path
import shutil
import glob

from findFiles import *

# ----------------------------------------------------------------------

def makeDirectoryIfDoesNotExist(s):

    """make directory at path s if that directory does not already exist

    :param s: directory path to create
    :return: None
    """
    if not os.path.exists(s):
        os.mkdir(s)
    else:
        if not os.path.isdir(s):
            print(f"{s} exists but is not a directory")

# ----------------------------------------------------------------------

def makeDirectoryAtDestinationIfDoesNotExist(dest, s):

    """make directory s in dest directory if does not already exist

    :param dest: the directory to make the new directory in
    :param s: the new directory to make in dest
    :return: None
    """

    dest = os.path.expanduser(dest)
    fullPath = os.path.join(dest, s)
    makeDirectoryIfDoesNotExist(fullPath)

# ----------------------------------------------------------------------

def moveFilesFromSourceToDestination(source, destination, files=None, extraFiles=None, overwrite=False):

    """move files from source directory to destination directory

    :param source: directory containing the source files
    :param destination: directory to move them the files to
    :param files: the files to move
    :param extraFiles: any extra files
    :param overwrite: if True, overwrite file in destination directory
    :param dryRun:
    :return:
    """
    
    # if default None, move all files
    if files is None:
        # get all files in directory
        files = glob.glob(f"{source}/*")
        # get just last file path
        files = [f.split("/")[-1] for f in files]
        
    if extraFiles is None:
        extraFiles = []
    files = list(files)
    files.extend(['messages.txt', 'grade.txt', 'grade-save.txt'])
    for f in files:
        fullSource = os.path.join(source, f)
        fullDest = os.path.join(destination, f)
        sourceExists = os.path.exists(fullSource)
        destExists = os.path.exists(fullDest)
        if sourceExists:
            if destExists and not overwrite:
                if f in ("grade.txt", "messages.txt", "help.txt"):
                    # combine the contents of these files if they already exist
                    tempFile = os.path.join(source, "newTempFile.txt")
                    cmd = f"cat {fullDest} {fullSource} > {tempFile}"
                    os.system(cmd)
                    os.rename(tempFile, fullDest)
                else:
                    print(f'{fullDest} exists and overwrite not specified')
            else:
                os.rename(fullSource, fullDest)
                if f not in ("grade.txt", "help.txt"):
                    shutil.copy(fullDest, f"{fullDest}-save")
        elif f not in ('messages.txt', 'grade.txt', 'grade-save.txt', 'help.txt'):
            print(f'{fullSource} does not exist')
            
    for f in extraFiles:
        fullSource = os.path.join(source, f)
        fullDest = os.path.join(destination, f)
        sourceExists = os.path.exists(fullSource)
        destExists = os.path.exists(fullDest)
        if sourceExists:
            if destExists and not overwrite:
                print(f'{fullDest} exists and overwrite not specified')
            else:
                os.rename(fullSource, fullDest)
                shutil.copy(fullDest, f"{fullDest}-save")

    # create grade.txt if does not exist
    fullGradePath = os.path.join(destination, "grade.txt")
    if not os.path.exists(fullGradePath):
        os.system(f"touch {fullGradePath}")

# ----------------------------------------------------------------------
        
def deleteIfEmpty(path):
    files = os.listdir(path)
    if not files:
        try:
            os.rmdir(path)
        except:
            pass

# ----------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='move files in directories of source directory to subdirectories in destination folder')
    parser.add_argument('-s', '--source', default='.', help='source directory')
    parser.add_argument('-o', '--overwrite', dest='overwrite', help='overwrite existing files')
    parser.add_argument('-d', '--dryrun', dest='dryrun', action='store_true', help='dryrun - do not rename files')
    parser.add_argument('-n', '--no-messages', dest='messages', action='store_false', help='write messages.txt with info')
    parser.add_argument('-r', '--rename-headers', dest='renameHeaders', action='store_true', help='rename .h to .hpp')
    parser.add_argument('dest', type=str, metavar='destination-directory', help='destination directory to put subdirectories and files in')
    parser.add_argument('files', type=str, nargs='*')
    parser.add_argument('-e', '--extra', dest='optionalFiles', type=str, nargs='+')
    parser.add_argument('-a', '--all', dest='allFiles', action='store_true', default=False)

    parser.set_defaults(dryrun=False, overwrite=False, messages=True)
    args = parser.parse_args()
    if args.allFiles:
        args.files = None
    
    if os.path.exists("Grade") and os.path.isdir("Grade"):
        os.chdir("Grade")
    
    makeDirectoryIfDoesNotExist(args.dest)

    os.chdir(args.source)
    studentDirs = [s for s in glob.glob('*') if os.path.isdir(s)]
    for d in studentDirs:
        # first if rename headers flag and not dry run, rename .h to .hpp
        if args.renameHeaders and not args.dryrun:
            files = glob.glob(f"{d}/*")
            for f in files:
                fBase, fExt = os.path.splitext(f)
                if fExt == ".h":
                    newName = ".".join((fBase, "hpp"))
                    os.rename(f, newName)
        
        # next fix any naming issues
        matches, missing, extra = findFilesInDirectory(d, args.files, True, args.optionalFiles)
        renameFiles(d, matches, missing, extra, args.messages, args.dryrun)

        if not args.dryrun:
            # now move files
            makeDirectoryAtDestinationIfDoesNotExist(args.dest, d)
            sourceDir = os.path.join(args.source, d)
            destDir = os.path.join(args.dest, d)

            moveFilesFromSourceToDestination(sourceDir, destDir, args.files, args.optionalFiles, args.overwrite)
            # if no files left in student directory, delete it
            deleteIfEmpty(d)

    # now tar up moved files
    dest = args.dest.strip()
    if dest[-1] == '/':
        dest = dest[:-1]
    head, tail = os.path.split(dest)
    os.chdir(head)
    cmd = f'tar zcf {tail}.tar.gz {tail}'
    os.system(cmd)


# ----------------------------------------------------------------------

if __name__ == '__main__':
    main()
