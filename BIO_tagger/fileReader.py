def docFileReader(filePath):
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
    
def ansFileReader(filePath,  isTrain=True):
    f = open(filePath, 'rU')
    text = f.read()
    lines = text.split('\n')
    tmpDict = {}
    answers = []
    eventTypes=[]
    if isTrain:
        BTargets = set()
        ITargets = set()
        BWeapons = set()
        IWeapons = set()
    roles = ['ID', 'INCIDENT', 'WEAPON', 'PERP INDIV',  'PERP ORG', 'TARGET', 'VICTIM']
    for l in lines:
        if l:
            parts = l.split(':')
            if parts[0] in roles:
                curRole = parts[0]
                i = len(curRole)+1
                if curRole=='ID':
                    if tmpDict:
                        answers += [tmpDict]
                        tmpDict={}
                item = l[i:].lstrip()
                if curRole == 'INCIDENT':
                    eventTypes += [item]
                if item=='-':
                    tmpDict[curRole]=[]
                else:
                    if isTrain:
                        if curRole == 'WEAPON':
                            weps = item.split(' / ')
                            for wep in weps:
                                wepParts = wep.split()
                                BWeapons.add(wepParts[0])
                                for wp in wepParts[1:]:
                                    IWeapons.add(wp)
                        elif curRole == 'TARGET':
                            trgs = item.split(' / ')
                            for trg in trgs:
                                trgParts = trg.split()
                                BTargets.add(trgParts[0])
                                for tp in trgParts[1:]:
                                    ITargets.add(tp)
                    tmpDict[curRole]=[item.split(' / ')]
            else:
                item = l.lstrip()
                if isTrain:
                    if curRole == 'WEAPON':
                        weps = item.split(' / ')
                        for wep in weps:
                            wepParts = wep.split()
                            BWeapons.add(wepParts[0])
                            for wp in wepParts[1:]:
                                IWeapons.add(wp)
                    elif curRole == 'TARGET':
                        trgs = item.split(' / ')
                        for trg in trgs:
                            trgParts = trg.split()
                            BTargets.add(trgParts[0])
                            for tp in trgParts[1:]:
                                ITargets.add(tp)
                tmpDict[curRole]+=[item.split(' / ')]
    answers += [tmpDict]    
    if isTrain:
        return [answers, eventTypes, BTargets, ITargets, BWeapons, IWeapons]
    else:
        return [answers,  eventTypes]
        
def predFileReader(filePath):
    f = open(filePath, 'rU')
    text = f.read()
    labels = text.split('\n')
    return labels[:-1]
