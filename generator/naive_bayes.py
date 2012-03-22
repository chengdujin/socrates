#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# this script serves to train articles, and 
# classify a new article
#
# @author Yuan JIN
# @contact chengdujin@gmail.com
# @since 2012.03.12
# @latest 2012.03.18
#

# reload the script encoding
import sys 
reload(sys)
sys.setdefaultencoding('UTF-8')


import redis
# redis constants
REDIS_SERVER = 'localhost'


class NaiveBayes(object):
    def __init__(self, docs):
        'disect the docs into dataset: labels and doc'
        self.docs = docs

    def train(self):
        'calculate the priors and conditional probabilities'
        r = redis.StrictRedis(REDIS_SERVER)
        for doc in self.docs:
            words = set(doc.category + doc.chinese + doc.latin)
            for label in doc.category:
                # compute the priors
                if r.exists(u'@%s' % label):
                    r.incr(u'@%s' % label)
                else:
                    r.set(u'@%s' % label, 1)
                    r.expire(u'@%s' % label, 60 * 60 * 24)
                # compute the conditional probabilities
                for word in words:
                    key = u'%s:%s' % (label, word)
                    if r.exists(key): 
                        r.incr(key)
                    else:
                        r.set(key, 1)
                        r.expire(key, 60 * 60 * 24)

    def valuate_pl(self, redis_cli, label):
        'calculate p(l)'
        prior = label
        return float(redis_cli.get(prior)) / float(len(redis_cli.keys(u"@*")))

    def valuate_pdl(self, redis_cli, doc, label):
        'calculate p(d|l)'
        pdl = 0 
        for word in doc:
            prior = label
            cond_prob = u'%s:%s' % (label, word)
            if redis_cli.exists(prior) and redis_cli.exists(cond_prob):
                pdl += float(redis_cli.get(cond_prob)) / float(redis_cli.get(prior))
            else:
                pdl += 1 / float(len(self.docs) + 1)
        if pdl == 0: 
            return 1 / float(len(redis_cli.keys('@*')))
        else: 
            return pdl

    def valuate(self, redis_cli, label, doc):
        'return the probability of doc with the label'
        'calculate p(d|l) * p(l) / p(d)'
	    # p(d|l); doc should be presented as doc.chinese, e.g.
        pdl = self.valuate_pdl(redis_cli, doc, label)

	    # p(l)
        pl = self.valuate_pl(redis_cli, label)
        
	    # pd
        '''pd = 0	 
        for tag in self.label_priors:
            pd += float(self.valuate_pdl(doc, tag)) * float(self.valuate_pl(tag))
        if pd == 0:
            pd = 1 / float(len(self.label_priors)) 
        '''
        return (pdl * pl)

    def classify(self, doc):
        'classify a file based on the trained model'
        'threshold says the confidence should be above some level'
        sys.path.append('../extractor')
        import media
        if isinstance(doc, media.Article):
            to_classify = doc.chinese + doc.latin
        else:
            # each d is an instance of media.Segment
            to_classify = [d.word for d in doc]

        r = redis.StrictRedis(REDIS_SERVER)
        # get all the words by indicating @ as prefix
        words = r.keys(u'@*')
        best = 0
        guesses = []
        for wid, label in enumerate(words):
            prob = self.valuate(r, label, to_classify)
            if prob > best:
                best = prob
                if len(guesses) > 10:
                    guesses = guesses[-10:]
                guesses.append((label[1:], best))
	    
        # publish
        labels = []
        if guesses:
            # turn the highest possibility at the top
            guesses.reverse()
            if len(guesses) > 7:
                labels.extend(guesses[:7]) 
            else:
                labels.extend(guesses)
            if labels:
                return labels
        return None
 
if __name__ == "__main__":
    pass
