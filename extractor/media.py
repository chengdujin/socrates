#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# this script serves to model a media type
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


class Document(object):
    'parent class of all source classes'
    def __init__(self):
        pass

    def collect_data(self, database):
        pass

    def read_databse(self, collection, screen_keys):
        'read out unicode data from mongodb'
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
	    return Exception("[error] read_databse: nothing is found!")

    def build_model(self, doc):
        pass


class Twitter(Document):
    'class that deals with twitter specific issues'
    def __init__(self):
	pass

    def collect_data(self, database):
        con = Connection(database['host'], database['port'])
        collection = con.tweets.tweets

        twitter_screen_keys = ['_id', 'truncated', 'place', 'geo', 'retweeted', 'coordinates', 'in_reply_to_status_id', 'i    n_reply_to_screen_name', 'in_reply_to_user_id', 'user']
        return super(Twitter, self).read_databse(collection, twitter_screen_keys)

    def __separate_languages(self, text):
        'remove punctuations, digits, space and separate chinese and latins'
        import re, string
    
        segments = text.split(' ')
        chinese = []
        latin = []
        chinese_punctuation = '！￥（）【】、‘’“”；：？。，《》' # utf-8 size: 3 unicode: 1
        trans_table = string.maketrans(string.punctuation, ' ' * len(string.punctuation)) 
        for word in segments:
            # remove unnecessary characters
            word = (word.encode('utf-8')).translate(trans_table).strip()
            if word.isalpha():
                # then it is composed of alphabets, francais?
		if len(word) > 2: # no need to keep a word with a length less than 3 letters
                    latin.append(word.decode('utf-8'))
            else: # japanaese?
                chinese.append(word.decode('utf-8'))

        return chinese, latin

    def build_model(self, doc):
        '''text reduction and collection, including the following
           1. collect users involved
           2. collect urls
           3. collect hashtags
           4. remove emotion words
           5. separate chinese and english'''
        
        import ttp, HTMLParser
	tweet = Tweet(doc['id'])
        tweet.created_at = doc['created_at']            
        tweet.source = HTMLParser.HTMLParser().unescape(doc['source'])
        tweet.retweeted = doc['retweet_count']
        tweet.favorited = doc['favorited']

        text = HTMLParser.HTMLParser().unescape(doc['text'])
        tweet.text = text
        parsed_text = ttp.Parser().parse(text)

        # tweet replied users
        tweet.users = parsed_text.users
        for user in tweet.users:
            user = u'@%s' % user
            if user in text:
                text =  text.replace(user, '') 
        # tweet hashtags
        tweet.hashtags = parsed_text.tags
        for hashtag in tweet.hashtags:
            hashtag = u'#%s' % hashtag
            if hashtag in text:
                text = text.replace(hashtag, '') 
        # tweet urls
        tweet.urls = parsed_text.urls
        for url in tweet.urls:
            if url in text:
                text = text.replace(url, '') 
            
        # separate chinese and latin, remove emotions and others 
        chinese, latin = self.__separate_languages(text)
        tweet.chinese = chinese
        tweet.latin = latin
        
        return tweet


class Tweet:
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
