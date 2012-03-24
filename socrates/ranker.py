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
    import time
    return int(time.strftime('%Y%m%d%H%M%S', time.strptime(orthod_time,'%a %b %d %H:%M:%S +0000 %Y')))

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
    scored_docs = []
    for collection in docs:
        score = score_segments(collection)
        scored_docs.append((score, collection))

    # ranking
    ranked_docs = []
    sorted_docs = sorted(scored_docs, key=lambda p:-p[0])
    for sd, sorted_doc in enumerate(sorted_docs):
        if sd > 5:
            break
        else:
            ranked_docs.append(sorted_doc[1])
    return ranked_docs

def rank(docs):
    'interface to ranking facility'
    return rank_segments(docs)

if __name__ == "__main__":
    rank()
