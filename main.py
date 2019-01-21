import csv
import sys
import json
from generateHomerCorpus import generateCorpusFile
from jsonifyResults import *
import subprocess
import os
import argparse
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

def getFileNumOfLines(filename):
    p = subprocess.Popen(['wc', '-l', filename], stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE)
    result, err = p.communicate()
    if p.returncode != 0:
        print('File %s broken' % filename)
        exit(1)
    return int(result.strip().split()[0])

def runAlignments(languages):
    for language in languages:
        filename = 'odyssey.%s' % language
        numOfLines = getFileNumOfLines(filename)
        print(numOfLines)
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
        json.dump(corpus, corpusFile, ensure_ascii=False)

        #generate model1 table json
        csv_writer.writerow(['model1'])
        res = generateList(open(model1, 'r'))
        for i in range(20):
            csv_writer.writerow([res[i][0], res[i][1], res[i][2]])
        resFile = open('./agr-%s-align.json' % language, 'w')
        json.dump(res, resFile, ensure_ascii=False)

        #generate model3 table json
        csv_writer.writerow(['model3'])
        res = makeActualResult(open(model3, 'r'), srcVcb, trgVcb)
        for i in range(20):
            csv_writer.writerow([res[i][0], res[i][1], res[i][2]])
        model3ResFile = open('./agr-%s-m3-align.json' % language, 'w')
        json.dump(res, model3ResFile, ensure_ascii=False)

        #generate hmm table json
        csv_writer.writerow(['hmm'])
        res = makeActualResult(open(hmm, 'r'), srcVcb, trgVcb)
        for i in range(100):
            csv_writer.writerow([res[i][0], res[i][1], res[i][2]])
        hmmResFile = open('./agr-%s-hmm-align.json' % language, 'w')
        json.dump(res, hmmResFile, ensure_ascii=False)

def removeTmpFiles():
    os.system('rm odyssey*')
    os.system('rm *Dict*')

def parseLanguageColumn(configFilename):
    if not os.path.exists(configFilename):
        return None
    configFile = open(configFilename, 'r')
    csv_reader = csv.reader(configFile)
    return [(row[0], int(row[1])) for row in csv_reader]

def checkLanguages(languageCols, source, targets):
    languages = [x for x in zip(*languageCols)][0]
    for target in targets:
        if target not in languages:
            return False
    return source in languages

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Odyssey Aligner', prog='main.py')
    parser.add_argument('--filename', help="Alignment CSV file")
    parser.add_argument('--config', help="config filename")
    parser.add_argument('--targets', nargs="+", help="target languages")
    parser.add_argument('--src', help="source language")
    args = parser.parse_args()
    if not args.config:
        parser.print_help()
        exit(1)
    languageCols = parseLanguageColumn(args.config)
    targets = args.targets
    source = args.src
    if not source or not targets or not languageCols or not checkLanguages(languageCols, source, targets):
        parser.print_help()
        exit(1)
    print(languageCols,targets,source )
    print(bcolors.HEADER + '###############Generating Corpus Files###############'+ bcolors.ENDC)
    generateAllCorpusFiles(languageCols, 'OdysseyAlign.csv')
    print(bcolors.HEADER + '###############Running Alignments###############'+ bcolors.ENDC)
    runAlignments(targets)
    print(bcolors.HEADER + '###############Generating JSON Data###############' + bcolors.ENDC)
    generateJSONData(targets)
    removeTmpFiles()
    print(bcolors.BOLD + bcolors.OKGREEN + "Finish!" + bcolors.ENDC)