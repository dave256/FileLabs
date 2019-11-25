#!/usr/bin/env python3

# ----------------------------------------------------------------------
# extractLabs.py
# Dave Reed
# 11/25/2019
# ----------------------------------------------------------------------

import sys
import csv
import os
import shutil
import glob
import zipfile
from RosterInfo import *

# ----------------------------------------------------------------------

def extractAndRename(course, directory, rosterInfo):
    # cd into directory with folders named by student's full name
    os.chdir(directory)
    studentDirectories = glob.glob("*")
    for d in studentDirectories:
        # iLearn seems to name by "firstName LastName_extraStuff
        # so get their full name
        fullName = d.split("_")[0]
        # attempt to find student
        s = rosterInfo.findStudentByName(fullName)
        # remove existing path with student email
        if os.path.exists(s.email):
            shutil.rmtree(s.email)
        # rename directory from their name with extraStuff to just email address
        os.rename(d, s.email)

    # move up one directory
    os.chdir("..")
    # move into $HOME/Labs/<CourseName>/Grade
    home = os.getenv("HOME")
    src = os.path.split(directory)[1]
    dest = os.path.join(home, "Labs")
    dest = os.path.join(dest, course)
    destGrade = os.path.join(dest, "Grade")
    # delete Grade directory if exists
    if os.path.exists(destGrade):
        shutil.rmtree(destGrade, True)
    # make paths up to but not including Grade directory if does not exist
    if not os.path.exists(dest):
        os.makedirs(dest)
    os.rename(src, destGrade)

# ----------------------------------------------------------------------

def main(argv):


    if len(argv) < 2:
        filePath = input("enter zip filename: ")
    else:
        filePath = argv[1]

    lastPath = os.path.split(filePath)[1]
    fileFields = lastPath.split("-")
    # zip filename contains course name such as CS-361-01
    # get course name without section
    course = f"{fileFields[0]}{fileFields[1]}"

    # read rosters based on environment variable
    rosterInfo = RosterInfo()
    rosterInfo.readRostersFromEnvironmentVariable("ROSTERS")

    # remove .zip extension
    directory = filePath[:-4]
    # delete directory with that name if already exists
    shutil.rmtree(directory, True)

    #unzip
    with zipfile.ZipFile(filePath, 'r') as zipRef:
        zipRef.extractall(directory)

    # move
    extractAndRename(course, directory, rosterInfo)

# ----------------------------------------------------------------------

if __name__ == '__main__':
    main(sys.argv)
