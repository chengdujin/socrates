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

doc_top = []
top_voc = []
number_topic = 7
alpha = 2 
beta = .5
iteration = 600 
burnin = 300


def initialize(docs, vocabs):
    'initialize doc_vocab, vocab_topic, doc_topic and topic lists'
    import random
    index_vocab = vocabs[0]
    vocab_index = vocabs[1]
    number_of_vocab = len(index_vocab)
    doc_vocab = {}
    vocab_topic = {}
    doc_topic = {}
    topic = {}
    for doc_id, doc in enumerate(docs):
        dc = {} 
	for word in doc:
	    rand_topic_index_vocab_id = random.randint(1, number_of_vocab) - 1
            word_vocab_id = vocab_index[word]
	    # build doc-vocab
            dc[word_vocab_id] = rand_topic_index_vocab_id

    	    # build vocab-topic
	    if not word_vocab_id in vocab_topic:
	        vt = {}
		vt[rand_topic_index_vocab_id] = 1
	    else:
		vt = vocab_topic[word_vocab_id]
		if rand_topic_index_vocab_id in vt:
	            vt[rand_topic_index_vocab_id] += 1
		else:
		    vt[rand_topic_index_vocab_id] = 1
            vocab_topic[word_vocab_id] = vt

	    # build doc-topic
	    if not doc_id in doc_topic:
		dt = {}
		dt[rand_topic_index_vocab_id] = 1
	    else:
		if rand_topic_index_vocab_id in dt:
		    print doc_id, rand_topic_index_vocab_id
		    dt[rand_topic_index_vocab_id] += 1
    		else:
		    dt[rand_topic_index_vocab_id] = 1
	    doc_topic[doc_id] = dt
            
	    # build topic
	    if not rand_topic_index_vocab_id in topic:
		topic[rand_topic_index_vocab_id] = 1
	    else:
		topic[rand_topic_index_vocab_id] += 1
        doc_vocab[doc_id] = dc 
    
    return (doc_vocab, vocab_topic, doc_topic, topic)

def vocab_indexer(docs):
    'create an word_id-word list, and word-word_id dict'
    # word_id --> word
    index_vocab = []
    # word --> word_id
    vocab_index = {}

    for doc in docs:
        for word in doc:
	    if word not in vocab_index:     
		index = len(index_vocab)
		index_vocab.append(word)
		vocab_index[word] = index
    return (index_vocab, vocab_index)

def prepare(docs):
    ''
    vocabs = vocab_indexer(docs)
    doc_vocab_topic = initialize(docs, vocabs)    

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
    prepare(seg_list)
    #screen()
    #learn()
    #publish()

if __name__ == '__main__':
    generate(SOURCE)
