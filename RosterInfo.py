#!/usr/bin/env python3

# ----------------------------------------------------------------------
# RosterInfo.py
# Dave Reed
# 11/25/2019
# ----------------------------------------------------------------------

import os
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

class RosterInfo:

    def __init__(self):

        self.lastNameToStudent = {}
        self.fullNameToStudent = {}
        self.emailToStudent = {}

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

    # ------------------------------------------------------------------

    def readRosters(self, courseAndFilenames: tuple):

        for course, filename in courseAndFilenames:
            csvReader = csv.reader(filename, delimiter=',')
            lineCount = 0
            headerDict = {}
            with open(filename) as csvFile:
                csvReader = csv.reader(csvFile, delimiter=',')
                for row in csvReader:
                    if lineCount == 0:
                        for index, value in enumerate(row):
                            headerDict[value] = index
                        for field in ("firstName", "first"):
                            try:
                                firstNameIndex = headerDict[field]
                            except:
                                pass
                        for field in ("lastName", "last"):
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
                        self._addOrUpdateStudent(firstName, lastName, email, course)

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

