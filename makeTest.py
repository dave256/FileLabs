#!/usr/bin/env python3.6

# ----------------------------------------------------------------------
# makeTest.py
# Dave Reed
# 12/28/2017
# ----------------------------------------------------------------------

import os
import shutil
import argparse
import time

def makeGradeTxt(inDirectory):
    s = f"\n{time.strftime('%m/%d/%Y %H:%M')}\n"
    outfile = open(os.path.join(inDirectory, 'grade.txt'), 'w')
    print(s, file=outfile)
    outfile.close()
    
def makeHelpTxt(inDirectory):
    s = 'no help\n'
    outfile = open(os.path.join(inDirectory, 'help.txt'), 'w')
    print(s, file=outfile)
    outfile.close()
    
def main():
    HOME = os.getenv('HOME', '/Users/dreed')
    TESTPATH = f'{HOME}/Labs/Test'
    PATH = f'{HOME}/Labs/Test/Grade/dreed@capital.edu'
    parser = argparse.ArgumentParser(description='make test directory ~/Labs/Test/Grade/dreed@capital.edu with files from command line')
    parser.add_argument('-a', '--add-help', dest='addHelp', action='store_true', help='make help.txt file')
    parser.add_argument('files', type=str, nargs='+')
    parser.set_defaults(addHelp=False)
    args = parser.parse_args()
    
    shutil.rmtree(PATH, True)
    os.makedirs(PATH)
    makeGradeTxt(PATH)
    
    for f in args.files:
        shutil.copy(f, PATH)
    
    if args.addHelp:
        makeHelpTxt(PATH)
    
    os.chdir(TESTPATH)
    os.system('tar zcvf Grade.tar.gz Grade')

# ----------------------------------------------------------------------

if __name__ == '__main__':
    main()
