import cPickle
import sys
from fileReader import predFileReader
from nltk.tokenize.treebank import TreebankWordDetokenizer

def main():
    inputFileName = sys.argv[1]
    inputFileName = inputFileName.split('/')
    inputFileName = inputFileName[-1]
    DT = TreebankWordDetokenizer()
    print "Loading necessary python objects from the generator2_multi.py python script..."
    with open('fromGen2.pickle') as f:
        roles, roleTags, IDs_tst, predIncLs, docSentsTagWords_tst = cPickle.load(f)
    assert(len(IDs_tst)==len(docSentsTagWords_tst) and len(IDs_tst)==len(predIncLs)),\
    'The number of extarcted IDs for the test files should be the same as the number of test documents and the number of predicted incident labels'
        
    print "Reading the predicted BIO tags..."
    predRoleIDs = predFileReader('predBIOs.txt')

    # Building a Numerical ID tag dictionary for BIO tags
    idLabelDict = {0:'O'}
    rTagRoleDict = dict(zip(roleTags, roles))
    id=1
    for t in roleTags:
        Btag = 'B-'+t
        idLabelDict[id]=Btag
        id+=1
        Itag = 'I-'+t
        idLabelDict[id]=Itag
        id+=1
        
    print "Extracting the required information of each document in the test dataset..."
    predAns = []
    predInd = 0
    for docInd, doc in enumerate(docSentsTagWords_tst):
#        thisDocDict = dict(zip(roles, [[] for i in range(len(roles))]))
        thisDocDict = dict(zip(roles, [dict() for i in range(len(roles))]))
        thisDocDict['ID'] = IDs_tst[docInd]
        thisDocDict['INCIDENT'] = predIncLs[docInd]
        for sent in doc:
            ind = predInd
            tmp = []
            currL = 'NONE'
            for wT in sent:
                word = wT[0]
                label = idLabelDict[int(predRoleIDs[ind])]
                if label[0] == 'I' and currL==label[2:]:
                    tmp+=[word]
                elif label[0] == 'B' and not tmp:
                    tmp = [word]
                    currL = label[2:]
                elif (label[0]=='B' or label[0]=='O') and tmp:
                    newEnt = DT.detokenize(tmp)
                    newEnt = newEnt.replace('[ ', '[').replace(' ]', ']').replace('( ', '(').replace(' )', ')')
                    if '[' in newEnt and ']' not in newEnt:
                       newEnt = newEnt.replace('[', '')
                    elif ']' in newEnt and '[' not in newEnt:
                        newEnt = newEnt.replace(']', '')
                    elif '(' in newEnt and ')' not in newEnt:
                       newEnt = newEnt.replace('(', '')
                    elif ')' in newEnt and '(' not in newEnt:
                        newEnt = newEnt.replace(')', '')
                    role = rTagRoleDict[currL]
                    if newEnt not in thisDocDict[role]:
#                                thisDocDict[role] += [newEnt]
                        thisDocDict[role][newEnt] = 1
                    else:
                        thisDocDict[role][newEnt] += 1
                    if label[0]=='B':
                        tmp = [word]
                        currL = label[2:]
                    else:
                        tmp = []
                        currL = 'NONE'
                ind += 1
            predInd = ind
        predAns += [thisDocDict]
    
    print "Writing the output file..."
    fOut = open(inputFileName+'.templates', 'w')
    for doc in predAns:
        #writing ID
        fOut.write('ID:             '+doc['ID']+'\n')
        
        #writing INCIDENT
        fOut.write('INCIDENT:       '+doc['INCIDENT']+'\n')
        
        #writing WEAPON, PERP INDIV, PERP ORG, TARGET, VICTIM
        notAnsList = ['THE', 'THIS', 'THAT', 'A', 'I', 'HE', 'SHE', 'THEY', 'WE', 'YOU', 'ME', 'HIM', 'HER', 'THEM', 'MY'\
        'HIS', 'HER', 'YOUR', 'THEIR', 'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE', 'TEN',\
        '1ST', '2ND', '3RD', 'MAN', 'MORE', 'MEMBER', 'MEMBER OF', 'MEMBERS OF', 'MEMBERS', 'GOVERNMENT' ]
        for role in roles:
            fOut.write(role+':')
            for i in range(16-len(role)-1):
                fOut.write(' ')
            tmpDict = dict(doc[role])
            for ent in tmpDict:
                if ent.upper() in notAnsList:
                    del doc[role][ent]
            if not doc[role]:
                fOut.write('-\n')
            else:
                ents=[]
                maxScr = max(doc[role].values())
                for ent in doc[role]:
                    if doc[role][ent]==maxScr:
                        ents+=[ent]
#                ents = doc[role]
                indEnt=0
                nEnt = len(ents)
                while (indEnt<nEnt and (ents[indEnt].upper() in notAnsList or len(ents[indEnt])<=2 )):
                    indEnt+=1
                if indEnt<nEnt:
                    fOut.write(ents[indEnt].upper()+'\n')
                else:
                    fOut.write('-\n')
                for ent in ents[indEnt+1:]:
                    if (ent.upper() not in notAnsList and len(ent)>2):
                        fOut.write('                '+ent.upper()+'\n')
        fOut.write('\n')
    fOut.close()
    
    return
if __name__ == '__main__':
    main()
