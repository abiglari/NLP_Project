from os import walk
from fileReader import docFileReader, ansFileReader

def extractDocs(directoryPath):
    # extracting the name of all the training file documents
    docFiles = []
    for (dirpath, dirnames, filenames) in walk(directoryPath):
        docFiles+=filenames
        break
    docFiles.sort()
    # extracting documents in all of the files with their IDs       
    docs = []
    IDs=[]
    for file in docFiles:
        tmpDocs, tmpIDs = docFileReader(directoryPath+file)
        docs+=tmpDocs
        IDs+=tmpIDs
    return [docs, IDs]
    
def extractAnss(directoryPath,  isTrain=True):
    # extracting the name of all the training file answer sheets
    ansFiles = []
    for (dirpath, dirnames, filenames) in walk(directoryPath):
        ansFiles+=filenames
        break
    ansFiles.sort()
    # extracting answers in all of the answer files
    answers = []
    labels = []
    if isTrain:
        BWeapons = set()
        IWeapons = set()
        BTargets = set()
        ITargets = set()
    for file in ansFiles:
        if isTrain:
            tmpAns, ls, bts, its, bws, iws = ansFileReader(directoryPath+file, isTrain)
            BWeapons.update(bws)
            IWeapons.update(iws)
            BTargets.update(bts)
            ITargets.update(its)
        else:
            tmpAns,  ls = ansFileReader(directoryPath+file, isTrain)            
        answers+=tmpAns
        labels += ls
    if isTrain:
        return [labels, answers, BTargets, ITargets, BWeapons, IWeapons]
    else:
        return [labels, answers]
