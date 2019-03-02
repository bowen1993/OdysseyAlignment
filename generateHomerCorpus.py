import csv
import sys
import re

import jieba

jieba.load_userdict('./ch_dict.txt')

def generateCorpusFile(languageCode, col, csv_reader):
    res_file = open('odyssey.%s' % languageCode, 'w')
    for index, row in enumerate(csv_reader):
        if len(row) <= col:
            continue
        line = row[col].strip(' \n')
        line = line.replace('\n', '')
        if languageCode == 'agr':
            line = re.sub(r'\[\d+\.?\d*\]\s', '', line)
            line = re.sub(r'\[\d+\.?\d*\]', '', line)
        if len(line) == 0:
            continue
        if languageCode == 'ch':
            # tokenize chinese file
            line = line.replace(' ', '')
            line = re.sub(r"[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）：；《）《》“”()»〔〕-]+", "", line)
            l = jieba.cut(line)
            res_file.write(u" ".join(l))
        else:
            line = re.sub(r'[\u2000-\u206F\u2E00-\u2E7F\\\'!"#$%&()*+,\-.\/:;<=>?@\[\]^_`{|}~]', '', line)
            res_file.write(line)
        res_file.write('\n')
    res_file.close()