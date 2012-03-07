#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# this script serves to do the dirty cleaning work for
# users' tweets.
# 
# @author Yuan JIN
# @contact chengdujin@gmail.com
# @since 2012.03.06
# @latest 2012.03.06
#

# reload the script encoding
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')


class Tweet:
    'class dedicated to tweet modeling'
    def __init__(self, id_ = None, text= None, favorited = None, created_at= None, retweeted = None, source = None):
        self.id_ = id_
	self.text = text
        self.favorited = favorited
        self.created_at = created_at
        self.retweeted = retweeted
        self.source = source
	
	# properties importantes
        self.users = []
        self.urls = []
        self.hashtags = []
        
	self.keywords = []
        self.chinese = []
        self.latin = []

    def __str__(self):
        return 'keywords:\n' + str(self.keywords) + '\nchiense:\n' + str(self.chinese) + '\nlatin:\n' + str(self.latin) + '\nurls:\n' + str(self.urls) + '\nhashtags:\n' + str(self.hashtags) + '\nusers:\n' + str(self.users) + '\ncreated_at:\n' + str(self.created_at) + '\nsource:\n' + str(self.source) + '\n'

def segment_tweet():
    ''
    pass

def filter_tweet(word_list):
    'remove punctuations, digits, space and separate chinese and latins'
    import re, string
    
    chinese = []
    latin = []
    identify = string.maketrans('', '')
    for word in word_list:
        # remove unnecessary characters
        word = (word.encode('utf-8')).translate(identify, string.punctuation)
        if word.isalpha():
            # then it is composed of alphabets, francais?
            latin.append(word.decode('utf-8'))
        else: # japanaese?
            chinese.append(word.decode('utf-8'))

    return chinese, latin

def clean_data(tweets):
    '''text reduction and collection, including the following
       1. collect users involved
       2. collect urls
       3. collect hashtags
       4. remove emotion words
       5. separate chinese and english'''
    sys.path.append("/Users/Yuan/Downloads/socrates/libs/tweetmotif/")
    import ttp, HTMLParser
    
    tweet_instances = []
    for tweet in tweets:
        # tweet id
        tweet_instance = Tweet(tweet['id'])
        tweet_instance.created_at = tweet['created_at']        
        tweet_instance.source = HTMLParser.HTMLParser().unescape(tweet['source'])
        tweet_instance.retweeted = tweet['retweet_count']
        tweet_instance.favorited = tweet['favorited']

        text = HTMLParser.HTMLParser().unescape(tweet['text'])
        tweet_instance.text = text
        parsed_text = ttp.Parser().parse(text)

        # tweet replied users
	tweet_instance.users = parsed_text.users
        for user in tweet_instance.users:
            user = '@%s' % user
            if user in text:
                text =  text.replace(user, '')
        # tweet hashtags
        tweet_instance.hashtags = parsed_text.tags
        for hashtag in tweet_instance.hashtags:
            hashtag = '#%s' % hashtag
            if hashtag in text:
                text = text.replace(hashtag, '')
        # tweet urls
        tweet_instance.urls = parsed_text.urls
        for url in tweet_instance.urls:
            if url in text:
                text = text.replace(url, '')
        
        # separate chinese and latin, remove emotions and others 
        segments = text.split(' ')
        chinese, latin = filter_tweet(segments)
        tweet_instance.chinese = chinese
        tweet_instance.latin = latin

        tweet_instances.append(tweet_instance)
        if tweet_instance.hashtags:
            print str(tweet_instance)
    return tweet_instances

def collect_data():
    'collect data from mongodb'
    # stop words for tweet info keys
    screen_tweet_info = ['_id', 'truncated', 'place', 'geo', 'retweeted', 'coordinates', 'in_reply_to_status_id', 'in_reply_to_screen_name', 'in_reply_to_user_id', 'user']
    tweets = []    

    from pymongo import Connection
    con = Connection('localhost', 27017)
    cursor = con.tweets.tweets.find()
    if cursor.count() > 0:
        for tweet_mongo in cursor:
            tweet = {}
            for key in tweet_mongo.keys():
		if not (key in screen_tweet_info):
		    # unicode
                    tweet[key] = (tweet_mongo[key])
	    if tweet:
	        tweets.append(tweet)
    else:
        print '[Error] Nothing is found for the user'
    
    return tweets

def main():
    'collect the data and rinse them'
    tweet_list = collect_data()
    clean_list = clean_data(tweet_list)

if __name__ == '__main__':
    main()

