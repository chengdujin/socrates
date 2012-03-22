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

from pymongo.errors import CollectionInvalid
from pymongo.connection import Connection
con = Connection(DB)
from pymongo.database import Database
db = Database(con, ARTICLES)
from pymongo.collection import Collection

def persist_classified(article, label_stats):
    'store the classified result in mongodb'
    try:
        col = db.create_collection(CLASSIFIED)
    except CollectionInvalid as e:
        col = Collection(db, CLASSIFIED)

    for guess in article.labels:
        label = guess[0]
	label_stats.append(label)
        probability = guess[1]

        # check if the label is already stored
        cursor = col.find({'word':label})
        if cursor.count():
            # should include at most on entry
            for entry in cursor:
                # articles --> (article, probability) * n
                articles = entry['articles']
                if str(article._id) in articles:
                    old_probability = articles[str(article._id)]
                    if probability > old_probability:
                        articles[str(article._id)] = probability
                else:
                    articles[str(article._id)] = probability
                col.update({'word':label}, {"$set": {"articles":articles}})
        else: # a new label
            articles = {}
            articles[str(article._id)] = probability
            col.insert({'word':label, 'articles':articles})   
	return list(set(label_stats))

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
                if '_id' in entry:
                    article._id = entry['_id']
                if 'title' in entry:
                    article.title = entry['title']
                if 'published' in entry:
                    article.published = entry['published']
                if 'source' in entry:
                    article.source = entry['source']
                if 'category' in entry:
                    article.category = restructure(entry['category'])
                if 'chinese' in entry:
                    article.chinese = entry['chinese']
                if 'latin' in entry:
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
    print 'read data from mongodb'
    training, testing = read_and_structure()

    # train
    print 'training ...'
    import naive_bayes
    nb = naive_bayes.NaiveBayes(training)
    nb.train()

    # classify
    print 'classifying'
    articles = testing + training
    total = len(articles)
    labels = []
    for aid, article in enumerate(articles):
        # article will be classified with lables
        nb.classify(article)
        labels = persist_classified(article, labels)
        print '[%s] %i' % ('-' * int(float(aid) / float(total) * 50),  int(float(aid) / float(total) * 100)) + "%"
    
if __name__ == "__main__":
    main()
