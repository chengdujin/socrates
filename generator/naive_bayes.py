#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# this script serves to train articles, and 
# classify a new article
#
# @author Yuan JIN
# @contact chengdujin@gmail.com
# @since 2012.03.12
# @latest 2012.03.13
#


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
   
if __name__ == "__main__":
    pass
