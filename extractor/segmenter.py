#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# this script serves to segment chinese and 
# english sentences
# 
# @author Yuan JIN
# @contact chengdujin@gmail.com
# @since 2012.03.07
# @latest 2012.03.07
#

import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

# CONSTANTS
# segmentation
WEB_SERVICE_SEG = 'http://jkx.fudan.edu.cn/fudannlp/seg/%s'
# keywords
WEB_SERVICE_KEY = 'http://jkx.fudan.edu.cn/fudannlp/key/%s'
CHINESE_STOP_WORDS = '/Users/Yuan/Downloads/socrates/extractor/chinese_stop_words'

def segment(tweets):
    'segmentation based on fudannlp web services'

    file = open(CHINESE_STOP_WORDS, 'r')
    stop_words_raw = file.readlines()
    file.close()
    stop_words = []
    for w in stop_words_raw:
        stop_words.append(w.strip())

    import urllib2
    con = urllib2.urlopen('http://jkx.fudan.edu.cn/fudannlp/seg/%s' % )
    data = con.read()

    
    for tweet in tweets:
        chinese = tweet.chinese
        for word in chinese:
            segment = mmseg.Algorithm(word)
            for word in segment:
                text = word.text
                if not text.encode('utf-8') in tweet.keywords:
                    if not text.encode('utf-8') in stop_words:
                        tweet.keywords.append(text) # unicode
        print ' '.join(tweet.chinese) 

if __name__ == '__main__':
    segment()
