#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# this script serves to provide ranking
# facility to segment ranking and article
# ranking.
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

# CONSTANTS
TWITTER_BASETIME = 200603212150

def convert_time(orthod_time):
    'convert a twitter orthodox time into integer'
    return 201203230425

def score_segment(word):
    ''
    # word is an instance of media.Segment
    # year and month are kept integer
    import math
    normalized_time = float(convert_time(word.published) - TWITTER_BASETIME) / 100
    word.retweeted = 2
    normalized_rt = 0.5 * math.log(float(word.retweeted), 5)
    normalized_fv = 0.2 * (1 if word.favorited else 0)
    normalized_nu = 0.4 * word.no_users  
    return float(normalized_nu + normalized_rt + normalized_fv) * float(normalized_time)

def score_segments(collection):
    '''1. the centroid is the very influential
       2. compute average score via the following factors:
        a) published time
        b) retweeted times
        c) is it favorited
        d) users of importance
    '''
    if not collection:
        return 0
    centroid = score_segment(collection[0])
    points = collection[1:]
    total = 0
    for point in points:
        total += score_segment(point)
    return float(centroid) * 0.35 + float(total) / float(len(points) + 1) * 0.65

def rank_segments(docs):
    'method to rank segments'
    'docs is a collection of collections of segments'
    'the idea is to rank the collections by its average ranking score'
    scored_docs = {}
    for collection in docs:
        score = score_segments(collection)
        strs = [c.word for c in collection]
        scored_docs[','.join(strs)] = score

    # ranking
    from ordereddict import OrderedDict
    sorted_docs = OrderedDict(sorted(scored_docs.items(), key=lambda x: -x[1]))  
    ranked_docs = []
    for sd, (k, v) in enumerate(sorted_docs.items()):
        if sd > 5:
            break
        else:
            print k
            k_splits = k.split(',')
            ranked_docs.append(k_splits)
    return ranked_docs

def rank(docs):
    'interface to ranking facility'
    return rank_segments(docs)

if __name__ == "__main__":
    rank()
