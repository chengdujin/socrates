#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# this script serves to find out user's
# specific interests
#
# @author Yuan JIN
# @contact chengdujin@gmail.com
# @since 2012.03.10
# @latest 2012.03.10
#

# reload the script encoding
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

# CONSTANTS
SOURCE = 'twitter/perryhau.chinese'
DB = '176.34.54.120:27017'


def initialize(segs):
    ''
    pass

def read(source):
    'simply read segments from mongodb'
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
            if 'seg' in entry.keys():
		docs.append(entry['seg'])
	return docs
    else:
	return Exception("[errot] read: nothing is found!")      

def generate(source):
    '''
    1. collect data from mongodb
    2. prepare data structure
    3. remove data of low frequency
    4. learn and repeat
    5. publish the result
    '''
    seg_list = read(source)
    initialize(seg_list)
    screen()
    learn()
    publish()

if __name__ == '__main__':
    generate(SOURCE)
