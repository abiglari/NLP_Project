import nltk

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
