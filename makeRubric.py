#!/usr/bin/env python3

# ----------------------------------------------------------------------
# name.py
# Dave Reed
# 07/24/2020
# ----------------------------------------------------------------------

from argparse import ArgumentParser

def rubricString(withHelpDeductions: bool = False):
    if withHelpDeductions:
        helpDeductions = """1 help deduction
2 help deduction
3 help deduction
5 help deduction
10 help deduction
"""
    else:
        helpDeductions = ""
    
    rubric = f"""80 Correctness
1 other minor issue
2 other minor issue
3 other minor issue
5 other minor issue
10 other issue
{helpDeductions}
10 Organization/Style
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
2 missing your name and/or course time in comments at top of file
2 did not submit help.txt
2 file(s) not named properly
5 incorrect files submitted
3 late
5 late
10 late
20 late

"""
    return rubric

def main():
    parser = ArgumentParser(description="make rubric.txt with generic rubric")
    parser.add_argument("-d", "--help-deductions", dest="helpDeductions", action="store_true", help="add deductions for getting help from instructor")

    options = parser.parse_args()

    rubric = rubricString(options.helpDeductions)

    with open("rubric.txt", 'w') as outfile:
        print(rubric, file=outfile)
        
# ----------------------------------------------------------------------

main()