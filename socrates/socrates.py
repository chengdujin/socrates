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


def get():
    '''1. get the segmented words
       2. rank the words
       3. classify the words
       4. find articles related
       5. rank the articles
       7. output the articles
    '''
    sys.path.append('../generator')
    import interest_generator
    cluster = interest_generator.generate('twitter/perryhau') 
    import ranker
    ranked = ranker.rank_segments(cluster)

    print '\nclassifying ...'
    import naive_bayes
    labels = []
    nb = naive_bayes.NaiveBayes(ranked)
    for doc in ranked:
        labels.extend(nb.classify(doc))
    
    # retrieve articles of these labels
    from pymongo.connection import Connection 
    con = Connection('176.34.54.120:27017')
    from pymongo.database import Database
    db = Database(con, 'articles')
    from pymongo.collection import Collection
    col = Collection(db, 'classified')

    import readable
    print 'read from database ...'
    result = {}
    for label in labels:
        print label[0]
        record = col.find_one({'word':label[0]})
        if record:
            print 'actually we have found something for %s' % label[0]
            articles = record['articles']
            selected = []
            # select the latest a few and rank
            for id, key in enumerate(sorted(articles.iterkeys())):
                if id > 50:
                    break
                else:
                    selected.append((float(articles[key]), key)) 
            sorted_selected = []
            for id, key in enumerate(sorted(selected, key=lambda p:-p[0])):
                sorted_selected.append(selected[id][1])
            result[label[0]] = sorted_selected
            readable.generate_html(sorted_selected)
            print label[0], ','.join(sorted_selected)
        else:
            print 'no articles found for keyword %s' % label[0]
            continue
    return result

if __name__ == "__main__":
    get()
