import cPickle
import sys
from fileReader import predFileReader
from nltk.tokenize.treebank import TreebankWordDetokenizer

def main():
    inputFileName = sys.argv[1]
    inputFileName = inputFileName.split('/')
    inputFileName = inputFileName[-1]
    DT = TreebankWordDetokenizer()
    print "Loading necessary python objects from the generator2.py python script..."
    with open('fromGen2.pickle') as f:
        roles, roleTags, IDs_tst, predIncLs, docSentsTagWords_tst = cPickle.load(f)
    assert(len(IDs_tst)==len(docSentsTagWords_tst) and len(IDs_tst)==len(predIncLs)),\
    'The number of extarcted IDs for the test files should be the same as the number of test documents and the number of predicted incident labels'
        
    predRoleIDs = dict()
    for rT, role in zip(roleTags, roles):
        print "Reading the predicted BIO tags for the "+role+" role..."
        predRoleIDs[role] = predFileReader('pred'+rT+'s.txt')

    print "Extracting the required information of each document in the test dataset..."
    predAns = []
    predInd = 0
    for docInd, doc in enumerate(docSentsTagWords_tst):
#        thisDocDict = dict(zip(roles, [[] for i in range(len(roles))]))
        thisDocDict = dict(zip(roles, [dict() for i in range(len(roles))]))
        thisDocDict['ID'] = IDs_tst[docInd]
        thisDocDict['INCIDENT'] = predIncLs[docInd]
        for sent in doc:
            for role in roles:
                ind = predInd
                tmp = []
                for wT in sent:
                    word = wT[0]
                    if predRoleIDs[role][ind] == '2':
                        if tmp:
                            tmp+=[word]
                    elif predRoleIDs[role][ind] == '1':
                        if not tmp:
                            tmp += [word]
                        else:
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
                            if newEnt not in thisDocDict[role]:
#                                thisDocDict[role] += [newEnt]
                                thisDocDict[role][newEnt] = 1
                            else:
                                thisDocDict[role][newEnt] += 1
                            tmp = [word]
                    else:
                        if tmp:
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
                            if newEnt not in thisDocDict[role]:
#                                thisDocDict[role] += [newEnt]
                                thisDocDict[role][newEnt] = 1
                            else:
                                thisDocDict[role][newEnt] += 1
                            tmp = []
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
