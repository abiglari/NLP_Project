import cPickle
from featureVecGenerator import doc2FtVec, makeFeatureIdDict
from annotator import annotate
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
    tagWordsBIODict = annotate(docSentsTagWords_tr, answers_tr, roles, roleTags)
#    print tagWordsBIODict
    validFTypes = ['WORDCON','POS','POSCON','ABBR','CAP','TARGET', 'WEAPON', 'INCIDENT']

    featureIdDict = dict()
    for role, roleT in zip(roles, roleTags):
        print "Writing feature vectores of the training dataset for "+role+" BIO tagger..."
        features=dict(zip(validFTypes,[True]*len(validFTypes)))
        if role!= 'TARGET':
            features['TARGET']=False
        if role!='WEAPON':
            features['WEAPON']=False
        featureIdDict[role] = makeFeatureIdDict(features, possWords, possPOSs, possIncLabels)
        if role=='TARGET':
            doc2FtVec(tagWordsBIODict[role], features, featureIdDict[role], incLabels_tr, possIncLabels,  roleT, True, BTargets, ITargets)
            print "Writing feature vectores of the test dataset for "+role+" BIO tagger..."
            doc2FtVec(docSentsTagWords_tst, features, featureIdDict[role], predIncLs, possIncLabels, roleT, False, BTargets, ITargets)
        elif role=='WEAPON':
            doc2FtVec(tagWordsBIODict[role], features, featureIdDict[role], incLabels_tr, possIncLabels, roleT, True, BWeapons, IWeapons)
            print "Writing feature vectores of the test dataset for "+role+" BIO tagger..."
            doc2FtVec(docSentsTagWords_tst, features, featureIdDict[role], predIncLs, possIncLabels, roleT, False, BWeapons, IWeapons)
        else:
            doc2FtVec(tagWordsBIODict[role], features, featureIdDict[role], incLabels_tr, possIncLabels, roleT, True)
            print "Writing feature vectores of the test dataset for "+role+" BIO tagger..."
            doc2FtVec(docSentsTagWords_tst, features, featureIdDict[role], predIncLs, possIncLabels, roleT, False)
#    print featureIdDict

    print "Saving necessary python objects for the generator3.py python script..."
    with open('fromGen2.pickle', 'w') as f:
        cPickle.dump([roles, roleTags, IDs_tst, predIncLs, docSentsTagWords_tst], f)
    f.close()
    return
if __name__ == '__main__':
    main()
