import os
import sys
import argparse
from wordSearch import Searcher, getWordCTSID

def generateIDMap(filename, isLemma=False, isCTS=False):
    corpusFile = open(filename, 'r')
    IDMap = dict()
    searcher = Searcher('tlg0012.tlg002.perseus-grc1.tb.xml')
    for line in corpusFile.readlines():
        line = line.strip()
        words = line.split()
        for word in words:
            if word not in IDMap:
                if isCTS:
                    cites = getWordCTSID(word, searcher, isLemma)
                else:
                    cites = []
                IDMap[word] = [len(IDMap), 1, cites]
            else:
                IDMap[word][1] += 1
    return IDMap

def outputIDtoFile(filename, IDMap):
    outputFilename = '%s.vcb' % filename
    with open(outputFilename, 'w') as outputFile:
        for word in IDMap:
            outputFile.write('%d %s %d %s\n' % (IDMap[word][0], word, IDMap[word][1], ' '.join(IDMap[word][2])))
            outputFile.flush()


def generateSNTFile(srcFilename, targetFilename, srcIDMap, targetIDMap):
    outputFilename = '%s_%s.snt' % (srcFilename, targetFilename)
    outputFile = open(outputFilename, 'w')
    with open(srcFilename, 'r') as srcFile, open(targetFilename, 'r') as targetFile:
        for src, target in zip(srcFile, targetFile):
            srcWords = src.strip().split()
            targetWords = target.strip().split()
            outputFile.write('1\n')
            srcSentList = [str(srcIDMap[word][0]) for word in srcWords]
            targetSentList = [str(targetIDMap[word][0]) for word in targetWords]
            outputFile.write(' '.join(srcSentList) + '\n')
            outputFile.write(' '.join(targetSentList) + '\n')
    outputFile.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='GIZA++ plain text to giza++ snt text', prog='plain2snt.py')
    parser.add_argument('files', nargs="+", help="plain text files")
    parser.add_argument('--lemma', type=bool, help="is lemma file")
    parser.add_argument('--cts', type=int, help="index for getting cts ids")
    args = parser.parse_args()
    if not args.files:
        parser.print_help()
        exit(1)
    cts = args.cts if args.cts else 0
    isLemma = args.lemma if args.lemma else False
    print('Generating id')
    print('file %s' % args.files[0])
    IDMap1 = generateIDMap(args.files[0], isLemma, cts==0)
    outputIDtoFile(args.files[0], IDMap1)
    print('file %s' % args.files[1])
    IDMap2 = generateIDMap(args.files[1], isLemma, cts==1)
    outputIDtoFile(args.files[1], IDMap2)
    print('Generating snt files')
    generateSNTFile(args.files[0], args.files[1], IDMap1, IDMap2)
    generateSNTFile(args.files[1], args.files[0], IDMap2, IDMap1)
