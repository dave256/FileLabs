#!/usr/bin/env python3

# ----------------------------------------------------------------------
# extractLabs.py
# Dave Reed
# 11/25/2019
# ----------------------------------------------------------------------

from __future__ import annotations

import sys
import csv
import os
import os.path
import shutil
import glob
import zipfile

class Student:

    def __init__(self, firstName, lastName, email):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.courses = []

    # ------------------------------------------------------------------

    def addCourse(self, course):
        self.courses.append(course)

    # ------------------------------------------------------------------

    def __str__(self):
        return f"{self.firstName} {self.lastName} {self.email} {str(self.courses)}"


# ----------------------------------------------------------------------

class Course:

    def __init__(self, courseWithSection, rosterFileName):
        self._name = courseWithSection
        self._rosterFilename = rosterFileName
        self._students = []

    def filename(self):
        return self._rosterFilename

    def rosterDirectory(self):
        return os.path.dirname(self._rosterFilename)

    def name(self):
        return self._name

    def addStudent(self, s):
        self._students.append(s)

    def students(self):
        return self._students

    def __str__(self):
        return self._name

    def __lt__(self, other: Course):
        return self._name < other._name


# ----------------------------------------------------------------------

class RosterInfo:

    def __init__(self):

        self.lastNameToStudent = {}
        self.fullNameToStudent = {}
        self.emailToStudent = {}
        self._courses = []

    # ------------------------------------------------------------------

    def courses(self):
        return self._courses

    # ------------------------------------------------------------------

    def findStudentByName(self, fullName):
        if fullName in self.fullNameToStudent:
            return self.fullNameToStudent[fullName]
        else:
            if self.lastNameToStudent is not None:
                firstName, lastName = fullName.split(" ")
                if lastName in self.lastNameToStudent:
                    return self.lastNameToStudent[lastName]

    # ------------------------------------------------------------------

    def courseWithName(self, name):
        for c in self._courses:
            if c.name() == name:
                return c
        return None

    # ------------------------------------------------------------------

    def findStudentByEmail(self, email):
        return self.emailToStudent[email]

    # ------------------------------------------------------------------

    def courseWithSectionForStudent(self, coursePrefix, student):
        for course in student.courses:
            if course.startswith(coursePrefix):
                return course

    # ------------------------------------------------------------------

    def _addOrUpdateStudent(self, firstName, lastName, email, course):
        fullName = f"{firstName} {lastName}"
        if email in self.emailToStudent:
            s = self.emailToStudent[email]
        elif fullName in self.fullNameToStudent:
            s = self.fullNameToStudent[fullName]
        else:
            s = Student(firstName, lastName, email)
            self.fullNameToStudent[fullName] = s
            self.emailToStudent[email] = s
            # support looking up by last name for last names that do not duplicate
            if lastName not in self.lastNameToStudent:
                self.lastNameToStudent[lastName] = s
            else:
                del self.lastNameToStudent[lastName]

        s.addCourse(course)
        return s

    # ------------------------------------------------------------------

    def courseAndFilenames():
        return self._courseAndFilenames

    # ------------------------------------------------------------------

    def readRosters(self, courseAndFilenames: tuple):
        self._courseAndFilenames = courseAndFilenames
        for course, filename in courseAndFilenames:
            courseObject = Course(course, filename)
            self._courses.append(courseObject)
            csvReader = csv.reader(filename, delimiter=',')
            lineCount = 0
            headerDict = {}
            with open(filename) as csvFile:
                csvReader = csv.reader(csvFile, delimiter=',')
                for row in csvReader:
                    if lineCount == 0:
                        for index, value in enumerate(row):
                            headerDict[value] = index
                        for field in ("firstName", "first", "First"):
                            try:
                                firstNameIndex = headerDict[field]
                            except:
                                pass
                        for field in ("lastName", "last", "Last"):
                            try:
                                lastNameIndex = headerDict[field]
                            except:
                                pass
                        for field in ("primaryEmail", "Email", "email1"):
                            try:
                                emailIndex = headerDict[field]
                            except:
                                pass
                    else:
                        firstName = row[firstNameIndex]
                        lastName = row[lastNameIndex]
                        email = row[emailIndex]
                        s = self._addOrUpdateStudent(firstName, lastName, email, course)
                        courseObject.addStudent(s)

                    lineCount += 1

    # ------------------------------------------------------------------

    def readRostersFromEnvironmentVariable(self, envVar):
        try:
            info = os.getenv(envVar)
        except:
            print(f"{envVar} environment variable not set")
            return

        info = info.split(":")

        # turn environment variable that has courseName:pathToRosterFile:courseName:pathToRosterFile
        # into ((courseName, pathToRosterFile), (courseName, pathToRosterFile))
        courseAndFilenames = tuple(zip(*(iter(info),) * 2))
        self.readRosters(courseAndFilenames)

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
    # move into $HOME/Homework/<CourseName>/Grade
    home = os.getenv("HOME")
    src = os.path.split(directory)[1]
    dest = os.path.join(home, "Homework")
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

    # need to edit this so it is for your classes and has path to roster files from iLearn
    os.environ["COURSE_ROSTERS"] = "CS161-12:/Users/dreed/Private/Grades/Spring2021/CS161-12/roster.csv:CS161-1:/Users/dreed/Private/Grades/Spring2021/CS161-1/roster.csv:CS381-9:/Users/dreed/Private/Grades/Spring2021/CS381-9/roster.csv:CS381-2:/Users/dreed/Private/Grades/Spring2021/CS381-2/roster.csv:CS410:/Users/dreed/Private/Grades/Spring2021/CS410/roster.csv"

    # read rosters based on environment variable
    rosterInfo = RosterInfo()
    rosterInfo.readRostersFromEnvironmentVariable("COURSE_ROSTERS")

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
    