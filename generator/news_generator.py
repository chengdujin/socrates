#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# this script serves to integrate classifier
# and cluster scripts
#
# @author Yuan JIN
# @contact chengdujin@gmail.com
# @since 2012.03.16
# @latest 2012.03.16
#


# reload the script encoding
import sys 
reload(sys)
sys.setdefaultencoding('UTF-8')

# CONSTANTS
DB = '176.34.54.120:27017'
database = 'articles'


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
    'read the data, train the classifier and cluster them'
    # read from data source
    articles = read _and_structure()

    # separate training articles and testing ones
    training_size = int(len(articles) * 0.95)
    training = []
    for id in range(training_size):
        article = articles.pop()
        training.append(article)

    # classify
    import naive_bayes
    nb = naive_bayes.NaiveBayes(training)
    nb.train()

    for article in articles:
        # article will be classified with a lables
        nb.classify(article)

    # cluster
    import k_means
    km = k_means.KMeans(articles, 3)
    km.cluster()

    # publish
    for cluster in km.clusters:
        centroid = cluster.centroid
        print 'centroid: ', centroid.title
        print 'category: ', ','.join(centroid.category)
        print 'labels: ', ','.join(centroid.labels)
        for id, point in enumerate(cluster.points):
            print '    %s. ' % str(id + 1), point.title
        print

if __name__ == "__main__":
    main()
