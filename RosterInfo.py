#!/usr/bin/env python3

# ----------------------------------------------------------------------
# RosterInfo.py
# Dave Reed
# 11/25/2019
# ----------------------------------------------------------------------

from __future__ import annotations

import os
import os.path
import csv

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
                nameFields = fullName.split(" ")
                if nameFields[-1].upper() in ("II", "III", "IV", "JR", "JR."):
                    del nameFields[-1]
                # handle pronouns that might be there after (
                elif len(nameFields[-1]) > 0 and nameFields[-1] == "(":
                    del nameFields[-1]
                firstName = nameFields[0]
                lastName = nameFields[-1]
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

        