#!/usr/bin/env python3

# ----------------------------------------------------------------------
# cproster.py
# Dave Reed
# 02/14/2020
# ----------------------------------------------------------------------

import os.path
from RosterInfo import *

def main():
    rosterInfo = RosterInfo()
    # for each course specified by ROSTERS environment variable
    rosterInfo.readRostersFromEnvironmentVariable("ROSTERS")
    for course in rosterInfo.courses():
        courseName = course.name()
        # reads the CSV file specified by environment variable
        # and creates file for upload to https://codepost.io
        filename = f"{course.name()}-codepost.txt"
        fullPath = os.path.join(course.rosterDirectory(), filename)
        with open(fullPath, "w") as f:
            for student in course.students():
                # make CSV line with email,course-section
                print(f"{student.email},{courseName}", file=f)

# ----------------------------------------------------------------------

if __name__ == '__main__':
    main()

