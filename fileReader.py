def fileReader(filePath):
    f = open(filePath, 'rU')
    text = f.read()
    lines = text.split('\n')
    docs=[]
    tmpDoc=''
    IDs = []
    for l,lNext in zip(lines, lines[1:]):
        if l:
            if (l[0:9]=='DEV-MUC3-' or l[0:10]=='TST1-MUC3-' or l[0:10]=='TST2-MUC4-'):
                i=0
                ch = l[i]
                while (ch!=' ' and ch!='\n' and ch!='('):
                    i+=1
                    ch=l[i]
                IDs += [l[0:i]]
                if tmpDoc:
                    docs += [tmpDoc]
                    tmpDoc=''
            else:
                s=0
                nCh = len(l)
                while (s<nCh and l[s]==' ' ):
                    s+=1
                for i in range(s, nCh):
                    if (i!=nCh-1 and l[i+1]!=' ' and l[i]==' '):
                        tmpDoc += l[i]
                    elif l[i]!=' ':
                        tmpDoc += l[i]
        if lNext:
            tmpDoc+=' '
    docs+=[tmpDoc]
    return [docs, IDs]
    
