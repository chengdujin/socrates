#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# this script serves to model a media type
#
# @author Yuan JIN
# @contact chengdujin@gmail.com
# @since 2012.03.07
# @latest 2012.03.13
#


# reload the script encoding
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

# CONSTANTS
DB = '176.34.54.120:27017'

class Document(object):
    'parent class of all source classes'
    def __init__(self):
        pass

    def collect_data(self, database):
        'read out unicode data from mongodb'
        from pymongo.connection import Connection
        con = Connection(DB)
        from pymongo.database import Database
        db = Database(con, database['db']) 
        from pymongo.collection import Collection
        col = Collection(db, database['collection'])
        
        screener = None
        if 'screener' in database:
            screener = database['screener']

        docs = []
        cursor = col.find()
        if cursor.count() > 0:
            for entry in cursor:
                doc = {}
                for key in entry.keys():
                    if screener and not key in screener:
                        doc[key] = entry[key]
                    elif not screener:
                        doc[key] = entry[key]
                if doc:
                    docs.append(doc)
            return docs
        else:
            return Exception("[error] collect_data: nothing is found!")

    def build_model(self, doc):
        pass

    def separate_languages(self, text):
        'remove punctuations, digits, space and separate chinese and latins'
        import re, string
    
        segments = text.split(' ')
        chinese = []
        latin = []
        unwanted = string.punctuation + string.digits
        trans_table = string.maketrans(unwanted, ' ' * len(unwanted)) 
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


class Twitter(Document):
    'class that deals with twitter specific issues'
    def __init__(self):
	pass

    def collect_data(self, database):
        database['screener'] = ['truncated', 'place', 'geo', 'retweeted', 'coordinates', 'in_reply_to_status_id', 'in_reply_to_screen_name', 'in_reply_to_user_id', 'user']
        return super(Twitter, self).collect_data(database)

    def build_model(self, doc):
        '''text reduction and collection, including the following
           1. collect users involved
           2. collect urls
           3. collect hashtags
           4. remove emotion words
           5. separate chinese and english'''
        sys.path.append('../libs/twitter-text-python/build/lib') 
        import ttp, HTMLParser
        
        tweet = Tweet()
        if 'id_' in doc:
            tweet.id_ = doc['id_']
        if '_id' in doc:
            tweet._id = doc['_id']
        if 'created_at' in doc:
            tweet.published = doc['created_at']            
        if 'source' in doc:
            tweet.source = HTMLParser.HTMLParser().unescape(doc['source'])
        if 'retweet_count' in doc:
            tweet.retweeted = doc['retweet_count']
        if 'favorited' in doc:
            tweet.favorited = doc['favorited']

        if 'text' in doc:
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
            chinese, latin = super(Twitter, self).separate_languages(text)
            tweet.chinese = chinese
            tweet.latin = latin
        
        return tweet


class News(Document):
    'class that deals with news sources mainly collected from rss via google reader'
    def __init__(self):
        pass

    def collect_data(self, database):
        return super(News, self).collect_data(database)

    def build_model(self, doc):
        article = Article() 
        if '_id' in doc:
            article._id = doc['_id']
        if 'author' in doc:
            article.author = doc['author']
        if 'title' in doc:
            article.title = doc['title']
        if 'published' in doc:
            article.published = doc['published']
        if 'source' in doc:
            article.source = doc['source']
        if 'category' in doc:
            article.category = doc['category']
    
        if 'title' in doc:
            chinese, latin = super(News, self).separate_languages(doc['title'])
            article.chinese = chinese
            article.latin = latin
        return article


class Article():
    ''
    def __init__(self, _id = None, author = None, title = None, published = None, source = None, category = None):
        # id_ - document id, which should be mapped to _id in mongodb
        self._id = _id
        self.author = author
        self.title = title
        self.published = published
        self.source = source
        self.category = []
        
        # labels are classified category information
        self.labels = []
        self.chinese = []
        self.latin = []
        
    def __str__(self):
        return 'title:\n' + str(self.title) + '\nauthor:\n' + str(self.author) + '\npublished:\n' + str(self.published) + '\nsource:\n' + str(self.source) + '\ncategory:\n' + ','.join(self.category) + '\nchinese:\n' + ','.join(self.chinese) + '\n'  


class Tweet:
    def __init__(self, id_ = None, _id = None, text = None, favorited = None, published = None, retweeted = None, source = None):
        # id_ - twitter id, which, however, should be mapped to _id in mongodb, not twitter id
        self.id_ = id_
        # mongodb id
        self._id = _id
        self.text = text
        self.favorited = favorited
        self.published = published
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
        return 'keywords:\n' + str(self.keywords) + '\nchinese:\n' + str(self.chinese) + '\nlatin:\n' + str(self.latin) + '\nurls:\n' + str(self.urls) + '\nhashtags:\n' + str(self.hashtags) + '\nusers:\n' + str(self.users) + '\npublished:\n' + str(self.created_at) + '\nsource:\n' + str(self.source) + '\n'

class Segment:
    'class to model a segment, including chinese, japanase and english'
    def __init__(self, word, entry):
        self.word = word
        # use mongodb id_ to relate segmented words to an item
        if 'id_' in entry.keys():
            self.id_ = entry['id_']
        if 'published' in entry.keys():
            self.published = entry['published']
        if 'retweeted' in entry.keys():
            self.retweeted = entry['retweeted']
        if 'favorited' in entry.keys():
            self.favorited = entry['favorited']
        if 'users' in entry.keys():
            self.no_users = len(entry['users'])
    
    def __str__(self):
        return self.word
