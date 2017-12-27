import glob
import os.path

def findFilesInDirectory(directory, files, ignoreGradeTxt=True, filesToIgnore=None):
    filesInDir = [f[len(directory)+1:] for f in glob.glob(os.path.join(directory, '*'))]
    return findFilesInList(files, filesInDir, ignoreGradeTxt, filesToIgnore)
    
def findFilesInList(files, listOfFiles, ignoreGradeTxt=True, filesToIgnore=None):
    
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
    return matchDict, list(filesToMatch.keys()), list(filesInDir.keys())
    
def renameFiles(directory, matches, missing, extra, writeMessages=False, dryRun=False):

    messages = []
    if len(missing) != 0:
        missingFiles = ', '.join(missing)
        messages.append(f'missing: {missingFiles}')

    for f in matches:
        if f != matches[f]:
            messages.append(f'mv {matches[f]} {f}')
            fullSource = os.path.join(directory, matches[f])
            fullDest = os.path.join(directory, f)
            if not dryRun:
                os.rename(fullSource, fullDest)
    
    if len(messages) > 0:
        if len(extra) > 0:
            messages.append('extra: ' + ', '.join(extra))
        messages = '\n'.join(messages) + '\n'
        print(directory + '\n' + messages)
            
        if not dryRun:
            if writeMessages:
                outfile = open(os.path.join(directory, 'messages.txt'), 'w')
                outfile.write(messages)
                outfile.close()

            gradePath = os.path.join(directory, 'grade.txt')
            if os.path.exists(gradePath):
                infile = open(gradePath, 'r')
                data = infile.read()
                infile.close()
                data = 60 * '#' + '\n\n' + messages + 60 * '#' + '\n\n' + data
                outfile = open(gradePath, 'w')
                outfile.write(messages)
                outfile.close()
        
