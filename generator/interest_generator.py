#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# this script serves to find out user's
# specific interests based on lda analysis
#
# @author Yuan JIN
# @contact chengdujin@gmail.com
# @since 2012.03.10
# @latest 2012.03.21
#

# reload the script encoding
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

# CONSTANTS
SOURCE = 'twitter/perryhau'
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
            if 'chinese' in entry:
                for word in entry['chinese']:
                    if word:
		                words.append(Segment(word, entry))
            if 'latin' in entry:
                for word in entry['latin']:
                    if word:
                        words.append(Segment(word, entry))

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
    6. cluster the result
    7. publish the clustered segemented words
    '''

    # read data from mongodb
    print 'reading data from database'
    seg_list = read(source)

    # compute hidden topics via lda
    print '\nlda starting ...'
    import lda
    topic_extractor = lda.LDA(seg_list)
    #screen()
    topic_extractor.learn()
    # topics is a collection of Segment instances
    topics = topic_extractor.publish()

    # cluster the segemented words
    print '\nclustering ...'
    import kmeans
    km = kmeans.KMeans(5, seg_list)
    km.cluster()
    cluster = km.publish()
    
if __name__ == '__main__':
    generate(SOURCE)
