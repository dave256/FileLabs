#!/usr/bin/env python3.6

# ----------------------------------------------------------------------
# findFiles.py
# Dave Reed
# 12/27/2017
# ----------------------------------------------------------------------

import glob
import os.path

# ----------------------------------------------------------------------

def findFilesInDirectory(directory, files, ignoreGradeTxt=True, filesToIgnore=None):

    """look for files in directory and return dictionary with mapping of actual filenames, missing files, and extra files

    :param directory: the directory to search for the files in
    :param files: list of files that we expect to have
    :param ignoreGradeTxt: if True, ignore files named grade.txt and grade-save.txt
    :param filesToIgnore: list of other files to ignore
     :return: three values: a dictionary with names from the files list that we found as keys mapping to the actual name of the file that we found,
    a list of the names from files that are missing,
    and a list of any extra names from listOfFiles that we did not use as dictionary values in the first return value
    """

    filesInDir = [f[len(directory)+1:] for f in glob.glob(os.path.join(directory, '*'))]
    return findFilesInList(files, filesInDir, ignoreGradeTxt, filesToIgnore)

# ----------------------------------------------------------------------

def findFilesInList(files, listOfFiles, ignoreGradeTxt=True, filesToIgnore=None):

    """look for files in listOfFiles and return dictionary with mapping of actual filenames, missing files, and extra files

    :param files: list of files that we expect to have
    :param listOfFiles: actual list of files
    :param ignoreGradeTxt: if True, ignore files named grade.txt and grade-save.txt
    :param filesToIgnore: list of other files to ignore
    :return: three values: a dictionary with names from the files list that we found as keys mapping to the actual name of the file that we found,
    a list of the names from files that are missing,
    and a list of any extra names from listOfFiles that we did not use as dictionary values in the first return value
    """

    helpMissing = False

    filesToMatch = { f : 1 for f in files }
    filesInDir = { f : 1 for f in listOfFiles }
    
    if 'messages.txt' in filesInDir:
        del filesInDir['messages.txt']
    
    if ignoreGradeTxt:
        if 'grade.txt' in filesInDir:
            del filesInDir['grade.txt']
        if 'grade-save.txt' in filesInDir:
            del filesInDir['grade-save.txt']

    if filesToIgnore is not None:
        for ignore in filesToIgnore:
            if ignore in filesInDir:
                del filesInDir[ignore]
 
    # the dictionary mapping the name of the file we expect to find to actual name of the file
    matchDict = {}
        
    # first get exact matches
    for f in list(filesToMatch.keys()):
        if f in filesInDir:
            matchDict[f] = f
            del filesToMatch[f]
            del filesInDir[f]
    
    # find any where they match except for the case
    for f in list(filesToMatch.keys()):
        for inDir in list(filesInDir.keys()):
            if f.lower() == inDir.lower():
                matchDict[f] = inDir
                del filesToMatch[f]
                del filesInDir[inDir]
                break
                
    # find any where they match except for the extension or case
    for f in list(filesToMatch.keys()):
        fBase, fExt = os.path.splitext(f)
        for inDir in list(filesInDir.keys()):
            inDirBase, inDirExt = os.path.splitext(inDir)
            if fBase.lower() == inDirBase.lower():
                matchDict[f] = inDir
                del filesToMatch[f]
                del filesInDir[inDir]
                break
    
    # try to match help.txt
    if 'help.txt' in filesToMatch:
        helpMissing = True
        for f in list(filesInDir.keys()):
            if f.lower()[:4] == 'help':
                matchDict['help.txt'] = f
                del filesInDir[f]
                helpMissing = False
                break
        del filesToMatch['help.txt']
    
    
    # if only one file left to match and only one file left in directory
    if len(filesToMatch) == 1 and len(filesInDir) == 1:
        f = list(filesToMatch.keys())[0]
        inDir = list(filesInDir.keys())[0]
        matchDict[f] = inDir
        filesToMatch = {}
        filesInDir = {}
    
    # if only one file left to match and only one file in directory with that extension (ignoring case), use it
    if len(filesToMatch) == 1:
        f = list(filesToMatch.keys())[0]
        fBase, fExt = os.path.splitext(f)
        fExt = fExt.lower()
        count = 0
        for inDir in list(filesInDir.keys()):
            inDirBase, inDirExt = os.path.splitext(inDir)
            if inDirExt.lower() == fExt:
                count += 1
                matchedFile = inDir
        if count == 1:
            matchDict[f] = matchedFile
            filesToMatch = {}
            del filesInDir[matchedFile]
    
    if helpMissing:
        filesToMatch['help.txt'] = 1

    # return the dictionary mapping the name of the file we expect to find to the actual file found,
    # the list of missing files, and the list of extra files
    return matchDict, list(filesToMatch.keys()), list(filesInDir.keys())

# ----------------------------------------------------------------------

def renameFiles(directory, matches, missing, extra, writeMessages=False, dryRun=False):

    """rename files to match their expected names using output from findFilesInList

    :param directory: the path to the directory with the files
    :param matches: dictionary mapping expected names to actual names (the first return value from the call findFilesInList)
    :param missing: list of missing files (the second return value from the call findFilesInList)
    :param extra:  any extra files in the directory (the third retun value from the call findFilesInList)
    :param writeMessages: put files we renamed, missing, and extra files in messages.txt
    :param dryRun: if True, don't actually rename files, just print out messages for what needs renamed, is missing, and extra files
    :return: None
    """

    # list of strings with messages for incorrect files
    messages = []
    if len(missing) != 0:
        # each missing file
        missingFiles = ', '.join(missing)
        messages.append(f'missing: {missingFiles}')

    for f in matches:
        if f != matches[f]:
            # each file that will need renamed based on our matching algorithm from findFilesInList
            messages.append(f'mv {matches[f]} {f}')
            fullSource = os.path.join(directory, matches[f])
            fullDest = os.path.join(directory, f)
            # if not a dry run, rename the file
            if not dryRun:
                os.rename(fullSource, fullDest)
    
    if len(messages) > 0:
        # if we are missing some files, also indicate which files are extra
        if len(extra) > 0:
            messages.append('extra: ' + ', '.join(extra))
        # make string out of messages and output it
        messages = '\n'.join(messages) + '\n'
        print(directory + '\n' + messages)

        # if not a dry run and writeMessages, create the messages.txt file
        if not dryRun and writeMessages:
            outfile = open(os.path.join(directory, 'messages.txt'), 'w')
            outfile.write(messages)
            outfile.close()

# ----------------------------------------------------------------------
