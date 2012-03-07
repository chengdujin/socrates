#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# this script serves to do the dirty cleaning work for
# users' tweets.
# 
# @author Yuan JIN
# @contact chengdujin@gmail.com
# @since 2012.03.06
# @latest 2012.03.07
#

# reload the script encoding
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

# CONSTANTS
DOCUMENT_PATH = '/Users/Yuan/Downloads/socrates/extractor'
# Database Configuration
DB = {'host':'localhost', 'port':27017}


def cleaner(source='twitter'):
    'collect, rearrange and filter information'
    sys.path.append(DOCUMENT_PATH)
    import media

    doc_type = media.Document()
    if 'twitter' in source:
        doc_type = media.Twitter()
    elif 'songshuhui' in source:
        #doc_type = media.News()
        pass
    else:
        return Exception('[error] cleaner: such source does not exist!')

    # read data from database
    docs = doc_type.collect_data(DB)

    # build document model
    collection = []
    for doc in docs:
        item = doc_type.build_model(doc)
        print ', '.join(item.latin)
        collection.append(item)

    return collection

if __name__ == '__main__':
    cleaner('twitter')
