import numpy

def docs2WordVec(docSentsTagWords, labels, dictLabelID, words,  outFileName, isTrain=True):
    if isTrain:
        assert(len(labels)==len(docSentsTagWords)), 'the number of lables and documents should be equal'
    nWords = len(words)
    nDocs = len(docSentsTagWords)
    dictWordID = dict(zip(words, [i for i in range(1, nWords+1)]))
    dictWordID['UNK']=nWords+1
    f = open(outFileName, 'w')
    for i in range(nDocs):
        doc = docSentsTagWords[i]
        if isTrain:
            l=labels[i]
        docWordCount= {}
        for sent in doc:
            for wtag in sent:
                w = wtag[0].upper()
                if not (len(w)<=2 and not w.isalnum()):
                    if w not in words:
                        if dictWordID['UNK'] in docWordCount.keys():
                            docWordCount[dictWordID['UNK']]+=1
                        else:
                            docWordCount[dictWordID['UNK']]=1
                    else:
                        if dictWordID[w] in docWordCount.keys():
                            docWordCount[dictWordID[w]]+=1
                        else:
                            docWordCount[dictWordID[w]]=1
        if isTrain:
            f.write(str(dictLabelID[l]))
        else:
            f.write('0')
        sortedIDs= sorted(docWordCount)
        for id in sortedIDs:
            f.write(' '+str(id)+':'+str(docWordCount[id]))
        if i!= nDocs-1:
            f.write('\n')
    return 
    
def makeFeatureIdDict(features, words, POSs, incidents):
    featureIdDict={}
    nextFId = 1
    if features['WORDCON']:
        featureIdDict['prev-word-PHI']=nextFId
        nextFId+=1
        featureIdDict['next-word-OMEGA']=nextFId
        nextFId+=1
    for word in words:
        featureIdDict['word-'+word]=nextFId
        nextFId+=1
        if features['WORDCON']:
            featureIdDict['prev-word-'+word]=nextFId
            nextFId+=1
            featureIdDict['next-word-'+word]=nextFId
            nextFId+=1
    featureIdDict['word-UNK']=nextFId
    nextFId+=1
    if features['WORDCON']:
        featureIdDict['prev-word-UNK']=nextFId
        nextFId+=1
        featureIdDict['next-word-UNK']=nextFId
        nextFId+=1
    if features['POSCON']:
        featureIdDict['prev-pos-PHIPOS']=nextFId
        nextFId+=1
        featureIdDict['next-pos-OMEGAPOS']=nextFId
        nextFId+=1
    for pos in POSs:
        if features['POS']:
            featureIdDict['pos-'+pos]=nextFId
            nextFId+=1
        if features['POSCON']:
            featureIdDict['prev-pos-'+pos]=nextFId
            nextFId+=1
            featureIdDict['next-pos-'+pos]=nextFId
            nextFId+=1
    if features['POS']:
        featureIdDict['pos-UNKPOS']=nextFId
        nextFId+=1
    if features['POSCON']:
        featureIdDict['prev-pos-UNKPOS']=nextFId
        nextFId+=1
        featureIdDict['next-pos-UNKPOS']=nextFId
        nextFId+=1
    if features['INCIDENT']:
        for inc in incidents:
            featureIdDict['incident-'+inc]=nextFId
            nextFId+=1            
    if features['ABBR']:
        featureIdDict['abbreviation']=nextFId
        nextFId+=1
    if features['CAP']:
        featureIdDict['capitalized']=nextFId
        nextFId+=1
    if features['TARGET']:
        featureIdDict['is-B-T']=nextFId
        nextFId+=1
        featureIdDict['is-I-T']=nextFId
        nextFId+=1   
    if features['WEAPON']:
        featureIdDict['is-B-W']=nextFId
        nextFId+=1
        featureIdDict['is-I-W']=nextFId
        nextFId+=1
    return featureIdDict        
        
def doc2FtVec(tagWordsBIODict, features, featureIdDict, incLs,  possIncLs, roleT, isTrain=True, BParts=[], IParts=[]):

    if isTrain:
        fOut = open(roleT+"_BIO_vectors_tr.txt","w")
    else:
        fOut = open(roleT+"_BIO_vectors_tst.txt","w")
    Btag = 'B-'+roleT
    Itag = 'I-'+roleT
    labelIdDict = {'O':0,Btag:1,Itag:2}
    
    nDocs = len(tagWordsBIODict)
    if isTrain:
        vecs = []
        nonNegVecs = []
    for docInd, doc in enumerate(tagWordsBIODict):
        nSents = len(doc)
        for sentInd, sent in enumerate(doc):
            nWords = len(sent)
            for i, wPOSLab in enumerate(sent):
                if isTrain:
                    isNonNeg = False
                    tmpVec = []
                    labels = wPOSLab[2]
