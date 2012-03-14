#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# this script serves to train articles
#
# @author Yuan JIN
# @contact chengdujin@gmail.com
# @since 2012.03.12
# @latest 2012.03.13
#

# reload the script encoding
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

# CONSTANTS
DB = '176.34.54.120:27017'
database = 'articles'


class NaiveBayes(object):
    def __init__(self, docs):
        'disect the docs into dataset: labels and doc'
        self.label_priors = {}
        self.label_cond_prob = {}
        self.docs = docs

    def train(self):
        'calculate the priors and conditional probabilities'
        for doc in self.docs:
            category = doc.category
            chinese = doc.chinese
            segments = category + chinese

            for label in segments:
		        # compute the priors
		        if label in self.label_priors:
		            self.label_priors[label] += 1
		        else:
		            self.label_priors[label] = 1
		            self.label_cond_prob[label] = {}
		
	    	    # compute the conditional probabilities
		        for word in chinese:
		            if not word in self.label_cond_prob[label]: 
			            self.label_cond_prob[label][word] = 1
		            else:
			            self.label_cond_prob[label][word] += 1 		

    def valuate_pl(self, label):
        'calculate p(l)'
        pl = float(self.label_priors[label]) / float(len(self.label_priors))
        return pl

    def valuate_pdl(self, doc, label):
        'calculate p(d|l)'
        pdl = 1 
        for word in doc:
            if word in self.label_cond_prob[label] and word in self.label_priors:
                pdl *= float(self.label_cond_prob[label][word]) / float(self.label_priors[word])
            else:
                pdl *= 1 / float((len(self.docs) + 1))
        if pdl == 1: 
            return 1 / float(len(self.label_priors))
        else: 
            return pdl

    def valuate(self, label, doc):
        'return the probability of doc with the label'
        'calculate p(d|l) * p(l) / p(d)'
	    # p(d|l); doc should be presented as doc.chinese, e.g.
        pdl = self.valuate_pdl(doc, label)

	    # p(l)
        pl = self.valuate_pl(label)

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
        best = 0
        guess = ''
        second_guess = ''
        third_guess = ''
        fourth_guess = ''
        for label in self.label_cond_prob:
            prob = self.valuate(label, doc.chinese)
            if prob > best:
                best = prob
                fourth_guess = third_guess
                third_guess = second_guess
                second_guess = guess
                guess = label
	    
        # publish
        print doc.title
        print ','.join(doc.category)
        print second_guess, third_guess, fourth_guess
        print

def read_and_structure():
    'read data from mongodb and structure them for the classification'
    sys.path.append('../extractor/')
    import media

    from pymongo.connection import Connection
    con = Connection(DB)
    from pymongo.database import Database
    db = Database(con, database)
    
    def restructure(category):
        new_category = []
        for item in category:
	        if not item.strip():
		        continue
	        else:
		        if '/' in item:
		            splits = item.split('/')
		            for split in splits:
			            if split:
			                new_category.append(split.strip())
		        else:
		            new_category.append(item.strip())
        return new_category

    from pymongo.collection import Collection
    collections = db.collection_names()
    articles = []
    for col in collections:
        if col <> 'system.indexes':
            collection = Collection(db, col)
            cursor = collection.find()
            for entry in cursor:
                article = media.Article()
                article.title = entry['title']
                article.published = entry['published']
                article.source = entry['source']
                article.category = restructure(entry['category'])
                article.chinese = entry['chinese']
                articles.append(article)
    return articles
   
def main():
    'main entrance to read data from db, train and classify'
    articles = read_and_structure()
    training_size = int(len(articles) * 0.9)
    training = []
    for id in range(training_size):
        article = articles.pop()
        training.append(article)

    # naive bayes training
    nb = NaiveBayes(training)
    nb.train()
    
    # testing
    for article in articles:
        nb.classify(article)

if __name__ == "__main__":
    main()
