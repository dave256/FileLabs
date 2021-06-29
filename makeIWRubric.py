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
    
    rubric = f"""100 Correctness
1 minor issue
3 minor issue
5 issue
10 significant issue
20 multiple major issues
25 multiple major issues
33 multiple major issues
40 multiple major issues
50 multiple major issues
25 no code or file not submitted
33 no code file not submitted
50 no code or file not submitted

30 Deductions
2 file(s) not named properly
5 incorrect files submitted
5 late
10 late
20 late

"""
    return rubric

def main():
    parser = ArgumentParser(description="make rubric.txt with generic rubric")

    options = parser.parse_args()

    rubric = rubricString()

    with open("rubric.txt", 'w') as outfile:
        print(rubric, file=outfile)
        
# ----------------------------------------------------------------------

main()