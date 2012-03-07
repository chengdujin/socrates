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

## CONSTANTS
CHINESE_STOP_WORDS = '/Users/Yuan/Downloads/socrates/extractor/chinese_stop_words'

## Database Configuration
DB = {'host':'localhost', 'port':'27017'}


def __filter_tweet(word_list):
    'remove punctuations, digits, space and separate chinese and latins'
    import re, string
    
    chinese = []
    latin = []
    identify = string.maketrans('', '')
    for word in word_list:
        # remove unnecessary characters
        word = (word.encode('utf-8')).translate(identify, string.punctuation)
        if word.isalpha():
            # then it is composed of alphabets, francais?
            latin.append(word.decode('utf-8'))
        else: # japanaese?
            chinese.append(word.decode('utf-8'))

    return chinese, latin

def __model_data(docs):
   'fill in the document instance with data from the docs' 
    collection = []
    for doc in docs:
        item = Document()
        item.build_model(doc)
        collection.append(item)
    return collection

def __collect_data(doc):
    'collect data from mongodb'
    return doc.read_datase(DB)

def cleaner(source='twitter'):
    'collect, rearrange and filter information'
    try:
        doc_type = Document()
        if 'twitter' in source:
            doc_type = Twitter()
        elif 'songshuhui' in source:
            doc_type = News()
        else:
            return Exception('[error] cleaner: such source does not exist!')

        docs = __collect_data(doc_type)
        collection = __model_data(docs)
        return collection
    except Exception as e:
        print e
        return None
