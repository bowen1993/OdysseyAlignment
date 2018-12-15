import csv
import json
from generateHomerCorpus import generateCorpusFile
from jsonifyResults import *
import subprocess
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def generateAllCorpusFiles(languages, csvFilename):
    for language, col in languages:
        with open(csvFilename, 'r') as csvFile:
            csv_reader = csv.reader(csvFile)
            generateCorpusFile(language, col, csv_reader)

def runAlignments(languages):
    for language in languages:
        print( bcolors.OKBLUE + 'Aligning %s' % language + bcolors.ENDC)
        filename = 'odyssey.%s' % language
        numOfLines = subprocess.check_output(['wc', '-l', filename]).strip().split()[0]
        os.system('head -n %s odyssey.agr > odyssey_%s.agr' % (numOfLines, language))
        subprocess.call(['./run.sh', 'odyssey_%s.agr' % language, filename, '%sDict' % language])

def generateJSONData(languages):
    csv_writer = csv.writer(open('top20s.csv', 'w'))
    for language in languages:
        csv_writer.writerow([language])
        # filenames
        model1 = '%sDict.actual.ti.final' % language
        model3 = '%sDict.t3.final' % language
        hmm = '%sDict.thmm.10' % language
        src_vcb = 'odyssey_%s.agr.vcb' % language
        target_vcb = 'odyssey.%s.vcb' % language

        #load vcb
        srcVcb = loadVcbMap(open(src_vcb, 'r'))
        trgVcb = loadVcbMap(open(target_vcb, 'r'))
        
        #generate aligned corpus in JSON
        corpus = generateAlignCorpus(open('odyssey_%s.agr' % language, 'r'), open('odyssey.%s' % language, 'r'))
        corpusFile = open('agr-%s.json' % language, 'w')
        json.dump(corpus, corpusFile, ensure_ascii=False, encoding='utf-8')

        #generate model1 table json
        csv_writer.writerow(['model1'])
        res = generateList(open(model1, 'r'))
        for i in range(20):
            csv_writer.writerow([res[i][0], res[i][1], res[i][2]])
        resFile = open('./agr-%s-align.json' % language, 'w')
        json.dump(res, resFile, ensure_ascii=False, encoding='utf-8')

        #generate model3 table json
        csv_writer.writerow(['model3'])
        res = makeActualResult(open(model3, 'r'), srcVcb, trgVcb)
        for i in range(20):
            csv_writer.writerow([res[i][0], res[i][1], res[i][2]])
        model3ResFile = open('./agr-%s-m3-align.json' % language, 'w')
        json.dump(res, model3ResFile, ensure_ascii=False, encoding='utf-8')

        #generate hmm table json
        csv_writer.writerow(['hmm'])
        res = makeActualResult(open(hmm, 'r'), srcVcb, trgVcb)
        for i in range(100):
            csv_writer.writerow([res[i][0], res[i][1], res[i][2]])
        hmmResFile = open('./agr-%s-hmm-align.json' % language, 'w')
        json.dump(res, hmmResFile, ensure_ascii=False, encoding='utf-8')

def removeTmpFiles():
    os.system('rm odyssey*')
    os.system('rm *Dict*')

if __name__ == '__main__':
    allLanguages = [('ch', 6), ('en', 4), ('fr', 8), ('gr', 3), ('it', 5), ('sp', 7), ('agr', 2), ('pe', 9)]
    targetLanguages = ['ch', 'gr', 'fr', 'it', 'sp', 'en', 'pe']
    print(bcolors.HEADER + '###############Generating Corpus Files###############' + bcolors.ENDC)
    generateAllCorpusFiles(allLanguages, 'OdysseyAlign.csv')
    print(bcolors.HEADER + '###############Running Alignments###############' + bcolors.ENDC)
    runAlignments(targetLanguages)
    print(bcolors.HEADER + '###############Generating JSON Data###############' + bcolors.ENDC)
    generateJSONData(targetLanguages)
    removeTmpFiles()
    print(bcolors.BOLD + bcolors.OKGREEN + "Finish!" + bcolors.ENDC)