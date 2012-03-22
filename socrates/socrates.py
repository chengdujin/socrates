#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# this script is the main entrance to the 
# backend code.
#
# @author Yuan JIN
# @contact chengdujin@gmail.com
# @since 2012.03.22
# @latest 2012.03.22
#

# reload the script encoding
import sys 
reload(sys)
sys.setdefaultencoding('UTF-8')


def get()
    '''1. get the segmented words
       2. rank the words
       3. classify the words
       4. find articles related
       5. rank the articles
       7. output the articles
    '''
    sys.path.append('../generator')
    import interest_generator
    cluster = interest_generator.generate('articles/perryhau') 
    import ranker
    ranked = ranker.rank_segments(cluster)
    import naive_bayes
    labels = []
    for doc in ranked:
        labels.extend(naive_bayes.classify(ranked))
    
    # retrieve articles of these labels
    from pymongo.connection import Connection 
    con = Connection('176.34.54.120:27017')
    from pymongo.database import Database
    db = Database(con, 'articles')
    from pymongo.collection import collection
    col = Collection(db, 'classified')

    result = {}
    for label in labels:
        record = col.find_one({'word':label})
        articles = record['articles']
        selected = {}
        # select the latest a few and rank
        for id, key in enumerate(sorted(articles.iterkeys())):
            if id > 50:
                break
            else:
                selected[float(articles[key])] = key 
        sorted_selected = []
        for key in sorted(selected.iterkeys()):
            sorted_selected.append(selected[key])
        result[label] = sorted_selected
    return result

if __name__ == "__main__":
    main()
