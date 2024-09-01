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
    
    prefixes = set()
    for course in rosterInfo.courses():
        courseName = course.name()
        prefix = courseName.split("-")[0]
        prefixes.add(prefix)
    for prefix in prefixes:
        fullPath = os.path.join(course.rosterDirectory(), f"../{prefix}-codepost.txt")
        if os.path.exists(fullPath):
            try:
                os.remove(fullPath)
            except:
                pass
    
    for course in rosterInfo.courses():
        courseName = course.name()
        prefix = courseName.split("-")[0]
        # reads the CSV file specified by environment variable
        # and creates file for upload to https://codepost.io
        filename = f"{course.name()}-codepost.txt"
        fullPath = os.path.join(course.rosterDirectory(), filename)
        with open(fullPath, "w") as f:
            for student in course.students():
                # make CSV line with email,course-section
                print(f"{student.email},{courseName}", file=f)
        
        fullPath = os.path.join(course.rosterDirectory(), f"../{prefix}-codepost.txt")
        if os.path.exists(fullPath):
            mode = "a"
        else:
            mode = "w"
        with open(fullPath, mode) as f:
            for student in course.students():
                # make CSV line with email,course-section
                print(f"{student.email},{courseName}", file=f)
        
    

# ----------------------------------------------------------------------

if __name__ == '__main__':
    main()

    