import jieba

jieba.load_userdict('./odyssey_ch_dict.txt')

# df = open('./odyssey_ch_dict.txt', 'r')
# for line in df.readlines():
#     jieba.add_word(line.strip(u' \n'))

inpf = open('./odyssey.ch', 'r')
resf = open('./odyssey_token.ch', 'w')

for line in inpf.readlines():
    l = jieba.cut(line.decode('utf8'))
    resf.write(u" ".join(l).encode('utf8'))
