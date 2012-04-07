#!/home/work/python/bin/python
# -*- coding: utf-8 -*-

import ngram
import pprint
import sys

reload(sys)
sys.setdefaultencoding("UTF-8")

def concat(bigrams, bigram):
    result = ''
    values = bigrams[bigram]
    for value in values:
	result += unicode(value)
    return result

def main():
    index = ngram.NGram(pad_len=1,N=2)
    bigrams = {}

    input = open('/home/work/yuanj/output.txt', 'r')
    entries = input.readlines()

    for entry in entries:
        # tokenize
        token = unicode(entry.strip().strip(",.!|&-_()[]<>{}/\"'").strip())
        enbis = index.ngrams_pad(token)

        # add to the dictionary
        for bigram in enbis:
	    bigram = unicode(bigram)
            if bigram in bigrams:
                tokens = bigrams[bigram]
                tokens.append('||' + token)
                bigrams[bigram] = tokens
            else:
                bigrams[bigram] = [token]
    input.close()

    # output the bigram reverse index
    output = open('/home/work/yuanj/bigrams.txt', 'w')
    for bigram in bigrams:
        output.write(bigram + ":" + concat(bigrams, unicode(bigram)) + '\n')
        #output.write(bigram + ":" + str(len(bigrams[bigram])) + '\n')

if __name__ == '__main__':
    main()
