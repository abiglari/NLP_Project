import cPickle
from featureVecGenerator import doc2FtVec_multi, makeFeatureIdDict
from annotator import annotate_all
from fileReader import predFileReader

def main():
    print "Loading necessary python objects from the generator1.py python script..."
    with open('fromGen1.pickle') as f:
        docSentsTagWords_tr, docSentsTagWords_tst, answers_tr, incLabels_tr,\
        possWords, possPOSs, possIncLabels, BTargets, ITargets, BWeapons, IWeapons, IDs_tst = cPickle.load(f)
        
    print "Reading predicted labels for the test dataset..."
    predIncLIDs = predFileReader('predIncidents.txt')
    dictIdLabel = dict(zip(range(len(possIncLabels)), possIncLabels))
    predIncLs = []
    for pLId in predIncLIDs:
        predIncLs += [dictIdLabel[int(pLId)]]

    print "Annotating the training dataset and making it ready for feature extraction..."
    roles = ['WEAPON', 'PERP INDIV', 'PERP ORG', 'TARGET', 'VICTIM']
    roleTags = ['W', 'PI', 'PO', 'T', 'V']    
    tagWordsBIO = annotate_all(docSentsTagWords_tr, answers_tr, roles, roleTags)
#    print tagWordsBIODict

    validFTypes = ['WORDCON','POS','POSCON','ABBR','CAP','TARGET', 'WEAPON', 'INCIDENT']

    featureIdDict = dict()
    print "Writing feature vectores of the training dataset for the multiclass BIO tagger..."
    features=dict(zip(validFTypes,[True]*len(validFTypes)))
    featureIdDict = makeFeatureIdDict(features, possWords, possPOSs, possIncLabels)
    doc2FtVec_multi(tagWordsBIO, features, featureIdDict, incLabels_tr, possIncLabels, roleTags, True, BTargets, ITargets, BWeapons, IWeapons)
    doc2FtVec_multi(docSentsTagWords_tst, features, featureIdDict, predIncLs, possIncLabels, roleTags, False, BTargets, ITargets, BWeapons, IWeapons)

#    print featureIdDict

    print "Saving necessary python objects for the generator3.py python script..."
    with open('fromGen2.pickle', 'w') as f:
        cPickle.dump([roles, roleTags, IDs_tst, predIncLs, docSentsTagWords_tst], f)
    f.close()
    return
if __name__ == '__main__':
    main()
