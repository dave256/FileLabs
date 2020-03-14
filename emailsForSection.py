#!/usr/bin/env python3

# ----------------------------------------------------------------------
# emailsForSection.py
# Dave Reed
# 03/14/2020
# ----------------------------------------------------------------------

import argparse
import re
import glob

from RosterInfo import *

# ----------------------------------------------------------------------

def main():

    parser = argparse.ArgumentParser(description='split student directories by section')
    parser.add_argument('-c', '--course-name', dest='course', default=None, help='name of course/section for which to list email addresses')

    parser.add_argument('sections', type=str, nargs='*', help="an even number of values that has the directoryNameForSection fileWithSectionEmailAddresses for each section")
    parser.set_defaults(dryrun=False, messages=True)
    args = parser.parse_args()

    rosterInfo = RosterInfo()
    if len(args.sections) == 0:
        rosterInfo.readRostersFromEnvironmentVariable("ROSTERS")
    elif len(args.sections) % 2 != 0:
        print("must have an even number of values")
    else:
        courseAndFilenames = tuple(zip(*(iter(args.sections),) * 2))
        rosterInfo.readRosters(courseAndFilenames)


    course = rosterInfo.courseWithName(args.course)
    for s in course.students():
        print(s.email)

    return

# ----------------------------------------------------------------------

if __name__ == '__main__':
    main()
