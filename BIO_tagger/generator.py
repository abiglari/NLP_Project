from os import walk
import nltk
import pickle
from fileReader import fileReader
from tokenizers import sent_splitter


def main():
    trainFiles = []
    trainDirPath = "data/train/texts/"
    for (dirpath, dirnames, filenames) in walk(trainDirPath):
        trainFiles+=filenames
        break
    docs = []
    IDs=[]
    for file in trainFiles:
        tmpDocs, tmpIDs = fileReader(trainDirPath+file)
        docs+=tmpDocs
        IDs+=tmpIDs
    docSents = sent_splitter(docs)
    docSentsTagWords=[]
    for doc in docSents:
        sentsTagWords=[]
        for sent in doc:
            words = nltk.word_tokenize(sent)
            taggedWords = nltk.pos_tag(words)
            sentsTagWords += [taggedWords]
        docSentsTagWords += [sentsTagWords]
    with open('POStags.pickle', 'w') as f:
        pickle.dump([IDs, docSentsTagWords], f)
    return
if __name__ == '__main__':
    main()
