#!/usr/bin/env python3

# ----------------------------------------------------------------------
# studentCounts.py
# Dave Reed
# 09/01/2020
# ----------------------------------------------------------------------

import argparse
import re
import glob

from RosterInfo import *

# ----------------------------------------------------------------------

def main():

    parser = argparse.ArgumentParser(description='count of students in sections')
    parser.add_argument('sections', type=str, nargs='*', help="an even number of values that has the directoryNameForSection fileWithSectionEmailAddresses for each section")
    args = parser.parse_args()

    rosterInfo = RosterInfo()
    if len(args.sections) == 0:
        rosterInfo.readRostersFromEnvironmentVariable("ROSTERS")
    elif len(args.sections) % 2 != 0:
        print("must have an even number of values")
    else:
        courseAndFilenames = tuple(zip(*(iter(args.sections),) * 2))
        rosterInfo.readRosters(courseAndFilenames)

    courses = rosterInfo.courses()
    courses.sort()
    for c in courses:
        students = c.students()
        print(f"{str(c):15} {len(students):2}")

    return

# ----------------------------------------------------------------------

if __name__ == '__main__':
    main()
