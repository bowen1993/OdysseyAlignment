import unicodedata
def strip_diacritics(s):
    return unicodedata.normalize("NFC", "".join((c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")))

def count(filename, isGreek=False):
    with open(filename, 'r') as f:
        words = []
        for line in f.readlines():
            if isGreek:
                words.extend(strip_diacritics(line.strip()).split())
            else:
                words.extend(line.strip().split())
    distinct = set(words)
    print(words[0], words[1])
    print(len(words), len(distinct))



