import nltk, cPickle
from Truecaser import getTrueCase

def sent_splitter(docs):
    #nltk.download()
#    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
#    fp = open("developset/texts/DEV-MUC3-0006", 'r')
#    data = fp.read()
#    print '\n-----\n'.join(tokenizer.tokenize(data))
    docSents=[]
    for doc in docs:
        sents = nltk.sent_tokenize(doc)
        docSents += [sents]
    return docSents

def docsPOSTagger(docs, isTrain=True):
    with open('distributions.obj', 'rb') as f:
        uniDist = cPickle.load(f)
        backwardBiDist = cPickle.load(f)
        forwardBiDist = cPickle.load(f)
        trigramDist = cPickle.load(f)
        wordCasingLookup = cPickle.load(f)
        f.close()
        
    docSents = sent_splitter(docs)
    docSentsTagWords=[]
    if isTrain:
        wordSet = set()
        possWords = set()
        possPOSs = set()
    for doc in docSents:
        sentsTagWords=[]
        for sent in doc:
            words = nltk.word_tokenize(sent)
            for i, w in enumerate(words):
                if isTrain and not ( len(w)<=2 and not w.isalnum()):
                    wordSet.add(w)
                words[i] = w.lower()
            truecaseWords = getTrueCase(words, 'title', wordCasingLookup, uniDist, backwardBiDist, forwardBiDist, trigramDist)
            taggedWords = nltk.pos_tag(truecaseWords)
            if isTrain:
                for tw in taggedWords:
                    possWords.add(tw[0])
                    possPOSs.add(tw[1])
            sentsTagWords += [taggedWords]
        docSentsTagWords += [sentsTagWords]
    if isTrain:
        return [docSentsTagWords,  wordSet, possWords, possPOSs]
    else:
        return docSentsTagWords
