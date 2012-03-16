#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# this script serves to do the dirty cleaning work for
# users' tweets.
# 
# @author Yuan JIN
# @contact chengdujin@gmail.com
# @since 2012.03.06
# @latest 2012.03.08
#

# reload the script encoding
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

# CONSTANTS
# Database Configuration
DB = '176.34.54.120:27017'
MICRO_BLOGS = ['twitter', 'weibo']
NEWS_SOURCES = ['articles']

def clean(source='articles/cnBeta'):
    'collect, rearrange and filter information'
    import media
    doc_type = media.Document()
    source = source.strip().lower()
    database = {}
 
    # [0] database name [1] collection name
    source_info = source.split('/')
    database['db'] = source_info[0]
    database['collection'] = source_info[1]
    
    if source_info[0] in MICRO_BLOGS:
        doc_type = media.Twitter()
    elif source_info[0] in NEWS_SOURCES:
        doc_type = media.News()
    else:
        return Exception('[error] cleaner: such source does not exist!')

    # read data from database
    docs = doc_type.collect_data(database)

    # build document model
    collection = []
    for doc in docs:
        if doc:
            item = doc_type.build_model(doc)
            collection.append(item)

    return collection

if __name__ == '__main__':
    clean('articles/cnbeta')
