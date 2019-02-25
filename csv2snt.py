import os
import sys
import argparse
import csv
from wordSearch import Searcher, getWordCTSID
import re

def filterChars(line):
    line = line.strip()
    line = re.sub(r'\[\d+\.?\d*\]\s', '', line)
    line = re.sub(r'\[\d+\.?\d*\]', '', line)
    line = re.sub(r'[\u2000-\u206F\u2E00-\u2E7F\\\'!"#$%&()*+,\-.\/:;<=>?@\[\]^_`{|}~]', '', line)
    return line

def generateIDs(line, IDMap, searcher, CTS=None, isLemma=False):
    words = line.split()
    for word in words:
        if word not in IDMap:
            if not CTS:
                cites = getWordCTSID(word, searcher, isLemma)
            else:
                cites = CTS
            IDMap[word] = [len(IDMap)+1, 1, cites]
        else:
            IDMap[word][1] += 1
    

def generateIDMaps(filename):
    corpusFile = open(filename, 'r')
    csvReader = csv.reader(corpusFile)
    IDMapEN = dict()
    IDMapGR = dict()
    IDMapGRL = dict()
    searcher = Searcher('tlg0012.tlg002.perseus-grc1.tb.xml')
    for row in csvReader:
        subdoc = row[1]
        CTSs = subdoc.split('-')
        enLine = filterChars(row[3])
        grLine = filterChars(row[2])
        grlLine = filterChars(row[4])
        generateIDs(enLine, IDMapEN, searcher, CTSs)
        generateIDs(grLine, IDMapGR, searcher)
        generateIDs(grlLine, IDMapGRL, searcher, None, True)
    return IDMapEN, IDMapGR, IDMapGRL

def writeToFile(l1, l2, srcIDMap, targetIDMap, outputFile):
    srcWords = l1.split()
    targetWords = l2.split()
    outputFile.write('1\n')
    srcSentList = [str(srcIDMap[word][0]) for word in srcWords]
    targetSentList = [str(targetIDMap[word][0]) for word in targetWords]
    outputFile.write(' '.join(srcSentList) + '\n')
    outputFile.write(' '.join(targetSentList) + '\n')

def generateSNTFile(csvFilename, enIDMap, grIDMap, grlIDMap):
    outputFilenamegr = 'odyssey.en_odyssey.agr.snt'
    outputFilenamegrl = 'odyssey.en_odyssey.agrl.snt'
    csvReader = csv.reader(open(csvFilename, 'r'))
    outputFilegr = open(outputFilenamegr, 'w')
    outputFilegrl = open(outputFilenamegrl, 'w')
    for row in csvReader:
        enLine = filterChars(row[3])
        grLine = filterChars(row[2])
        grlLine = filterChars(row[4])
        writeToFile(grLine, enLine, grIDMap, enIDMap, outputFilegr)
        writeToFile(grlLine, enLine, grlIDMap, enIDMap, outputFilegrl)
    outputFilegr.close()
    outputFilegrl.close()

def outputIDtoFile(filename, IDMap):
    outputFilename = '%s.vcb' % filename
    with open(outputFilename, 'w') as outputFile:
        for word in IDMap:
            outputFile.write('%d %s %d %s\n' % (IDMap[word][0], word, IDMap[word][1], ' '.join(IDMap[word][2])))
            outputFile.flush()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='GIZA++ plain text to giza++ snt text', prog='plain2snt.py')
    parser.add_argument('file', help="csv data files")
    args = parser.parse_args()
    if not args.file:
        parser.print_help()
        exit(1)
    print('Generating id')
    enIDMap, GRIDMap, GRLIDMap = generateIDMaps(args.file)
    print('Writing ID to file')
    print('EN')
    outputIDtoFile('odyssey.en', enIDMap)
    print('GREEK')
    outputIDtoFile('odyssey.agr', GRIDMap)
    print('GREEK LEMMA')
    outputIDtoFile('odyssey.agrl', GRLIDMap)
    generateSNTFile(args.file, enIDMap, GRIDMap, GRLIDMap)