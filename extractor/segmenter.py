#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# this script serves to segment chinese and 
# english sentences
# 
# @author Yuan JIN
# @contact chengdujin@gmail.com
# @since 2012.03.06
# @latest 2012.03.07
#

import sys
reload(sys)
sys.setdefaultencoding('UTF-8')


def segment_tweet(tweets):
    'simple chinese segmentation'
    import mmseg

    file = open(CHINESE_STOP_WORDS, 'r')
    stop_words_raw = file.readlines()
    file.close()
    stop_words = []
    for w in stop_words_raw:
        stop_words.append(w.strip())

    mmseg.dict_load_defaults()
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
