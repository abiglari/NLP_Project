import nltk

def annotate(docSentsTagWords, answers, roles, roleTags):
    tagWordsBIODict = dict()
    for role in roles:
        tagWordsBIODict[role] = []
    for doc, ansDict in zip(docSentsTagWords, answers):
        for role, roleT in zip(roles, roleTags):
            roleItems = ansDict[role]
            BIOdoc=[]
            for sent in doc:
                BIOsent = []
                nWords = len(sent)
                BIOtags = [[] for w in range(nWords)]
                for i, wordT in enumerate(sent):
                    word=wordT[0].upper()
                    if not BIOtags[i]:
                        for its in roleItems:
                            for item in its:
                                itemParts =  nltk.word_tokenize(item)
                                matched = True
                                if word==itemParts[0]:
                                    ind = 1
                                    j=i + ind
                                    nParts = len(itemParts)
                                    while (j<nWords and ind<nParts):
                                        if (sent[j][0].upper()!=itemParts[ind]):
                                            matched = False
                                        j+=1
                                        ind+=1
                                else:
                                    matched = False
                                if matched == True:
                                    if 'B-'+roleT not in BIOtags[i]:
                                        BIOtags[i]+=['B-'+roleT]
                                    for j in range(i+1, i+ind):
                                        if 'I-'+roleT not in BIOtags[j]:
                                            BIOtags[j]+=['I-'+roleT]
                    if not BIOtags[i]:
                        BIOtags[i]+=['O']
                    BIOsent += [wordT]
                    BIOsent[i] += (BIOtags[i], )
#                for i in range(nWords):
#                    BIOsent[i] += (BIOtags[i], )
                BIOdoc += [BIOsent]
            tagWordsBIODict[role] += [BIOdoc]
    return tagWordsBIODict