#                    fOut.write(str(labelIdDict[labels[0]]))
                    tmpVec += [labelIdDict[labels[0]]]
                    if labels[0]!='O':
                        isNonNeg = True
                else:
                    fOut.write('0')
                pos  = wPOSLab[1]
                word = wPOSLab[0]
                
                idList=[]
                #WORD
                ft = 'word-'+word
                if ft in featureIdDict:
                    idList += [featureIdDict[ft]]
                else:
                    idList += [featureIdDict['word-UNK']]
                #WORDCON
                if features['WORDCON']:
                    if i==0:
                        idList += [featureIdDict['prev-word-PHI']]
                    else:
                        ft = 'prev-word-'+sent[i-1][0]
                        if ft in featureIdDict:
                            idList += [featureIdDict[ft]]
                        else:
                            idList += [featureIdDict['prev-word-UNK']]
                    if i==nWords-1:
                         idList += [featureIdDict['next-word-OMEGA']]
                    else:
                        ft = 'next-word-'+sent[i+1][0]
                        if ft in featureIdDict:
                            idList += [featureIdDict[ft]]
                        else:
                             idList += [featureIdDict['next-word-UNK']]
                #POS
                if features['POS']:
                    ft = 'pos-'+pos
                    if ft in featureIdDict:
                        idList += [featureIdDict[ft]]
                    else:
                        idList += [featureIdDict['pos-UNKPOS']]
                #POSCON
                if features['POSCON']:
                    if i==0:
                        idList += [featureIdDict['prev-pos-PHIPOS']]
                    else:
                        ft = 'prev-pos-'+sent[i-1][1]
                        if ft in featureIdDict:
                            idList += [featureIdDict[ft]]
                        else:
                            idList += [featureIdDict['prev-pos-UNKPOS']]
                    if i==nWords-1:
                        idList += [featureIdDict['next-pos-OMEGAPOS']]
                    else:
                        ft = 'next-pos-'+sent[i+1][1]
                        if ft in featureIdDict:
                            idList += [featureIdDict[ft]]
                        else:
                            idList += [featureIdDict['next-pos-UNKPOS']]
                #ABBR
                if features['ABBR']:
                    if word.replace('.','').isalpha() and word.upper()==word and len(word)<=4:
                        idList += [featureIdDict['abbreviation']]
                #CAP
                if features['CAP']:
                    if word[0].isalpha() and word[0]==word[0].upper():
                        idList += [featureIdDict['capitalized']]
                #TARGET
                if features['TARGET']:
                    if word in BParts:
                        idList += [featureIdDict['is-B-T']]
                    if word in IParts:
                        idList += [featureIdDict['is-I-T']]
                #WEAPON
                if features['WEAPON']:
                    if word in BParts:
                        idList += [featureIdDict['is-B-W']]
                    if word in IParts:
                        idList += [featureIdDict['is-I-W']]
                #INCIDENT
                if features['INCIDENT']:
                    idList += [featureIdDict['incident-'+incLs[docInd]]]
                 
                if isTrain:
                    tmpVec += sorted(idList)
                    vecs += [tmpVec]
                    if isNonNeg:
                        nonNegVecs += [tmpVec]
                else:
                    for id in sorted(idList):
                        fOut.write(' '+str(id)+':1')
                if isTrain and len(labels)>1:
                    for l in labels[1:]:
                        tmpVec = [labelIdDict[l]]
                        tmpVec += sorted(idList)
                        vecs += [tmpVec]
                        nonNegVecs += [tmpVec]
#                        fOut.write('\n'+str(labelIdDict[l]))
#                        for id in sorted(idList):
#                            fOut.write(' '+str(id)+':1')
                elif not isTrain:
                    isLastLine = (docInd==nDocs-1 and sentInd==nSents-1 and i==nWords-1)
                    if not isLastLine:
                        fOut.write('\n')

    if isTrain:
        nIns = len(vecs)
        nNonNeg = len(nonNegVecs)
        nShort = max(0, nIns - 2* nNonNeg)
        if nNonNeg!=0:
            for i in range(nShort):
                vecs+= [nonNegVecs[i%nNonNeg]]
        nIns = len(vecs)
        inds = numpy.random.permutation(nIns)
        for ind, i in enumerate(inds):
            vec = vecs[i]
            fOut.write(str(vec[0]))
            for id in vec[1:]:
                fOut.write(' '+str(id)+':1')
            if ind!= nIns-1:
                fOut.write('\n')
    fOut.close()    
    return
