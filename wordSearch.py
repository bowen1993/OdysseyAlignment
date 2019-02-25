from lxml import etree
from bs4 import BeautifulSoup

class Searcher(object):
    def __init__(self, filename=''):
        self.filename = filename
        self.tree = None
    
    def setFilename(self, filename):
        self.filename = filename
    
    def loadToMemory(self):
        if not self.filename:
            raise FileNotFoundError()
        with open(self.filename, 'r') as xmlFile:
            self.tree = etree.fromstring(bytes(bytearray(str(BeautifulSoup(xmlFile.read(), "xml")), encoding='utf-8')))
        
    def memorySearch(self, word, subdoc=None, isLemma=False):
        if not self.tree:
            self.loadToMemory()
        targets = self.__searchForTag(self.tree, word, subdoc, isLemma)
        return targets
    
    def releaseMemory(self):
        del self.tree
        self.tree = None

    def search(self, word, subdoc=None, isLemma=False):
        self.loadToMemory()
        res = self.memorySearch(word, subdoc, isLemma)
        self.releaseMemory()
        return res
    
    def __findSubodc(self, node, subdocId):
        sents = node.xpath("//sentence[@subdoc='%s']" % subdocId)
        if len(sents) == 0:
            raise KeyError
        return sents[0]
    
    def __searchForTag(self, node, word, subdoc, isLemma):
        if subdoc:
            node = self.__findSubodc(node, subdoc)
        xpathStr = u"{0}word[@{1}='{2}']".format('' if subdoc else '//',(u'lemma' if isLemma else u'form'), word)
        targets = node.xpath(xpathStr)
        return targets
    
def getWordCTSID(word, searcher, isLemma=False):
    nodes = searcher.memorySearch(word, subdoc=None, isLemma=isLemma)
    res = [n.get('cite') for n in nodes]
    return res
