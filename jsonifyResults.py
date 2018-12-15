import json
import csv

def generateList(inputFile):
    res = []
    for line in inputFile.readlines():
        # line = line.decode('utf8')
        t, s, p = line.strip(' \n').split()
        res.append((s, t, p))
    res.sort(key=lambda x: float(x[2]), reverse=True)
    return res

def loadVcbMap(vcbFile):
    res = {}
    for line in vcbFile.readlines():
        l = line.strip(' \n').split()
        if len(l) == 3:
            res[l[0]] = l[1]
    return res


def makeActualResult(tableFille, srcVcb, tstVcb):
    res = []
    for line in tableFille.readlines():
        t, s, p = line.strip(' \n').split()
        if t in srcVcb and s in tstVcb:
            res.append((srcVcb[t], tstVcb[s], p))
    res.sort(key=lambda x: float(x[2]), reverse=True)
    return res



def generateAlignCorpus(src, target):
    res = []
    for line in src.readlines():
        l = line.strip(' \n').split()
        res.append([l])
    for index, line in enumerate(target.readlines()):
        l = line.strip(' \n').split()
        res[index].append(l)
    return res

# if __name__ == '__main__':
#     csv_writer = csv.writer(open('top20s.csv', 'w'))
#     for language in ['ch', 'en', 'fr', 'gr', 'it', 'sp']:
#         csv_writer.writerow([language])
#         foldername = './agr-%s/' % language
#         model1 = '%sDict.actual.ti.final' % language
#         model3 = '%sDict.t3.final' % language
#         hmm = '%sDict.thmm.5' % language
#         src_vcb = '%sDict.trn.src.vcb' % language
#         target_vcb = '%sDict.trn.trg.vcb' % language
#         srcVcb = loadVcbMap(open('%s%s' % (foldername, src_vcb), 'r'))
#         tstVcb = loadVcbMap(open('%s%s' % (foldername, target_vcb), 'r'))
#         # generate aligned corpus json
#         corpus = generateAlignCorpus(open('%sodyssey1.agr' % foldername, 'r'), open('%sodyssey.%s' % (foldername, language), 'r'))
#         corpusFile = open('agr-%s.json' % language, 'w')
#         json.dump(corpus, corpusFile, ensure_ascii=False, encoding='utf-8')

#         #generate model1 table json
#         csv_writer.writerow(['model1'])
#         res = generateList(open('%s%s' % (foldername, model1)))
#         for i in range(20):
#             csv_writer.writerow([res[i][0], res[i][1], res[i][2]])
#         resFile = open('./agr-%s-align.json' % language, 'w')
#         json.dump(res, resFile, ensure_ascii=False, encoding='utf-8')

#         #generate model3 table json
#         csv_writer.writerow(['model3'])
#         model3Filename = '%s%s' % (foldername, model3)
#         res = makeActualResult(open(model3Filename, 'r'), srcVcb, tstVcb)
#         for i in range(20):
#             csv_writer.writerow([res[i][0], res[i][1], res[i][2]])
#         model3ResFile = open('./agr-%s-m3-align.json' % language, 'w')
#         json.dump(res, model3ResFile, ensure_ascii=False, encoding='utf-8')

#         #generate hmm table json
#         csv_writer.writerow(['hmm'])
#         hmmFilename = '%s%s' % (foldername, hmm)
#         res = makeActualResult(open(hmmFilename, 'r'), srcVcb, tstVcb)
#         for i in range(20):
#             csv_writer.writerow([res[i][0], res[i][1], res[i][2]])
#         hmmResFile = open('./agr-%s-hmm-align.json' % language, 'w')
#         json.dump(res, hmmResFile, ensure_ascii=False, encoding='utf-8')


