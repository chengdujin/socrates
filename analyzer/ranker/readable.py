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
import os

# reload the script encoding
import sys 
reload(sys)
sys.setdefaultencoding('UTF-8')


def generate(doc_id):
    'entrance to readability'
    '1. find the source url of the doc_id'
    '2. call readability-lxml to generate hmtl'
    collections = db.collection_names()
    doc = None
    for collection in collections:
        if collection <> 'system.indexes' and collection <> 'classified':
            col = Collection(db, collection)
            doc = col.find_one({'_id':ObjectId(doc_id)})  
            if doc:
                break
    if doc:
        doc_url = doc['source']
        doc_html = urllib.urlopen(doc_url).read()
        readable_doc = Document(doc_html).summary()
        readable_doc_title = Document(doc_html).short_title()
        return readable_doc, readable_doc_title
    else:
        return None

def generate_html(id_list):
    'generate html code for every article id'
    os.system('rm -f /home/ec2-user/socrates/read/*')
    for id in id_list:
        html, title = generate(id)
        # save them onto disk
        try:
            f = open('/home/ec2-user/socrates/read/%s.html' % title, 'w')
            f.write(html)
            f.close()
            print 'successfully generate %s.html' % title
        except Exception as e:
            print 'cannot generate %s.html' % title
            pass
    # send the file to the wordpress server
    os.system("scp -i /home/ec2-user/socrates.pem /home/ec2-user/socrates/read/* ec2-user@176.34.54.120:/home/ec2-user/read/")

if __name__ == '__main__':
    id_list = ['4f6710e7ca5be34ea7000000', '4f6710e7ca5be34ea7000001', '4f661c76ca5be32a26000002']
    generate_html(id_list)
