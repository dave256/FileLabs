#!/usr/bin/env python3

# ----------------------------------------------------------------------
# splitBySection.py
# Dave Reed
# 11/25/2019
# ----------------------------------------------------------------------

import sys
import re
import glob

from RosterInfo import *

# ----------------------------------------------------------------------

def main(argv):
    course = None
    cwd = os.getcwd()
    result = re.findall(r"CS\d\d\d", cwd)
    if len(result) == 1:
        course = result[0]
    if course is None:
        course = input("enter course (such as CS361):")
    if os.path.exists("Grade"):
        os.chdir("Grade")

    # get files with @ signs in them as should have directory of email addresses
    files = glob.glob("*@*")
    if len(files) == 0:
        print("must be in directory where Grade directory is or in the directory with email addresses as directories")
        return

    rosterInfo = RosterInfo()
    rosterInfo.readRostersFromEnvironmentVariable("ROSTERS")

    cwd = os.getcwd()

    path = os.path.normpath(cwd)
    pathList = path.split(os.sep)
    # last path component is the assignment name
    assignmentName = pathList[-1]

    # for each student directory
    for f in files:
        student = rosterInfo.findStudentByEmail(f)
        if student is not None:
            # get the student's section
            courseSection = rosterInfo.courseWithSectionForStudent(course, student)
            if courseSection is not None:
                # src is the directory named by their email address
                src = f

                # dest is two levels, which should be ~/Labs/, and then add courseSection/assignmentName
                dest = "."
                for d in ("..", "..", courseSection, assignmentName):
                    dest = os.path.join(dest, d)

                # make directory if does not exist
                if not os.path.exists(dest):
                    os.makedirs(dest)

                # add on student email address for final destination
                dest = os.path.join(dest, f)
                os.rename(src, dest)


# ----------------------------------------------------------------------

if __name__ == '__main__':
    main(sys.argv)
