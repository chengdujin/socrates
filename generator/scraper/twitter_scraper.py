#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# this script serves to retrieve all the tweets of a user, and
# do some text mining based on the data
#
# @author Yuan JIN
# @contact chengdujin@gmail.com
# @since 2012.03.01
# @latest 2012.04.07

import httplib
from BeautifulSoup import BeautifulStoneSoup
import HTMLParser
import time

# reload the script encoding
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

# CONSTANTS
f = open('config', 'r')
constants = f.readlines()
CONSTANTS = dict(map(lambda x:tuple((x[:-1] if x[-1] == '\n' else x).split('=')), constants))
f.close()

# initialization
from pymongo.connection import Connection
mongo_con = Connection(CONSTANTS['DB'])
from pymongo.database import Database
db = Database(mongo_con, 'twitter')
from pymongo.collection import Collection
coll = Collection(db, CONSTANTS['TWITTER_USER'])

tweet_properties = ['text', 'favorite', 'retweet_count', 'created_at', 'id' ]


def convert_time(time_str):
    'convert twitter time format to common one'
    return time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(time_str,'%a %b %d %H:%M:%S +0000 %Y'))

def parse_and_store(user, data):
    if not data:
        return None

    root = BeautifulStoneSoup(data)
    tweets = root.contents[2].contents
    lowest_id = ''
    for tweet in tweets:
        if tweet <> '\n':
            doc = {}
            for item in tweet.contents:
                if item <> '\n':
                    try:
                        if item.string and item.name in tweet_properties:
                            item_value = HTMLParser.HTMLParser().unescape(str(item.string))

                            if item.name == 'created_at':
                                item_name = 'published'
                                item_value = convert_time(item_value)
                            elif item.name == 'retweet_count':
                                item_name = 'retweeted'
                            else:
			                    item_name = item.name

                            if isinstance(item_value, str):
                                item_value = item_value.decode('utf-8')
                            doc[item_name] = item_value
                    except Exception as e:
                        print tweet

            if doc and 'id' in doc:
                coll.save(doc)
                lowest_id = doc['id']
    return lowest_id

def retrieve_data(user, max_id):
    http_con = httplib.HTTPConnection("api.twitter.com")
    http_con.request("GET", "/1/statuses/user_timeline.xml?contributor_details=0&trim_user=1&count=100&screen_name=%s&%s" % (user, max_id))
    reply = http_con.getresponse()
    data = reply.read()
    http_con.close()
    return data

def scrape():
    'entrance to tweets retrieval'
    max_id = ''
    while True:
        data = retrieve_data(CONSTANTS['TWITTER_USER'], max_id)
        max_id = parse_and_store(CONSTANTS['TWITTER_USER'], data)
        print max_id
        if not max_id:
            break
        else:
            max_id = 'max_id=' + str(int(max_id) - 1)

if __name__ == '__main__':
    scrape()
