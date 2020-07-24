#!/usr/bin/env python3

# ----------------------------------------------------------------------
# name.py
# Dave Reed
# 07/24/2020
# ----------------------------------------------------------------------

def main():
    rubric = """75 Correctness
3 other issue
5 other minor issue
10 other issue

15 Organization/Style
0 other style issue
2 other style issue
2 use descriptive variable names
5 use descriptive variable names
2 follow naming conventions (camelCase for variables/functions, CamelCase for classes)
2 spacing between sections of code and functions
2 extra unnecessary code
5 code not organized into functions/methods

10 Comments
1 needs comments
3 needs comments
5 needs comments
10 code has no comments

-5 Bonus
-5 did bonus

30 Deductions
2 missing your name at top of file
2 did not submit help.txt
5 late
10 late
20 late
"""

    with open("rubric.txt", 'w') as outfile:
        print(rubric, file=outfile)
# ----------------------------------------------------------------------

main()