#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# this script serves to do the dirty cleaning work for
# users' tweets.
# 
# @author Yuan JIN
# @contact chengdujin@gmail.com
# @since 2012.03.08
# @latest 2012.03.08
#

# reload the script encoding
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')


def generate(source='twitter'):
    'combines cleaner and segmenter'
    import cleaner, segmenter
    
    documents = []
    source = source.strip().lower()
    if source == 'twitter':
        'output a list of Tweet instances'
        tweets = cleaner.clean(source)
        documents = segmenter.segment(tweets)

    return documents

if __name__ == '__main__':
    generate('twitter')
