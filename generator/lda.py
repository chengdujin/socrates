#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# this script serves to use lda - latent
# dirichlet allocation to find out the
# hidden topics of documents (incl. Tweets)
#
# @author Yuan JIN
# @contact chengdujin@gmail.com
# @since 2012.03.18
# @latest 2012.03.21
#

import random
# reload the script encoding
import sys 
reload(sys)
sys.setdefaultencoding('UTF-8')

TOPIC_NUMBER = 10
ALPHA = 2
BETA = .5
ITERATION = 500
burnin = 200

class LDA(object):
    'class to model lda computation'
    def __init__(self, docs):
        'create data structure and initialize them'
        self.docs = docs
        self.index_vocab, self.vocab_index = self.indexer()
        self.doc_vocab, self.vocab_topic, self.doc_topic, self.topics, self.documents = self.initialize()    

    def indexer(self):
        'create an word_id-word list, and word-word_id dict'
        # word_id --> word
        index_vocab = []
        # word --> word_id
        vocab_index = {}

        # a 'terms' refers to all the segmented words of a tweet/weibo
        for terms in self.docs:
            # a term is an instance of media.Segment class
            for term in terms:
                if term not in vocab_index:
                    index_number = len(index_vocab)
                    index_vocab.append(term)
                    vocab_index[term] = index_number
        return index_vocab, vocab_index

    def initialize(self):
        'initialize doc_vocab, vocab_topic, doc_topic and topic lists'
        doc_vocab = {}
        vocab_topic = {}
        doc_topic = {}
        topics = {}
        documents = {}

        for doc_id, doc in enumerate(self.docs):
            # build documents
            # a doc is a collection of Segment instances
            documents[doc_id] = len(doc)

            dc = {}
            # a word is an instance of Segment
            for word in doc:
                rand_topic = random.randint(0, TOPIC_NUMBER-1)
                word_vocab_id = self.vocab_index[word]
                # build doc-vocab
                dc[word_vocab_id] = rand_topic

                # build vocab-topic
                if word_vocab_id not in vocab_topic:
                    vt = {}
                    vt[rand_topic] = 1
                else:
                    vt = vocab_topic[word_vocab_id]
                    if rand_topic in vt:
                        vt[rand_topic] += 1
                    else:
                        vt[rand_topic] = 1
                vocab_topic[word_vocab_id] = vt

                # build doc-topic
                if doc_id not in doc_topic:
                    dt = {}
                    dt[rand_topic] = 1
                else:
                    if rand_topic in dt:
                        dt[rand_topic] += 1
                    else:
                        dt[rand_topic] = 1
                doc_topic[doc_id] = dt

                # build topic
                if rand_topic not in topics:
                    topics[rand_topic] = 1
                else:
                    topics[rand_topic] += 1
            doc_vocab[doc_id] = dc
        return doc_vocab, vocab_topic, doc_topic, topics, documents

    def learn(self):
        'lda implementation'
        for it in xrange(0, ITERATION):
            print 'processing %i of %i' % (it, ITERATION)
            for doc_id in self.doc_vocab:
                for word_vocab_id in self.doc_vocab[doc_id]:
                    # sample full conditional
                    topic = self.doc_vocab[doc_id][word_vocab_id]
                    self.vocab_topic[word_vocab_id][topic] -= 1
                    self.doc_topic[doc_id][topic] -= 1
                    self.topics[topic] -= 1
                    self.documents[doc_id] -= 1

                    # multinomial sampling via cumulative method
                    probability = {}
                    for k in xrange(0, TOPIC_NUMBER):
                        probability[k] = (float(self.vocab_topic[word_vocab_id][topic]) + float(BETA)) / (float(self.topics[topic]) + float(len(self.vocab_index)) * float(BETA)) * (float(self.doc_topic[doc_id][topic]) + float(ALPHA)) / (float(self.documents[doc_id]) + float(TOPIC_NUMBER) * float(ALPHA))
                
                    # cumulate multinomial parameters
                    for k in xrange(1, len(probability)):
                        probability[k] += probability[k - 1];

                    # scaled sample because of unnormalised probability[]
                    u = float(random.random()) * float(probability[TOPIC_NUMBER -1])
                    for topic in xrange(0, len(probability)):
                        if probability[topic] > u:
                            break

                    # add back new estimated value
                    if topic not in self.vocab_topic[word_vocab_id]:
                        self.vocab_topic[word_vocab_id][topic] = 1
                    else:
                        self.vocab_topic[word_vocab_id][topic] += 1

                    if not topic in self.doc_topic[doc_id]:
                        self.doc_topic[doc_id][topic] = 1
                    else:
                        self.doc_topic[doc_id][topic] += 1

                    if topic not in self.topics:
                        self.topics[topic] = 1
                    else:
                        self.topics[topic] += 1

                    self.documents[doc_id] += 1
                    self.doc_vocab[doc_id][word_vocab_id] = topic

    def publish_topics(self):
        'generate a list of all topics for a corpus'
        topic_word = self.generate_topic_word()
        topics_linked = []
        for topic in self.topics:
            #print ','.join([term.word for term in topic_word[topic]])
            topics_linked.append(topic_word[topic])
        return topics_linked

    def generate_topic_word(self):
        'generate estimated topics for a document'
        from collections import OrderedDict

        # build topic-vocab map
        topic_vocab = {}
        for word_vocab_id in self.vocab_topic:
            vt = self.vocab_topic[word_vocab_id]
            sorted_vt = OrderedDict(sorted(vt.items(), key=lambda x: -x[1]))
            for svt, (k, v) in enumerate(sorted_vt.items()):
                if svt > 10:
                    break
                else:
                    if k not in topic_vocab:
                        vocab_list = {}
                        vocab_list[word_vocab_id] = v
                    else:
                        vocab_list = topic_vocab[k]
                        if word_vocab_id in vocab_list:
                            old_association = vocab_list[word_vocab_id]
                            if old_association < v:
                                vocab_list[word_vocab_id] = v
                        else:
                            vocab_list[word_vocab_id] = v
                    topic_vocab[k] = vocab_list

        # combine topic-vocab with index_vocab to create a topic_id --> vocabulary list map
        topic_word = {}
        for topic_id in topic_vocab:
            topic_word[topic_id] = []
            tv = topic_vocab[topic_id]
            sorted_tv = OrderedDict(sorted(tv.items(), key=lambda x: -x[1]))
            for stv, (k, v) in enumerate(sorted_tv.items()):
                if stv > 10:
                    break
                else:
                    topic_word[topic_id].append(self.index_vocab[k])
        return topic_word

        '''# publish
        for doc_id, doc in enumerate(self.docs):
            if doc_id in self.doc_topic and len(doc) > 2:
                topic_list = self.doc_topic[doc_id]
                sorted_topic_list =  OrderedDict(sorted(topic_list.items(), key=lambda x: -x[1]))
                wanted_strings = []
                for stl, (k, v) in enumerate(sorted_topic_list.items()):
                    if stl > 3:
                        break
                    else:
                        wanted_strings.append(topic_word[k])
            print str(doc_id + 1) + '.' +  ','.join(doc)
            print '>> ' + ' '.join(wanted_strings)
            print'''

if __name__ == '__main__':
    pass
