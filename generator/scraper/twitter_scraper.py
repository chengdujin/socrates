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

# reload the script encoding
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

# CONSTANTS
f = open('config', 'r')
constants = f.readlines()
CONSTANTS = dict(map(lambda x:tuple((x[:-1] if x[-1] == '\n' else x).split('=')), constants))
f.close()

def parse_and_store(user, data):
    from pymongo.connection import Connection
    con = Connection(DB)
    from pymongo.database import Database
    db = Database(con, 'twitter')
    from pymongo.collection import Collection
    collection = Collection(db, user)

    from BeautifulSoup import BeautifulStoneSoup
    root = BeautifulStoneSoup(data)
    tweets = root.contents[2].contents
    lowest_id = ''
    for tweet in tweets:
        if tweet <> '\n':
            doc = {}
            for item in tweet.contents:
                if item <> '\n':
		    try:
			if item.string == 'created_at':
			    item_name = 'published'
			else:
			    item_name = item.name
                        doc[item_name] = str(item.string)
		    except Exception as e:
			print tweet
            if doc:
		if 'id' in doc:	
                    collection.save(doc)
                    lowest_id = doc['id']
    return lowest_id

def retrieve_data(user, max_id):
    import httplib
    con = httplib.HTTPConnection("api.twitter.com")
    con.request("GET", "/1/statuses/user_timeline.xml?contributor_details=0&trim_user=1&count=100&screen_name=%s&%s" % (user, max_id))
    reply = con.getresponse()
    data = reply.read()
    con.close()
    return data

def scrape():
    'entrance to tweets retrieval and analysis'
    max_id = ''
    while True:
        data = retrieve_data(USER, max_id)
        max_id = parse_and_store(USER, data)
        print max_id
        if not max_id:
            break
        else:
            max_id = 'max_id=' + str(int(max_id) - 1)

if __name__ == '__main__':
    scrape()
