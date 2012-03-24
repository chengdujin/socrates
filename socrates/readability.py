#!/usr/bin/python                                                              
# -*- coding: utf-8 -*-

##
# this script serves to turn an articl id into
# readability-suited html code
#
# @author Yuan JIN
# @contact chengdujin@gmail.com
# @since 2012.03.24
# @latest 2012.03.24
#

from pymongo.connection import Connection
con = Connection('176.34.54.120:27017')
from pymongo.database import Database
db = Database(con, 'articles')
from pymongo.collection import Collection
from pymongo.objectid import ObjectId

from readability.readability import Document
import urllib

# reload the script encoding
import sys 
reload(sys)
sys.setdefaultencoding('UTF-8')


def generate_html(doc_id):
    'entrance to readability'
    '1. find the source url of the doc_id'
    '2. call readability-lxml to generate hmtl'
    collections = db.collection_names()
    doc_url = None
    for collection in collections:
        if collection <> 'system.indexes' and collection <> 'classified':
            col = Collection(db, collection)
            doc = col.find_one({'_id':ObjectId(doc_id)})  
            if doc:
                doc_url = doc['source']
                break
    if doc_url:
        doc_html = urllib.urlopen(doc_url).read()
        readable_doc = Document(doc_html).summary()
        return readable_doc
