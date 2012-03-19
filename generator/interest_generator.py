#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# this script serves to find out user's
# specific interests based on lda analysis
#
# @author Yuan JIN
# @contact chengdujin@gmail.com
# @since 2012.03.10
# @latest 2012.03.19
#

import random
# reload the script encoding
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

# CONSTANTS
SOURCE = 'twitter/chengdujin.chinese'
DB = '176.34.54.120:27017'


def read(source):
    'simply read segments from mongodb'
    sys.path.append('../extractor')
    from media import Segment

    lines = source.split('/')
    head = lines[0]
    content = lines[1]

    from pymongo.connection import Connection
    con = Connection(DB)
    from pymongo.database import Database
    db = Database(con, head)
    from pymongo.collection import Collection
    collection = Collection(db, content)

    cursor = collection.find()
    if cursor.count() > 0:
	    docs = []
        for entry in cursor:
            # wrap the segmented word in an Segment class
            words = []
            if 'chinese' in entry.keys():
                for word in entry['chinese']:
		            words.append(Segment(word, entry))
            if 'latin' in entry.keys():
                for word in entry['latin']:
                    words.extend(Segment(word, entry))

            if words: # array of self-aware segmented word
                docs.append(words)
	    return docs
    else:
	    return Exception("[error] read: nothing is found!")      

def generate(source):
    '''
    1. collect data from mongodb
    2. prepare data structure
    3. remove data of low frequency
    4. learn and repeat
    5. publish the result
    '''
    seg_list = read(source)
    import lda
    topic_extractor = lda.LDA(seg_list)
    #screen()
    topic_extractor.learn()
    topic_extractor.publish()

if __name__ == '__main__':
    generate(SOURCE)
