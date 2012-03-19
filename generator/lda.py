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
# @latest 2012.03.19
#

# reload the script encoding
import sys 
reload(sys)
sys.setdefaultencoding('UTF-8')

TOPIC_NUMBER = 20
ALPHA = 2
BETA = .5
ITERATION = 1000
burnin = 500

class LDA(object):
    'class to model lda computation'
    def __init__(self, docs):
        'create data structure and initialize them'
        self.index_vocab, self.vocab_index = self.vocab_indexer(docs)
        self.doc_vocab_topic = self.initialize(docs, vocabs)    

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

    def initialize(docs, vocabs):
        'initialize doc_vocab, vocab_topic, doc_topic and topic lists'
        index_vocab = vocabs[0]
        vocab_index = vocabs[1]
        doc_vocab = {}
        vocab_topic = {}
        doc_topic = {}
        topics = {}
        documents = {}
        for doc_id, doc in enumerate(docs):
            dc = {}
            # build documents
            documents[doc_id] = len(doc)
            for word in doc:
                rand_topic = random.randint(1, TOPIC_NUMBER)
                word_vocab_id = vocab_index[word]
                # build doc-vocab
                dc[word_vocab_id] = rand_topic

                # build vocab-topic
                if not word_vocab_id in vocab_topic:
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
            if not doc_id in doc_topic:
                dt = {}
                dt[rand_topic] = 1
            else:
                if rand_topic in dt:
                    dt[rand_topic] += 1
                else:
                    dt[rand_topic] = 1
            doc_topic[doc_id] = dt

            # build topic
            if not rand_topic in topics:
                topics[rand_topic] = 1
            else:
                topics[rand_topic] += 1
            doc_vocab[doc_id] = dc

        return (doc_vocab, vocab_topic, doc_topic, topics, documents)

    def learn(vocabs, data):
        'lda implementation'
        index_vocab = vocabs[0]
        vocab_index = vocabs[1]

        doc_vocab = data[0]
        vocab_topic = data[1]
        doc_topic = data[2]
        topics = data[3]
        documents = data[4]
        for it in xrange(0, ITERATION):
        for doc_id in doc_vocab:
            for word_vocab_id in doc_vocab[doc_id]:
            # sample full conditional
                topic = doc_vocab[doc_id][word_vocab_id]
                vocab_topic[word_vocab_id][topic] -= 1
            doc_topic[doc_id][topic] -= 1
            topics[topic] -= 1
            documents[doc_id] -= 1

            # multinomial sampling via cumulative method
            probability = {}
                for k in xrange(0, TOPIC_NUMBER):
                probability[k] = (vocab_topic[word_vocab_id][topic] + BETA) / (topics[topic] + len(vocab_index) * BETA) * (doc_topic[doc_id][topic] + ALPHA) / (documents[doc_id] + TOPIC_NUMBER * ALPHA)
            # cumulate multinomial parameters
            for k in xrange(1, len(probability)):
                probability[k] += probability[k - 1];

            # caled sample because of unnormalised probability[]
                u = random.random() * probability[TOPIC_NUMBER -1]
            for topic in xrange(0, len(probability)):
                if probability[topic] > u:
                break

            # add back new estimated value
            if not topic in vocab_topic[word_vocab_id]:
                vocab_topic[word_vocab_id][topic] = 1
            else:
                vocab_topic[word_vocab_id][topic] += 1
            if not topic in doc_topic[doc_id]:
                    doc_topic[doc_id][topic] = 1
            else:
                doc_topic[doc_id][topic] += 1
            if not topic in topics:
                topics[topic] = 1
            else:
                    topics[topic] += 1
                documents[doc_id] += 1
            doc_vocab[doc_id][word_vocab_id] = topic

        return (doc_vocab, vocab_topic, doc_topic, topics, documents)

    def publish(docs, vocabs, data):
        'simple publication'
        from collections import OrderedDict

        index_vocab = vocabs[0]
        vocab_index = vocabs[1]

        doc_vocab = data[0]
        vocab_topic = data[1]
        doc_topic = data[2]
        topics = data[3]
        documents = data[4]

        # build topic-vocab map
        topic_vocab = {}
        for word_vocab_id in vocab_topic:
            vt = vocab_topic[word_vocab_id]
            sorted_vt = OrderedDict(sorted(vt.items(), key=lambda x: -x[1]))
            for svt, (k, v) in enumerate(sorted_vt.items()):
                if svt > 3:
                    break
                else:
                    if not k in topic_vocab:
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
            topic_word[topic_id] = ''
            tv = topic_vocab[topic_id]
            sorted_tv = OrderedDict(sorted(tv.items(), key=lambda x: -x[1]))
            for stv, (k, v) in enumerate(sorted_tv.items()):
                if stv > 3:
                    break
                else:
                    topic_word[topic_id] += index_vocab[k] + ','

        # publish
        for doc_id, doc in enumerate(docs):
            if doc_id in doc_topic and len(doc) > 2:
                topic_list = doc_topic[doc_id]
                sorted_topic_list =  OrderedDict(sorted(topic_list.items(), key=lambda x: -x[1]))
                wanted_strings = []
                for stl, (k, v) in enumerate(sorted_topic_list.items()):
                    if stl > 3:
                        break
                    else:
                        wanted_strings.append(topic_word[k])
            print str(doc_id + 1) + '.' +  ','.join(doc)
            print '>> ' + ' '.join(wanted_strings)
            print

if __name__ == '__main__':
    pass
