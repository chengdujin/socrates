#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# this script serves to model a tweet
#
# @author Yuan JIN
# @contact chengdujin@gmail.com
# @since 2012.03.07
# @latest 2012.03.07
#

from pymongo import Connection
# reload the script encoding
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')


class Document:
    'parent class of all source classes'
    def __init__(self):
        pass

    def read_database(self, database):
        pass

    def find_database(self, collection, screen_keys):
        docs = []
        cursor = collection.find()
        if cursor.count() > 0:
            for entry in cursor:
		doc = {}
                for key in entry.keys():
		    if not key in screen_keys:
			doc[key] = entry[key]
	        if doc:
		    docs.append(doc)
	    return docs
	else:
	    return Exception("[error] find_database: nothing is found!")

    def build_model(self, doc):
        pass


class Twitter(Document):
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

    def read_database(self, database):
        con = Connection(database['host'], database['port'])
        collection = con.tweets.tweets

        twitter_screen_keys = ['_id', 'truncated', 'place', 'geo', 'retweeted', 'coordinates', 'in_reply_to_status_id', 'i    n_reply_to_screen_name', 'in_reply_to_user_id', 'user']
        return Document.find_database(collection, twitter_screen_keys)

    def build_model(self, doc):
        '''text reduction and collection, including the following
           1. collect users involved
           2. collect urls
           3. collect hashtags
           4. remove emotion words
           5. separate chinese and english'''
        
        import ttp, HTMLParser, Tweet
	item = Tweet.Tweet(tweet['id'])
        item.created_at = tweet['created_at']            
        item.source = HTMLParser.HTMLParser().unescape(tweet['source'])
        item.retweeted = tweet['retweet_count']
        item.favorited = tweet['favorited']

        text = HTMLParser.HTMLParser().unescape(tweet['text'])
        item.text = text
        parsed_text = ttp.Parser().parse(text)

        # tweet replied users
        item.users = parsed_text.users
        for user in item.users:
            user = '@%s' % user
            if user in text:
                text =  text.replace(user, '') 
        # tweet hashtags
        item.hashtags = parsed_text.tags
        for hashtag in item.hashtags:
            hashtag = '#%s' % hashtag
            if hashtag in text:
                text = text.replace(hashtag, '') 
        # tweet urls
        item.urls = parsed_text.urls
        for url in item.urls:
            if url in text:
                text = text.replace(url, '') 
            
        # separate chinese and latin, remove emotions and others 
        segments = text.split(' ')
        chinese, latin = __filter_tweet(segments)
        item.chinese = chinese
        item.latin = latin
