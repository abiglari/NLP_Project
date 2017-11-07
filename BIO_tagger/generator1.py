import cPickle
import sys
from extractors import extractDocs, extractAnss
from tokenizers import docsPOSTagger
from featureVecGenerator import docs2WordVec
from fileReader import docFileReader

def main():
    inputFileName = sys.argv[1]
    # extracting each document as a single line without \n alongside its corresponding ID
    print "Reading the training files in data/train/texts/ folder...\n"
    docs_tr, IDs_tr = extractDocs("data/train/texts/")
    print "Reading the test file..."
    docs_tst, IDs_tst = docFileReader(inputFileName)

    # POS tagging of the words
    print "POS tagging the training data set..."
    docSentsTagWords_tr, wordSet, possWords, possPOSs = docsPOSTagger(docs_tr)
    print "POS tagging the test data set..."
    docSentsTagWords_tst = docsPOSTagger(docs_tst, False)
#    print docSentsTagWords_tr
    
    # extracting the answers as a dictionary of event roles and all incident types as labels for further event classification
    print "Reading the training file answers in data/train/answers/ folder and extracting information..."
    labels_tr, answers_tr, BTargets, ITargets, BWeapons, IWeapons = extractAnss("data/train/answers/")
#    labels_tst, answers_tst = extractAnss("data/test/answers/", False)
#    print BTargets
#    print BWeapons
#    print answers_tr
    possibleLabels = ['ARSON', 'ATTACK', 'BOMBING', 'KIDNAPPING', 'ROBBERY']
    dictLabelID = dict(zip(possibleLabels, range(len(possibleLabels))))
    print "Building word vectors of the training dataset for training an INCIDENT classifier..."
    docs2WordVec(docSentsTagWords_tr, labels_tr, dictLabelID, wordSet, 'docWordVecs_tr.txt', True)
    print "Building word vectors of the test dataset for the INCIDENT classifier in order to predict the INCIDENT labels..."
    docs2WordVec(docSentsTagWords_tst, [], dictLabelID, wordSet, 'docWordVecs_tst.txt', False)
    
    print "Saving necessary python objects for the generator2.py python script..."
    with open('fromGen1.pickle', 'w') as f:
        cPickle.dump([docSentsTagWords_tr, docSentsTagWords_tst, answers_tr, labels_tr,\
        possWords, possPOSs, possibleLabels, BTargets, ITargets, BWeapons, IWeapons, IDs_tst], f)
    f.close()
    return
if __name__ == '__main__':
    main()
