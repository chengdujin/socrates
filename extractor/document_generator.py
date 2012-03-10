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


# CONSTANTS
DB = '176.34.54.120:27017'
INPUT = 'twitter/mijia'

def publish(docs, source):
    'leave a mark in database'
    source_info = source.strip().lower().split('/')
    database = source_info[0]
    collection = source_info[1]

    from pymongo.errors import CollectionInvalid
    from pymongo.connection import Connection
    con = Connection(DB)
    from pymongo.database import Database
    db = Database(con, database)
    from pymongo.collection import Collection
    new_collection = collection + '.chinese'
    col = None
    try:
        col = db.create_collection(new_collection)
    except CollectionInvalid as e:
        col = Collection(db, new_collection)
    for doc in docs:
        col.insert({'seg':doc.chinese}) 

def generate(source='articles/cnbeta'):
    'combines cleaner and segmenter'
    import cleaner, segmenter
    
    documents = []
    items = cleaner.clean(source)
    documents = segmenter.segment(items)
    publish(documents, source)
    
    return documents

if __name__ == '__main__':
    generate(INPUT)
