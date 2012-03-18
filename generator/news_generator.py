#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# this script serves to integrate classifier
# and cluster scripts
#
# @author Yuan JIN
# @contact chengdujin@gmail.com
# @since 2012.03.16
# @latest 2012.03.18
#


# reload the script encoding
import sys 
reload(sys)
sys.setdefaultencoding('UTF-8')

# CONSTANTS
DB = '176.34.54.120:27017'
ARTICLES = 'articles'
CLASSIFIED = 'classified'

from pymongo.connection import Connection
con = Connection(DB)
from pymongo.database import Database
db = Database(con, ARTICLES)
from pymongo.collection import Collection

def persist_classified(article):
    'store the classified result in mongodb'
    col = Collection(db, CLASSIFIED)
    for guess in article.labels:
        label = guess[0]
        probability = guess[1]

        # check if the label is already stored
        cursor = col.find({'word':label})
        if cursor.count():
            # should include at most on entry
            for entry in cursor:
                # articles --> (article, probability) * n
                articles = set(entry['articles'])
                # one article indeed could have several probability values
                articles.add((article, probability))
                col.update({'word':label}, {"$set", {"articles":articles}})
        else: # a new label
            articles = set([])
            articles.add((article, probability))
            col.insert({'word':label, 'articles':articles})   

def read_and_structure():
    'read data from mongodb and structure them for the classification'
    sys.path.append('../extractor/')
    import media
    
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

    collections = db.collection_names()
    training = []
    testing = []
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
                article.latin = entry['latin']

                if article.category:
                    if article.chinese or article.latin:
                        training.append(article)
                else:
                    if article.chinese or article.latin:
                        testing.append(article)
    return training, testing

def main():
    'read the data, train the classifier and classify articles'
    # read from data source
    training, testing = read_and_structure()

    # train
    import naive_bayes
    nb = naive_bayes.NaiveBayes(training)
    nb.train()

    # classify
    for article in testing:
        # article will be classified with lables
        nb.classify(article)
        persist_classified(article)
    
if __name__ == "__main__":
    main()
